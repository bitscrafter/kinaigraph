#!/usr/bin/env bash
# Regenerate map.svg by base64-embedding the cartoon map as a data: URI.
#
# Two hard-won choices:
#   * INLINE, not linked. A linked <image href> renders blurry in the headless
#     pipeline; inlining the pixels is the reliable path.
#   * JPEG, not PNG. The backdrop is re-rasterised every frame; a 4MB PNG base64
#     (~5.6MB of text) is a memory/CPU hog that can freeze the render and truncate
#     the output. A quality-90 JPEG of the same 1920x1080 cartoon is ~0.8MB and
#     visually identical, ~5x lighter to render.
# Re-run whenever hiking.png changes.
#   usage: ./make_map_svg.sh   (run from resources/diagram/)
set -euo pipefail
PNG="hiking.png"
QUALITY="${QUALITY:-90}"
W=$(sips -g pixelWidth  "$PNG" | awk '/pixelWidth/{print $2}')
H=$(sips -g pixelHeight "$PNG" | awk '/pixelHeight/{print $2}')
JPG="$(mktemp -t mapjpg).jpg"
magick "$PNG" -background white -flatten -quality "$QUALITY" "$JPG"
B64=$(base64 -i "$JPG")
rm -f "$JPG"
{
  printf '%s\n' '<!--'
  printf '%s\n' '  Backdrop layer for the hiking-trails showcase: the cartoon nature map.'
  printf '%s\n' '  Base64-embedded as a JPEG data: URI — inlined (a linked href renders blurry'
  printf '%s\n' '  in the headless pipeline) and JPEG-compressed (a PNG base64 is ~5x heavier and'
  printf '%s\n' '  can freeze/truncate the per-frame render). viewBox matches the pixel size, so'
  printf '%s\n' '  overlay-layer actors (routes, markers) address the same coordinate space.'
  printf '%s\n' '  Regenerate with ./make_map_svg.sh after replacing hiking.png (QUALITY env tunes it).'
  printf '%s\n' '-->'
  printf '<svg id="map" width="%s" height="%s" viewBox="0 0 %s %s"\n' "$W" "$H" "$W" "$H"
  printf '%s\n' '     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
  printf '  <image id="map-photo" x="0" y="0" width="%s" height="%s" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,' "$W" "$H"
  printf '%s' "$B64"
  printf '%s\n' '" />'
  printf '%s\n' '</svg>'
} > map.svg
echo "map.svg regenerated from ${PNG} (${W}x${H}) jpeg q${QUALITY}, $(du -h map.svg | cut -f1)"
