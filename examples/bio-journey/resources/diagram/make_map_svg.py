#!/usr/bin/env python3
"""
Generates the world-map backdrop and the flight-route overlay for `bio-journey`.

Two layers come out of one run, both on the shared 1920x1080 viewBox:

  world_map.svg     the land silhouette + a graticule. Backdrop.
  flights_layer.svg one <path> per flight, each a dense polyline. The rails the
                    planes ride.

Nothing here is drawn by hand. The land comes from Natural Earth (public domain,
committed beside this script as ne_110m_land.geojson); the routes are computed as
true GREAT CIRCLES between the city coordinates in CITIES, then projected. That is
the whole point of the layer: the arc you see and the arc a plane rides are one
path, and moving a city moves both.

Projection is equirectangular (plate carree) for one reason: longitude and latitude
map to x and y LINEARLY, so a city's pixel position is arithmetic rather than a
fitted guess. A great circle is not a straight line under it — it bows poleward,
which is exactly the airline-map look.

Arc length is printed per route because there is no `.length` on a path in the
language: a scene divides a pasted pixel figure by a shared pace to get its
duration. Paste the printed FLIGHT_*_PX consts into scene_03_map.yaml, or the
plane's speed drifts from the line drawn.

Usage:
    ./make_map_svg.py            # regenerate both layers, print the const block
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Canvas ───────────────────────────────────────────────────────────────────
# Matches the other examples' 1920x1080 so a template and CSS can be shared.
WIDTH = 1920
HEIGHT = 1080

# The window on the world is a FRAMING choice, and the only one in this file.
#
# A full globe was the first attempt and it composes badly: Honolulu, Austin and
# Paris span 160 degrees of longitude, so on a 360-degree map all three sit in the
# left half and the right half is empty Pacific. Cropping to the region the routes
# actually cross spreads them across the frame and lets the planes be large enough
# to read.
#
# Both axes keep the SAME degrees-per-pixel scale, so nothing is stretched -- the
# latitude band is whatever that scale makes it, centred vertically. Honolulu is the
# westernmost subject, so the west edge sits just far enough past it to leave the
# marker room; the east edge leaves a wider margin because the Paris callout hangs
# there.
LON_MIN, LON_MAX = -175.0, 45.0
LAT_MAX, LAT_MIN = 70.0, -50.0

PX_PER_DEG = WIDTH / (LON_MAX - LON_MIN)
BAND_HEIGHT = (LAT_MAX - LAT_MIN) * PX_PER_DEG
BAND_TOP = (HEIGHT - BAND_HEIGHT) / 2.0

# ── Subject ──────────────────────────────────────────────────────────────────
# The three cities the piece names. Coordinates are the conventional city centres.
CITIES = {
    "austin": (30.2672, -97.7431),
    "honolulu": (21.3069, -157.8583),
    "paris": (48.8566, 2.3522),
}

# One entry per flight. `id` becomes the <path> id a scene rides by name.
FLIGHTS = [
    {"name": "honolulu", "id": "flight-honolulu", "from": "austin", "to": "honolulu"},
    {"name": "paris", "id": "flight-paris", "from": "austin", "to": "paris"},
]

# Points sampled along each great circle. Dense enough that `orient: auto` reads as
# a smooth turn rather than a series of kinks.
ARC_STEPS = 120

# Graticule spacing in degrees; 0 disables it.
GRATICULE_LON = 30
GRATICULE_LAT = 20


def project(lat, lon):
    """Equirectangular: degrees to canvas pixels."""
    x = (lon - LON_MIN) * PX_PER_DEG
    y = BAND_TOP + (LAT_MAX - lat) * PX_PER_DEG
    return x, y


def great_circle(lat1, lon1, lat2, lon2, steps=ARC_STEPS):
    """
    Sample a great circle between two points by interpolating on the unit sphere.

    Straight spherical interpolation (slerp) of the two position vectors. The
    result is the shortest path over a sphere, which is what an aircraft actually
    flies and what makes the drawn line bow toward the pole.
    """
    p1 = _unit(lat1, lon1)
    p2 = _unit(lat2, lon2)

    dot = max(-1.0, min(1.0, sum(a * b for a, b in zip(p1, p2))))
    omega = math.acos(dot)
    if omega < 1e-9:
        return [(lat1, lon1)]

    out = []
    sin_omega = math.sin(omega)
    for i in range(steps + 1):
        t = i / steps
        a = math.sin((1.0 - t) * omega) / sin_omega
        b = math.sin(t * omega) / sin_omega
        v = tuple(a * p1[k] + b * p2[k] for k in range(3))
        out.append(_latlon(v))
    return out


def _unit(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def _latlon(v):
    x, y, z = v
    hyp = math.hypot(x, y)
    return (math.degrees(math.atan2(z, hyp)), math.degrees(math.atan2(y, x)))


def polyline(points):
    """Projected lat/lon pairs to an SVG polyline `d`, and its pixel length."""
    pts = [project(lat, lon) for lat, lon in points]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    length = sum(
        math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)
    )
    return d, length


def land_paths():
    """Natural Earth land polygons as SVG path data, one per ring."""
    with open(os.path.join(HERE, "ne_110m_land.geojson"), encoding="utf-8") as fh:
        gj = json.load(fh)

    out = []
    for feature in gj["features"]:
        geom = feature["geometry"]
        polys = (
            [geom["coordinates"]]
            if geom["type"] == "Polygon"
            else geom["coordinates"]
        )
        for poly in polys:
            for ring in poly:
                # Drop rings entirely outside the latitude clip; clamp the rest so a
                # polygon straddling the edge still closes instead of flying off.
                if all(lat < LAT_MIN or lat > LAT_MAX for _, lat in ring):
                    continue
                pts = [
                    project(max(LAT_MIN, min(LAT_MAX, lat)), lon) for lon, lat in ring
                ]
                if len(pts) < 3:
                    continue
                out.append(
                    "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
                )
    return out


def graticule():
    lines = []
    if GRATICULE_LON:
        lon = LON_MIN
        while lon <= LON_MAX:
            d, _ = polyline([(LAT_MAX, lon), (LAT_MIN, lon)])
            lines.append(d)
            lon += GRATICULE_LON
    if GRATICULE_LAT:
        lat = math.ceil(LAT_MIN / GRATICULE_LAT) * GRATICULE_LAT
        while lat <= LAT_MAX:
            d, _ = polyline([(lat, LON_MIN), (lat, LON_MAX)])
            lines.append(d)
            lat += GRATICULE_LAT
    return lines


def write_world_map():
    paths = land_paths()
    grat = graticule()
    parts = [
        "<!--",
        "  GENERATED by ./make_map_svg.py - do not hand-edit; the next run overwrites it.",
        "",
        "  World-map backdrop for bio-journey. Land geometry is Natural Earth 1:110m",
        "  (public domain), projected equirectangular so that a city's pixel position is",
        "  arithmetic on its coordinates. viewBox matches the pixel size, so the flight",
        "  overlay and the marker layer address this same coordinate space.",
        "-->",
        f'<svg id="world_map" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect id="ocean" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" '
        'class="map-ocean" />',
        '  <g id="graticule" class="map-graticule">',
    ]
    parts += [f'    <path d="{d}" />' for d in grat]
    parts.append("  </g>")
    parts.append('  <g id="land" class="map-land">')
    parts += [f'    <path d="{d}" />' for d in paths]
    parts.append("  </g>")
    parts.append("</svg>")

    _write("world_map.svg", parts)
    return len(paths), len(grat)


def write_flights_layer():
    """
    One group per flight holding a casing path and the ridden path.

    The casing is a wider stroke UNDER the line, so a route stays legible where it
    crosses land; only the inner path carries an id, because only it is ridden.
    """
    parts = [
        "<!--",
        "  GENERATED by ./make_map_svg.py - do not hand-edit; the next run overwrites it.",
        "",
        "  Flight-route overlay. Each path is a great circle between two CITIES entries,",
        "  sampled and projected - not a hand-drawn arc. The id on the inner path is what",
        "  a scene names in `move ... along`, so the route travelled cannot drift from the",
        "  route drawn.",
        "-->",
        f'<svg id="flights_layer" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
    ]

    lengths = {}
    for flight in FLIGHTS:
        lat1, lon1 = CITIES[flight["from"]]
        lat2, lon2 = CITIES[flight["to"]]
        d, length = polyline(great_circle(lat1, lon1, lat2, lon2))
        lengths[flight["name"]] = length
        parts += [
            f'  <g id="{flight["id"]}-group" opacity="0">',
            f'    <path class="flight-casing" d="{d}" />',
            # Two classes: the shared one carries width and dash, the per-route one
            # carries only the hue. A new destination needs one CSS rule, not a
            # duplicated stroke declaration.
            f'    <path id="{flight["id"]}" '
            f'class="flight-line flight-line-{flight["name"]}" d="{d}" />',
            "  </g>",
        ]

    parts.append("</svg>")
    _write("flights_layer.svg", parts)
    return lengths


def _write(name, lines):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    n_land, n_grat = write_world_map()
    lengths = write_flights_layer()

    print(f"world_map.svg      {n_land} land rings, {n_grat} graticule lines")
    print(f"flights_layer.svg  {len(lengths)} routes")
    print()
    print("City positions (paste into markers_flights.svg):")
    for name, (lat, lon) in CITIES.items():
        x, y = project(lat, lon)
        print(f"  {name:<10} lat {lat:>8.4f}  lon {lon:>9.4f}  ->  x {x:7.1f}  y {y:6.1f}")
    print()
    print("Arc lengths (paste into scene_03_map.yaml `const`):")
    for name, length in lengths.items():
        print(f"  FLIGHT_{name.upper()}_PX: {length:.1f}")


if __name__ == "__main__":
    main()
