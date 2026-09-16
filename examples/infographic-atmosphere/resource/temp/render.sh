#!/usr/bin/env bash
# Rasterise a poster SVG to PNG at a device scale factor.
#   ./render.sh atmosphere.svg 1100 2600 2
set -euo pipefail
SVG="$1"; W="$2"; H="$3"; SCALE="${4:-2}"
CHROME="${KINAIGRAPH_BROWSER:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
OUT="${SVG%.svg}.png"
PAGE="$(mktemp -t poster).html"
cat > "$PAGE" <<HTML
<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#000}
svg{display:block}
</style></head><body>
$(sed -e 's/<?xml[^>]*?>//' "$SVG")
</body></html>
HTML
"$CHROME" --headless --disable-gpu --hide-scrollbars \
          --force-device-scale-factor="$SCALE" \
          --screenshot="$OUT" --window-size="$W,$H" \
          --allow-file-access-from-files "$PAGE" >/dev/null 2>&1
rm -f "$PAGE"
echo "$OUT  ($(sips -g pixelWidth -g pixelHeight "$OUT" 2>/dev/null | awk '/pixel/{printf "%s ", $2}'))"
