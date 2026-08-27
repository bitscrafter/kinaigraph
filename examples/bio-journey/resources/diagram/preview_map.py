#!/usr/bin/env python3
"""
Renders a STILL composite of the map layers, for checking geometry without running
the engine.

This is a development aid, not part of the pipeline. It exists because the three
map layers only ever appear together at render time: alone, each one is an
unstyled fragment, and the scene files set every actor to `opacity: 0` in their
setup entry. Checking that an arc actually terminates on its city dot should not
require a full render and a video scrub.

What it does: stacks world_map.svg + flights_layer.svg + markers_flights.svg in
declaration order, inlines the theme stylesheet, forces every actor visible, and
parks the two planes mid-route so their hue and heading can be seen.

Two deliberate cheats, both PREVIEW ONLY:

  * `var()` is resolved by hand. librsvg does not implement CSS custom properties,
    so a faithful inline render comes out unstyled black. The engine's browser
    renderer has no such limit -- do not "fix" the stylesheet to suit this script.
  * the parked plane transforms are injected here, never written to the layer.

Usage:
    ./preview_map.py [-o OUT.png] [-w WIDTH]
"""

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(HERE, os.pardir, "css", "theme_bio.css")
LAYERS = ("world_map.svg", "flights_layer.svg", "markers_flights.svg")

# Where to park each plane for the still, and its heading. Chosen to sit clear of
# the city markers so the glyph is judged on its own.
PARKED = {
    "plane-honolulu": "translate(400 395) rotate(188)",
    "plane-paris": "translate(1100 250) rotate(-24)",
}


def svg_inner(path):
    """The body of an SVG file, with its own root element stripped."""
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    s = re.sub(r"^.*?<svg[^>]*>", "", s, flags=re.S)
    return s.rsplit("</svg>", 1)[0]


def resolve_vars(css):
    """Substitute :root custom properties inline. See the docstring's caveat."""
    root = re.search(r":root\s*\{(.*?)\}", css, re.S)
    if not root:
        return css
    table = {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r"--([\w-]+)\s*:\s*([^;]+);", root.group(1))
    }
    # Repeat so a property defined in terms of another still resolves.
    for _ in range(4):
        css = re.sub(
            r"var\(--([\w-]+)\)", lambda m: table.get(m.group(1), "magenta"), css
        )
    return css


def park_planes(markup):
    """Give each plane a mid-route pose so the still shows hue and heading."""
    for actor, transform in PARKED.items():
        markup = re.sub(
            r'(id="%s"[^>]*?)transform="[^"]*"' % re.escape(actor),
            r'\1transform="%s"' % transform,
            markup,
            flags=re.S,
        )
    return markup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="/tmp/bio_map_preview.png")
    ap.add_argument("-w", "--width", type=int, default=1400)
    args = ap.parse_args()

    with open(CSS, encoding="utf-8") as fh:
        css = resolve_vars(fh.read())

    body = "".join(svg_inner(os.path.join(HERE, name)) for name in LAYERS)
    body = park_planes(body.replace('opacity="0"', 'opacity="1"'))

    svg = (
        '<svg width="1920" height="1080" viewBox="0 0 1920 1080" '
        'xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink">'
        # CDATA because the stylesheet is inlined into an XML document here; the
        # engine emits it into HTML, where the rules are laxer.
        "<style><![CDATA[%s]]></style>%s</svg>" % (css, body)
    )

    tmp_svg = args.out.rsplit(".", 1)[0] + ".svg"
    with open(tmp_svg, "w", encoding="utf-8") as fh:
        fh.write(svg)

    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(args.width), tmp_svg, "-o", args.out],
            check=True,
        )
    except FileNotFoundError:
        sys.exit("rsvg-convert not found (brew install librsvg)")

    print("wrote %s" % args.out)
    print("      %s" % tmp_svg)


if __name__ == "__main__":
    main()
