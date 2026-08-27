#!/usr/bin/env python3
"""Regenerate a route overlay SVG from an owner-authored two-colour trace over the map.

The owner paints each route directly onto a copy of the baked map (`hiking.png`) with
two flat brush colours — one per visibility state:

    VISIBLE  the walker can be seen on this stretch
    HIDDEN   the stretch rides *behind* something on the map (a tree, a hut, a
             signboard)

A run masks only its own two colours in ONE image and is blind to every other stroke on
the canvas, so routes may cross, or share the stretch out of the trailhead, without the
chainer confusing one for the other. Keeping them apart therefore needs only that a
route own its trace FILE or its colour PAIR — see ROUTES below, where some routes share
one painting under distinct pairs and others get their own painting and reuse a pair.

This script turns that painting into overlay geometry:

  1. collect every exactly-matching trace pixel (the brush is hard-edged, no
     antialiasing, so an exact match is both sufficient and precise);
  2. group them into stroke components and chain the components start → destination
     by nearest-neighbour, bridging the gaps the brush left;
  3. walk the chain with a weighted (10/14) geodesic from the start end, and
     take the centroid of the trace pixels in each arc-length bin — that yields an
     ORDERED centreline through a stroke of any thickness, which a row-scan or a
     naive nearest-point walk cannot do on switchbacks;
  4. smooth (centripetal Catmull-Rom) and resample at a fixed arc-length step;
  5. split at every visible↔hidden colour change, sharing the boundary vertex so
     consecutive segments butt together with no seam.

Each segment becomes one `<g>` holding a casing path and the route line. The line
carries its own id: `move … along: <line actor>` rides that geometry directly, so
the route the eye sees and the route the marker travels are the SAME curve — there
are no waypoints duplicated into the scene file to drift out of step.

The printed segment table (length + suggested duration at a constant walking speed)
is what the scene file's per-leg duration consts are derived from — copy it across
whenever the route changes, so the marker keeps one steady pace.

To re-route: paint a fresh trace over `hiking.png`, save it BESIDE this script, point
the route's `trace` at it, re-run, and update the scene file's `LEG_n_MS` consts (and
its asset list, if the number of stretches changed). Save it LOSSLESS if you can: a JPEG
holds no pixel at the brush colour exactly and has to be read through a `tolerance`
radius instead.

Every trace an example depends on lives HERE, next to the generator — never in a
scratch directory outside the example, which is not published and would leave a fresh
clone unable to regenerate the overlay it ships.

    usage: ./make_route_svg.py --route summit        (run from resources/diagram/)
           ./make_route_svg.py --route lake
           ./make_route_svg.py --route rest
"""

from __future__ import annotations

import argparse
import heapq
import math
from collections import deque
from dataclasses import dataclass

from PIL import Image

TRACE_DEFAULT = "hiking_trace.png"


@dataclass(frozen=True)
class Route:
    """One destination off the signpost, and how to pull it out of the shared trace."""

    title: str
    visible: str  # brush colour for the stretches where the walker is seen
    hidden: str  # brush colour for the stretches that ride behind something
    out: str  # overlay SVG this route is written to
    svg_id: str  # id of that overlay's root <svg> — the scene asset name
    prefix: str  # id stem for the emitted stretches: <prefix>-seg-01, <prefix>-line-01
    start: str  # which end of the stroke the walk begins at (see EXTREME)
    pace_kmh: float  # travel pace used to turn this route's length into a time
    ascent_m: int  # AUTHORED, not measured (see MAP_SCALE_KM_PER_1000PX)
    grade: str  # AUTHORED difficulty word for the callout's last line
    trace: str = TRACE_DEFAULT  # the painting this route is pulled out of
    tolerance: int = 0  # how far a pixel may sit from the brush colour (see read_trace)
    line_colour: str = "#8a4126"  # the drawn route's own tone (see the palette note)


# TWO things keep the routes apart, and a route needs only one of them: its own trace
# FILE, or its own colour PAIR within a shared one. Painting each route on its own copy
# of the map is the simpler habit — the pair may then be reused, since a run only ever
# looks at one file. Sharing a file demands distinct pairs instead, and buys the
# guarantee that the routes were painted in one coordinate space. Both work because a
# run masks two colours in one image and is blind to everything else on the canvas, so
# routes may cross, or share the stretch out of the trailhead, without confusing the
# chainer.
#
# The values below were checked against `hiking.png` and appear nowhere in the art,
# which is what makes the match unambiguous — re-check with a pixel scan before
# introducing a new pair.
#
# `start` names the end of the stroke the walk begins at, because the geometry alone
# cannot say which end is the trailhead. Summit climbs from the bottom of the frame;
# a route whose destination is also low would otherwise be walked backwards, and the
# only symptom is a marker that sets off from the wrong end.
#
# `tolerance` is a property of the trace's FILE FORMAT, not of the route: a lossless
# PNG holds the brush colour exactly and wants 0, while a JPEG's quantisation moves
# every painted pixel a little and needs a radius to catch them (see read_trace).
#
# PALETTE. Each route is ONE hue at three lightnesses: `line_colour` here draws the
# route, a stronger tone of the same hue carries the ring, star and travelling markers
# (in that route's marker layer), and a much darker tone sets the callout text. The
# summit's measured triplet — S57/L34 line, S80/L54 strong, S56/L19 text at hue 16 — is
# the pattern the others follow. Lightness is not free, though: the tone has to sit
# DARKER than whatever the route crosses. Blue clears the meadow at the summit's own
# lightness, but the map's trails are already sandy gold, so the rest route is
# deliberately darker (L27) or it vanishes into the path it runs along.
ROUTES = {
    "summit": Route(
        title="Summit Peak",
        visible="#d312d7",
        hidden="#0dcde3",
        out="route_layer.svg",
        svg_id="route_layer",
        prefix="route",
        start="bottom",
        pace_kmh=3.5,  # climbing pace
        ascent_m=340,
        grade="moderate",
    ),
    "river": Route(
        title="River Rapids & Kayaks",
        visible="#ff6a00",
        hidden="#00ff5a",
        out="route_layer_river.svg",
        svg_id="route_layer_river",
        prefix="river",
        start="bottom",
        pace_kmh=4.5,  # valley floor, easy going
        ascent_m=60,
        grade="easy",
    ),
    # Lake and rest are each painted on their OWN copy of the map, so both reuse the
    # summit's colour pair. The walk to the lake was traced entirely in the visible
    # brush — it never ducks behind anything — so it comes out as a single stretch and
    # the ghost marker never appears in its scene. That is the trace speaking, not a
    # limit: paint cyan where the trail passes behind the pines and it will split.
    "lake": Route(
        title="Serenity Lake",
        visible="#d312d7",
        hidden="#0dcde3",
        out="route_layer_lake.svg",
        svg_id="route_layer_lake",
        prefix="lake",
        start="bottom",
        pace_kmh=4.0,  # lakeside meadow, easy going
        ascent_m=120,
        grade="easy",
        trace="hiking_trace_lake.jpeg",
        tolerance=50,
        line_colour="#26588a",  # hue 210 at the summit's own lightness
    ),
    "rest": Route(
        title="Viewpoint Rest Stop",
        visible="#d312d7",
        hidden="#0dcde3",
        out="route_layer_rest.svg",
        svg_id="route_layer_rest",
        prefix="rest",
        start="bottom",
        pace_kmh=3.8,  # a short pull up past the cabin
        ascent_m=180,
        grade="easy",
        trace="hiking_trace_rest.jpeg",
        tolerance=50,
        line_colour="#a56f04",  # hue 40, darkened to clear the sandy trail it rides
    ),
}

# The map is a drawing, not a survey — nothing in it fixes a real-world distance. So
# ONE scale is declared here and every route's figures fall out of it, which is what
# keeps the three callouts consistent with each other and with the trace: re-paint a
# route longer and its distance and time both grow. Chosen so the summit climb reads
# as a believable half-day walk (~4.2 km).
#
# `ascent_m` and `grade` in ROUTES above are the exception — a top-down cartoon
# carries no elevation, so those are AUTHORED flavour, not derived. They are the only
# numbers in the callouts a re-trace will not correct.
MAP_SCALE_KM_PER_1000PX = 2.8


def figures(route: Route, pixels: float) -> tuple[str, str]:
    """This route's callout figures: (distance, walking time), both derived."""
    km = pixels / 1000.0 * MAP_SCALE_KM_PER_1000PX
    minutes = round(km / route.pace_kmh * 60 / 5) * 5  # to the nearest 5 min
    hours, mins = divmod(minutes, 60)
    clock = f"{hours} h {mins:02d}" if hours else f"{mins} min"
    return f"{km:.1f} km", clock

# Which end of the stroke to treat as the start: the one furthest along this axis.
EXTREME = {
    "bottom": lambda p: p[1],
    "top": lambda p: -p[1],
    "left": lambda p: -p[0],
    "right": lambda p: p[0],
}


def rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    if len(text) != 6:
        raise SystemExit(f"{value}: expected a #rrggbb colour")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))

BIN = 8.0  # arc-length bin for the geodesic centreline, px
STEP = 6.0  # resample step of the emitted polyline, px
CR_SAMPLES = 8  # Catmull-Rom samples per span
TRAVEL_MS = 14000  # total walking time the duration table is scaled to

# How hard to smooth before the spline. Each pass is a 1-2-1 average, which pulls
# the line OFF the painted centreline — it does not merely round the joins.
# Measured against the trace, over the whole route:
#
#     passes  max deviation  p95   mean   samples touching the brush edge
#       0          0.9 px    0.5   0.1     9 / 262
#       1          3.2 px    2.0   0.5    24 / 254
#       2          5.2 px    3.6   0.8    29 / 250
#
# Centripetal Catmull-Rom is INTERPOLATING — it passes through every point it is
# given — so 0 passes still glides; it just glides through the trace instead of
# across its corners. Raise this only to deliberately relax a hairpin.
SMOOTH_PASSES = 2

Point = tuple[float, float]


# ── 1. read the trace ──────────────────────────────────────────────────────────
def read_trace(
    path: str, visible: str, hidden: str, tolerance: int = 0
) -> dict[tuple[int, int], str]:
    """Pixels matching THIS route's two colours. Other routes' strokes are invisible here.

    `tolerance` is a radius in RGB space, and a pixel inside it is classified by which
    of the two brushes it is NEARER. Zero means an exact match, which is what a
    lossless trace wants — the brush is hard-edged, so exact is both sufficient and
    precise. A LOSSY trace (a JPEG) has no exactly-matching pixel anywhere: quantisation
    moves every painted pixel a little, and the symptom is a run that reports the route
    as unpainted. A radius recovers the stroke, but it is a real widening of the net —
    keep it well under the distance from either brush to anything in the art beneath,
    and check the reported stroke count and bridged gaps, since a tolerance that reaches
    into the sky or the water invents components the chainer will dutifully join.
    """
    want_visible, want_hidden = rgb(visible), rgb(hidden)
    limit = tolerance * tolerance
    image = Image.open(path).convert("RGB")
    width, height = image.size
    pixels = image.load()
    trace: dict[tuple[int, int], str] = {}
    exact = 0
    for y in range(height):
        for x in range(width):
            colour = pixels[x, y]
            if colour == want_visible:
                trace[(x, y)] = "visible"
                exact += 1
            elif colour == want_hidden:
                trace[(x, y)] = "hidden"
                exact += 1
            elif limit:
                to_visible = sum((a - b) ** 2 for a, b in zip(colour, want_visible))
                to_hidden = sum((a - b) ** 2 for a, b in zip(colour, want_hidden))
                nearest = min(to_visible, to_hidden)
                if nearest <= limit:
                    trace[(x, y)] = "visible" if to_visible <= to_hidden else "hidden"
    if not trace:
        raise SystemExit(
            f"{path}: no pixels matching {visible} / {hidden} — is this route painted yet, "
            f"and does the brush match those values exactly (no antialiasing, no opacity)? "
            f"A lossy trace (JPEG) never matches exactly; give it --tolerance."
        )
    if tolerance:
        print(f"  tolerance {tolerance}: {exact} exact px, "
              f"{len(trace) - exact} recovered within the radius")
    return trace


# ── 2. components, chained start → destination ─────────────────────────────────
def components(trace: dict[tuple[int, int], str]) -> list[list[tuple[int, int]]]:
    neighbours = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
    seen: set[tuple[int, int]] = set()
    out = []
    for seed in trace:
        if seed in seen:
            continue
        queue = deque([seed])
        seen.add(seed)
        blob = []
        while queue:
            node = queue.popleft()
            blob.append(node)
            for dx, dy in neighbours:
                near = (node[0] + dx, node[1] + dy)
                if near in trace and near not in seen:
                    seen.add(near)
                    queue.append(near)
        out.append(blob)
    return out


def closest_pair(a, b):
    best = (math.inf, None, None)
    for p in a:
        for q in b:
            d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
            if d < best[0]:
                best = (d, p, q)
    return math.sqrt(best[0]), best[1], best[2]


def bridge(blobs, start: str = "bottom") -> tuple[set[tuple[int, int]], list[tuple]]:
    """Chain the stroke components and fill the brush gaps between them.

    The chain starts at the component furthest towards `start` — the trailhead end —
    and repeatedly appends whichever remaining component is nearest.
    """
    reach = EXTREME[start]
    order = [max(range(len(blobs)), key=lambda i: max(reach(p) for p in blobs[i]))]
    left = set(range(len(blobs))) - set(order)
    joins = []
    while left:
        head = blobs[order[-1]]
        pick = min(((closest_pair(head, blobs[j]), j) for j in left), key=lambda t: t[0][0])
        (dist, p, q), j = pick
        joins.append((p, q, dist))
        order.append(j)
        left.discard(j)

    mask = {p for i in order for p in blobs[i]}
    radius = 2
    disk = [
        (dx, dy)
        for dx in range(-radius, radius + 1)
        for dy in range(-radius, radius + 1)
        if dx * dx + dy * dy <= radius * radius
    ]
    for p, q, _ in joins:
        steps = int(max(abs(q[0] - p[0]), abs(q[1] - p[1]))) + 1
        for t in range(steps + 1):
            cx = round(p[0] + (q[0] - p[0]) * t / steps)
            cy = round(p[1] + (q[1] - p[1]) * t / steps)
            for dx, dy in disk:
                mask.add((cx + dx, cy + dy))
    return mask, joins


# ── 3. ordered centreline by weighted geodesic ─────────────────────────────────
NEIGHBOURS = [
    (dx, dy, 10 if dx == 0 or dy == 0 else 14)
    for dx in (-1, 0, 1)
    for dy in (-1, 0, 1)
    if (dx, dy) != (0, 0)
]


def geodesic(mask: set[tuple[int, int]], source: tuple[int, int]) -> dict[tuple[int, int], int]:
    dist = {source: 0}
    frontier = [(0, source)]
    while frontier:
        d, node = heapq.heappop(frontier)
        if d > dist[node]:
            continue
        for dx, dy, w in NEIGHBOURS:
            near = (node[0] + dx, node[1] + dy)
            if near in mask and dist.get(near, 1 << 30) > d + w:
                dist[near] = d + w
                heapq.heappush(frontier, (d + w, near))
    return dist


def centreline(trace, mask, start_at: str = "bottom") -> list[tuple[float, float, str]]:
    seed = next(iter(mask))
    reach = geodesic(mask, seed)
    if len(reach) != len(mask):
        raise SystemExit("trace did not chain into one path — check the brush gaps")
    far = max(reach, key=reach.get)
    from_far = geodesic(mask, far)
    other = max(from_far, key=from_far.get)
    # Walk from the trailhead end: of the stroke's two ends, whichever sits furthest
    # towards `start_at`. Geometry alone cannot tell which end is the trailhead.
    toward = EXTREME[start_at]
    if toward(far) > toward(other):
        head, tail, dist = far, other, from_far
    else:
        head, tail, dist = other, far, geodesic(mask, other)
    print(f"  start {head}, destination {tail}")

    bins: dict[int, list[float]] = {}
    for p, kind in trace.items():
        d = dist.get(p)
        if d is None:
            continue
        slot = bins.setdefault(int(d / 10 / BIN), [0.0, 0.0, 0.0, 0.0])
        slot[0] += p[0]
        slot[1] += p[1]
        slot[2] += 1
        if kind == "hidden":
            slot[3] += 1
    out = []
    for key in sorted(bins):
        sx, sy, n, hidden = bins[key]
        out.append((sx / n, sy / n, "hidden" if hidden * 2 > n else "visible"))
    return out


# ── 4. smooth + resample ───────────────────────────────────────────────────────
def smooth(points: list[Point], passes: int) -> list[Point]:
    for _ in range(passes):
        out = [points[0]]
        for i in range(1, len(points) - 1):
            a, b, c = points[i - 1], points[i], points[i + 1]
            out.append(((a[0] + 2 * b[0] + c[0]) / 4, (a[1] + 2 * b[1] + c[1]) / 4))
        out.append(points[-1])
        points = out
    return points


def catmull_rom(points: list[Point], samples: int) -> list[Point]:
    """Centripetal Catmull-Rom through `points` — interpolating, no overshoot."""
    pad = [points[0]] + list(points) + [points[-1]]
    out = [points[0]]
    for i in range(len(pad) - 3):
        p0, p1, p2, p3 = pad[i], pad[i + 1], pad[i + 2], pad[i + 3]
        t = [0.0]
        for a, b in ((p0, p1), (p1, p2), (p2, p3)):
            t.append(t[-1] + max(math.dist(a, b), 1e-6) ** 0.5)
        for s in range(1, samples + 1):
            tt = t[1] + (t[2] - t[1]) * s / samples
            a1 = lerp(p0, p1, (t[1] - tt) / (t[1] - t[0]), (tt - t[0]) / (t[1] - t[0]))
            a2 = lerp(p1, p2, (t[2] - tt) / (t[2] - t[1]), (tt - t[1]) / (t[2] - t[1]))
            a3 = lerp(p2, p3, (t[3] - tt) / (t[3] - t[2]), (tt - t[2]) / (t[3] - t[2]))
            b1 = lerp(a1, a2, (t[2] - tt) / (t[2] - t[0]), (tt - t[0]) / (t[2] - t[0]))
            b2 = lerp(a2, a3, (t[3] - tt) / (t[3] - t[1]), (tt - t[1]) / (t[3] - t[1]))
            out.append(lerp(b1, b2, (t[2] - tt) / (t[2] - t[1]), (tt - t[1]) / (t[2] - t[1])))
    return out


def lerp(a: Point, b: Point, wa: float, wb: float) -> Point:
    return (a[0] * wa + b[0] * wb, a[1] * wa + b[1] * wb)


def resample(points: list[Point], step: float) -> list[Point]:
    out = [points[0]]
    carry = 0.0
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        span = math.dist(a, b)
        if span < 1e-9:
            continue
        walked = step - carry
        while walked <= span:
            f = walked / span
            out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
            walked += step
        carry = (carry + span) % step
    if math.dist(out[-1], points[-1]) > 1e-6:
        out.append(points[-1])
    return out


def polyline_length(points: list[Point]) -> float:
    return sum(math.dist(points[i], points[i + 1]) for i in range(len(points) - 1))


# ── 5. split at the colour changes ─────────────────────────────────────────────
def split(raw: list[tuple[float, float, str]], curve: list[Point]) -> list[tuple[str, list[Point]]]:
    """Cut `curve` where the raw centreline changes colour, sharing the boundary."""
    changes = []
    for i in range(len(raw) - 1):
        if raw[i][2] != raw[i + 1][2]:
            mid = ((raw[i][0] + raw[i + 1][0]) / 2, (raw[i][1] + raw[i + 1][1]) / 2)
            changes.append((min(range(len(curve)), key=lambda j: math.dist(curve[j], mid)), raw[i + 1][2]))

    segments = []
    kind = raw[0][2]
    lo = 0
    for cut, next_kind in changes:
        segments.append((kind, curve[lo : cut + 1]))
        lo, kind = cut, next_kind
    segments.append((kind, curve[lo:]))
    return [(k, pts) for k, pts in segments if len(pts) >= 2]


# ── emit ───────────────────────────────────────────────────────────────────────
HEADER = """<!--
  Route overlay — {title}. Stacked transparently over map.svg (shared 0 0 {w} {h}
  viewBox, so every overlay and the baked map address one coordinate space), and
  carrying nothing but this route's highlight. The map photo shows through, and so
  does any other route layered below.

  GENERATED by ./make_route_svg.py for route "{route}" from the owner's trace over the
  map — edit the trace and re-run, do not hand-edit the geometry. (Nothing in this
  comment may contain a double hyphen: XML forbids it, and the compiler rejects the
  whole overlay if one slips in.) Each route owns a
  colour PAIR in the one shared trace: here {vis} paints the stretches where the
  walker is VISIBLE and {hid} the stretches that ride BEHIND something on the map
  (a tree, a hut, a signboard). The trace is smoothed (centripetal Catmull-Rom) so
  the line and the marker glide instead of faceting.

  Each stretch is one <g>: a casing path for contrast against the busy map, plus the
  route line, which carries its own id. The scene file's `move … along: <line>` rides
  that line, so the drawn route and the travelled route are one curve — no waypoints
  are copied into the scene file where they could drift.

  Treatment:
    - visible line  = solid, in this route's own tone (each route owns one hue).
    - hidden line   = dashed + semi-transparent (the map idiom for "out of sight").
    - solid marker  = filled arrowhead — rides the visible stretches.
    - ghost marker  = outline-only + semi-transparent — rides the hidden stretches.
  Markers point +x at rest; `orient: auto` turns them onto the travel tangent.
-->
<svg id="{svg_id}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"
     xmlns="http://www.w3.org/2000/svg">
  <style>
    .route-casing  {{ fill: none; stroke: #fbf3ea; stroke-width: 14; opacity: 0.55;
                     stroke-linecap: round; stroke-linejoin: round; }}
    .route-visible {{ fill: none; stroke: {line}; stroke-width: 8;
                     stroke-linecap: round; stroke-linejoin: round; }}
    .hidden-casing {{ fill: none; stroke: #fbf3ea; stroke-width: 11; opacity: 0.25;
                     stroke-linecap: round; stroke-linejoin: round; }}
    .route-hidden  {{ fill: none; stroke: {line}; stroke-width: 6; opacity: 0.5;
                     stroke-dasharray: 11 10; stroke-linecap: round; stroke-linejoin: round; }}
  </style>
"""


def path_data(points: list[Point]) -> str:
    head = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
    return head + "".join(f" L {x:.1f} {y:.1f}" for x, y in points[1:])


SCENE_HEADER = '''# ------------------------------------------
# hiking-trails — Summit route, WAYPOINT form (a test bed for `along.smoothing`)
# ------------------------------------------
# GENERATED by `resources/diagram/make_route_svg.py --scene` — do not hand-edit; the
# waypoints below are the same trace `{svg}` draws.
#
# A companion to `scene_summit.yaml`, which rides the overlay's `<path>`s by name.
# This one carries the route as an explicit `along.segments` POLYLINE instead, because
# `smoothing` applies only when every segment is a point — one asset segment anywhere in
# an `along` and the field is rejected. So the smoothing field can only be exercised from
# a waypoint route like this one.
#
# The polyline is deliberately UNSMOOTHED and coarsely sampled ({step:g} px between
# waypoints, no spline), so it visibly facets. That is the point: it gives the smoother
# something to work on. Dial `SMOOTH_STRENGTH` from 0 (off — the raw polyline) to 1.
#
# The route highlight in `{svg}` is the same coarse polyline, so the drawn line facets
# exactly like the unsmoothed motion — at `SMOOTH_STRENGTH: 0` the marker tracks the drawn
# corner for corner, and as the strength rises you are watching the smoother pull the
# motion off the drawn line. That divergence IS the readout.

defs:
    assets:
        map:
            type: "scene"
            file: "./resources/diagram/map.svg"
        route_layer:
            type: "scene"
            file: "./resources/diagram/{svg}"
        # Declared last of the three scenes: declaration order is the render z-order,
        # so the markers paint over the route. Hand-authored and shared with
        # scene_summit.yaml — the generated overlay carries route geometry only.
        markers:
            type: "scene"
            file: "./resources/diagram/markers.svg"
'''

SCENE_CONSTS = '''
        dest_ring:
            type: "actor"
            part_of: markers
            id: dest-ring
            origin: center
        dest_star:
            type: "actor"
            part_of: markers
            id: dest-star
            origin: center
        traveller_solid:
            type: "actor"
            part_of: markers
            id: traveller-solid
            origin: center
        traveller_ghost:
            type: "actor"
            part_of: markers
            id: traveller-ghost
            origin: center

        template:
            type: "template"
            file: "./resources/template/main.html"
            style: style
        style:
            type: "style"
            file: "./resources/css/theme_dark.css"

    const:
        # The knob under test: 0 = off (the bare polyline), 1 = the method's maximum.
        SMOOTH_STRENGTH: {strength}
        FADE_WINDOW: {fade}
        VIDEO_MARGIN: 600
        GHOST_OPACITY: 0.55
        PULSE_CYCLES: 2
        # Star settle — shorter than one pulse cycle, so it is planted before the
        # ring's first beat rather than growing through it.
        STAR_ARRIVE_MS: 420
'''


def emit_scene(segments, svg_name: str, step: float, strength: float, out: str) -> None:
    """Write the companion waypoint-form scene — the only form `smoothing` accepts."""
    total = sum(polyline_length(pts) for _, pts in segments)
    millis = [max(1, round(polyline_length(pts) / total * TRAVEL_MS)) for _, pts in segments]
    fade = min(min(millis), 260)

    body = [SCENE_HEADER.format(svg=svg_name, step=step)]
    for i, _ in enumerate(segments, 1):
        body.append(
            f"\n        seg_{i}:\n"
            f'            type: "actor"\n'
            f"            part_of: route_layer\n"
            f"            id: route-seg-{i:02d}\n"
        )
    body.append(SCENE_CONSTS.format(strength=strength, fade=fade))

    for i, ms in enumerate(millis, 1):
        length = polyline_length(segments[i - 1][1])
        body.append(f"        LEG_{i}_MS: {ms}  # {length:6.1f} px  {segments[i - 1][0]}\n")

    body.append("\nanimation:\n    defaults:\n        assets:\n            scene: map\n")
    body.append("\n    timeline:\n        0 @ setup_ts:\n")
    body.append(
        "            - map:\n                  - show:\n                        opacity: 1\n"
        '                        hold:\n                            after: "VIDEO_MARGIN"\n'
    )
    for i in range(1, len(segments) + 1):
        body.append(f"            - seg_{i}:\n                  - show:\n                        opacity: 0\n")
    for name in ("dest_ring", "dest_star", "traveller_solid", "traveller_ghost"):
        body.append(f"            - {name}:\n                  - show:\n                        opacity: 0\n")

    for i, (kind, pts) in enumerate(segments, 1):
        rider = "traveller_solid" if kind == "visible" else "traveller_ghost"
        leaving = "traveller_ghost" if kind == "visible" else "traveller_solid"
        start = "setup_ts.end" if i == 1 else f"leg{i - 1}_ts.end"
        opacity = "1" if kind == "visible" else "GHOST_OPACITY"
        body.append(f"\n        # --- Leg {i} ({kind.upper()}) — {polyline_length(pts):.0f} px, "
                    f"{len(pts)} waypoints ---\n")
        body.append(f"        {start} @ leg{i}_ts:\n")
        if i > 1:
            body.append(f"            - {leaving}:\n                  - show:\n"
                        f"                        opacity: 0\n")
        body.append(f"            - seg_{i}:\n                  - show:\n"
                    f"                        duration: FADE_WINDOW\n"
                    f"                        opacity: 1\n")
        body.append(f"            - {rider}:\n                  - show:\n")
        if i == 1:
            body.append("                        duration: FADE_WINDOW\n")
        body.append(f"                        opacity: {opacity}\n")
        body.append(f"                  - move:\n"
                    f"                        duration: LEG_{i}_MS\n"
                    f"                        easing: linear\n"
                    f"                        orient: auto\n"
                    f"                        along:\n"
                    f"                            segments:\n")
        for x, y in pts:
            body.append(f"                                - x: {x:.1f}\n"
                        f"                                  y: {y:.1f}\n")
        body.append(f"                            smoothing:\n"
                    f'                                method: "catmull_rom"\n'
                    f"                                strength: SMOOTH_STRENGTH\n")

    body.append(
        f"\n        # --- Summit reached ---\n"
        f"        leg{len(segments)}_ts.end @ arrive_ts:\n"
        f"            - traveller_solid:\n                  - show:\n                        opacity: 0\n"
        f"            - dest_ring:\n                  - show:\n                        opacity: 1\n"
        f"                  - pulse:\n                        duration: 1100\n"
        f"                        cycles: PULSE_CYCLES\n"
        f"                        stroke: 'css(\"kg-arrive-stroke\")'\n"
        f"                        stroke_width: 'css(\"kg-pulse-stroke-width\")'\n"
        f"            - dest_star:\n                  - show:\n"
        f"                        duration: STAR_ARRIVE_MS\n                        opacity: 1\n"
        f"                        scale:\n                            from: 0.4\n"
        f"                            to: 1\n                        easing: ease_out_back\n"
        f"\n        arrive_ts.end @ tear_down_ts:\n"
        f"            - map:\n                  - show:\n                        opacity: 1\n"
        f'                        hold:\n                            after: "VIDEO_MARGIN"\n'
        f"\n    capture:\n        video_summit:\n"
        f'            output: "./video/scene_summit_faceted.mp4"\n            fps: 30\n'
    )
    with open(out, "w") as handle:
        handle.write("".join(body))
    print(f"{out} written — {sum(len(pts) for _, pts in segments)} waypoints, "
          f"smoothing strength {strength}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build one route's overlay SVG from the shared multi-route trace."
    )
    parser.add_argument("trace", nargs="?", help="override the painted trace this route is read from")
    parser.add_argument("--route", choices=sorted(ROUTES), default="summit",
                        help="which route to pull out of the trace (default summit)")
    parser.add_argument("--visible", help="override this route's VISIBLE brush colour (#rrggbb)")
    parser.add_argument("--hidden", help="override this route's HIDDEN brush colour (#rrggbb)")
    parser.add_argument("--tolerance", type=int,
                        help="RGB radius around each brush colour; 0 is an exact match, and a "
                             "lossy (JPEG) trace needs a radius to match at all")
    parser.add_argument("--start", choices=sorted(EXTREME),
                        help="which edge of the frame the trailhead end sits towards")
    parser.add_argument("-o", "--out", help="SVG to write (default: the route's own overlay)")
    parser.add_argument("--smooth", type=int, default=SMOOTH_PASSES,
                        help="1-2-1 passes before the spline; 0 tracks the trace most closely")
    parser.add_argument("--no-spline", dest="spline", action="store_false",
                        help="emit the bare waypoint polyline — angular corners, nothing rounded")
    parser.add_argument("--step", type=float, default=STEP,
                        help=f"resample step in px (default {STEP:g}); raise it to coarsen the polyline")
    parser.add_argument("--scene", metavar="FILE",
                        help="also write a waypoint-form companion scene (the `smoothing` test bed)")
    parser.add_argument("--strength", type=float, default=0.5,
                        help="SMOOTH_STRENGTH seeded into --scene (default 0.5)")
    args = parser.parse_args()

    route = ROUTES[args.route]
    if args.scene and args.route != "summit":
        # The companion scene is the `along.smoothing` test bed, written against the
        # summit's asset names throughout. Emitting it for another route would produce
        # a scene wired to ids that route does not have — fail here instead.
        raise SystemExit("--scene is summit-only (it is the smoothing test bed)")
    visible = args.visible or route.visible
    hidden = args.hidden or route.hidden
    start = args.start or route.start
    out_path = args.out or route.out
    tolerance = route.tolerance if args.tolerance is None else args.tolerance

    trace_png = args.trace or route.trace
    print(f"reading {trace_png}  [{args.route}: {route.title}]  "
          f"visible {visible}, hidden {hidden}, start {start}")
    print(f"  (smooth={args.smooth}, spline={'on' if args.spline else 'off'}, "
          f"step={args.step:g}px, tolerance={tolerance})")
    trace = read_trace(trace_png, visible, hidden, tolerance)
    blobs = components(trace)
    mask, joins = bridge(blobs, start)
    print(f"  {len(trace)} trace px in {len(blobs)} strokes; "
          f"bridged gaps: {', '.join(f'{d:.0f}px' for _, _, d in joins)}")

    raw = centreline(trace, mask, start)
    points = smooth([(x, y) for x, y, _ in raw], args.smooth)
    if args.spline:
        points = catmull_rom(points, CR_SAMPLES)
    curve = resample(points, args.step)
    segments = split(raw, curve)

    total = sum(polyline_length(pts) for _, pts in segments)
    print(f"  {len(segments)} segments, {total:.0f}px of route")

    width, height = Image.open(trace_png).size
    body = [HEADER.format(w=width, h=height, title=route.title, route=args.route,
                          svg_id=route.svg_id, vis=visible, hid=hidden,
                          line=route.line_colour)]
    print(f"\n  {'segment':<12} {'kind':<8} {'px':>7} {'ms':>6}   (at {TRAVEL_MS} ms end to end)")
    for i, (kind, pts) in enumerate(segments, 1):
        length = polyline_length(pts)
        millis = round(length / total * TRAVEL_MS)
        print(f"  {route.prefix}-seg-{i:02d}  {kind:<8} {length:7.1f} {millis:6d}")
        casing = "route-casing" if kind == "visible" else "hidden-casing"
        body.append(
            f'\n  <!-- {kind} stretch {i} of {len(segments)} — {length:.0f}px -->\n'
            f'  <g id="{route.prefix}-seg-{i:02d}" opacity="0">\n'
            f'    <path class="{casing}" d="{path_data(pts)}" />\n'
            f'    <path id="{route.prefix}-line-{i:02d}" class="route-{kind}" '
            f'd="{path_data(pts)}" />\n'
            f"  </g>\n"
        )

    # Route geometry only. The glyphs that ride and terminate it live in the
    # hand-authored markers.svg, stacked above this layer — so re-tracing can
    # never clobber them. Their resting poses are reported below; if a re-trace
    # moves the trailhead or the destination appreciably, nudge markers.svg to match.
    destination = segments[-1][1][-1]
    trailhead = segments[0][1][0]
    ghost_start = next((pts[0] for kind, pts in segments if kind == "hidden"), None)
    body.append("</svg>\n")

    # XML forbids a double hyphen inside a comment, and the header names flags. Catch
    # it here: otherwise the overlay is written happily and fails much later, at compile
    # time, as a parse error against a GENERATED file nobody is meant to hand-edit.
    banner = body[0].split("-->", 1)[0].removeprefix("<!--")
    if "--" in banner:
        raise SystemExit("the overlay header contains '--', which XML forbids in a comment")

    with open(out_path, "w") as handle:
        handle.write("".join(body))
    if args.scene:
        import os
        emit_scene(segments, os.path.basename(out_path), args.step, args.strength,
                   os.path.join("../..", args.scene))
    # The callout text is a literal in the scene file — a `type: text` asset holds it.
    # Printing it here is what keeps it honest: the distance and time are derived from
    # the trace just measured, so a re-trace surfaces the new figures to paste across.
    distance, clock = figures(route, total)
    print(f"\n  note text — {route.title} · {distance} · {clock}\n"
          f"      {route.title}\n"
          f"      {distance} · {route.ascent_m} m ascent\n"
          f"      ≈ {clock} · {route.grade}")

    ghost = f"({ghost_start[0]:.0f}, {ghost_start[1]:.0f})" if ghost_start else "none (no hidden stretch)"
    print(f"\n  markers.svg resting poses — trailhead ({trailhead[0]:.0f}, {trailhead[1]:.0f})"
          f"  ghost-start {ghost}"
          f"  destination ({destination[0]:.0f}, {destination[1]:.0f})")
    print(f"\n{out_path} regenerated — {len(segments)} stretches, {route.title} at "
          f"({destination[0]:.0f}, {destination[1]:.0f})")


if __name__ == "__main__":
    main()
