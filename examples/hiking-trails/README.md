# Hiking Trails — Capabilities Showcase

Three walking routes drawn across one cartoon map. A marker travels each trail, ducks
behind the scenery where the trail does, and arrives at a callout that names where it
got to. The three clips stitch into a single narrated piece.

The point of the example is that **none of the route geometry is authored**. Each route
was painted once, by hand, over a copy of the map in two flat colours — one for the
stretches where the walker can be seen, one for the stretches that ride behind
something. A generator turns that painting into overlay geometry, and the scene file
rides it. Re-paint a trail and re-run; the drawn line, the travelled line and the
figures in the callout all move together, because they all come from the same trace.

## The three routes

| Route | Scene | Stretches | Beat |
| ----- | ----- | --------- | ---- |
| Summit Peak | `scene_summit.yaml` | 9 (alternating) | The long climb. The marker turns onto the curve as it walks, and hands off between a solid arrowhead and an outline ghost nine times as the pines hide it. |
| Serenity Lake | `scene_lake.yaml` | 1 (all visible) | The open walk. Traced entirely in the visible brush, so there is no ghost at all — the difference from the summit is the painting, not the code. |
| Viewpoint Rest Stop | `scene_rest.yaml` | 7 (alternating) | The pull past the stone cabin, whose roof hides the longest stretch of the three. Ends on a callout anchored to the marker rather than to a coordinate. |

`scene_00_tts_generation.yaml` is synthesis-only — it generates the narration MP3s under
`audio/` from the scripts under `script/`. `scene_stitch.yaml` concatenates the three
clips into the headline deliverable.

Each route scene sizes **itself** to its narration: it declares the line as an audio
asset purely to probe its duration, and derives the callout's dwell from it. The audio
is not played there — all three lines and the ambience bed mix once, in the stitch.

## How the capabilities show up

- **Move along a named path.** Each leg's `move … along` rides the stretch's own
  `<path>` by name, so the route the eye follows and the route the marker travels are
  one curve. No waypoints are copied into the scene file where they could drift.
- **Orientation from the tangent.** `orient: auto` turns the marker onto its direction
  of travel. The glyphs are authored pointing +x at rest — the engine's zero rotation —
  so no per-asset correction is needed anywhere.
- **Cross-scene riders.** The travelling markers live in a marker layer but ride curves
  that live in the route overlay; move-along resolves an asset segment across scenes
  within a frame, so a rider and its rail need not share a file.
- **Anchored callouts.** Each route ends with a `note` whose pointer targets the
  destination ring by asset, not by coordinate. Move the destination and the leader
  follows it.
- **One pace, derived per leg.** Every leg's duration is `LEG_n_PX / PACE_PX_PER_S`,
  and all three scenes carry the same pace. The marker cannot change speed at a handoff
  because each leg divides the same constant — a property of the structure, not of a
  duration table that has to keep agreeing with itself.
- **Narration-driven timing.** A scene's callout dwell is
  `narration.duration - WALK_MS - FIXED_MS`: the walk is rigid (distance over pace) and
  whatever the voice leaves over lands on the beat where someone is reading. Re-record
  a line, re-render, and the clip re-fits — the figure is probed, never pasted. Each
  clip lands within one frame of its line.
- **Self-adjusting composition.** The stitch chains clips by bookmark `.end` and slices
  the ambience bed by expressions over their probed durations, so re-rendering one
  route shifts everything after it with no edit.
- **Per-route palette.** Each route is one hue at three lightnesses — the drawn line,
  a stronger tone for the ring, star and markers, and a darker one for the callout
  text. Lightness is not free: a route has to sit darker than whatever it crosses,
  which is why the gold route is pushed darker than the blue one (the map's own trails
  are already sandy gold).

## Files

| Path | What |
| ---- | ---- |
| `resources/diagram/hiking.png` | The source map artwork. |
| `resources/diagram/map.svg` | The backdrop layer — the map base64-embedded as a JPEG data URI. Rebuild with `make_map_svg.sh`. |
| `resources/diagram/hiking_trace*.png` / `*.jpeg` | The owner-authored paintings each route is extracted from. Every trace an example depends on lives here, beside the generator. |
| `resources/diagram/make_route_svg.py` | Turns a trace into a route overlay. One entry per route in its `ROUTES` table. |
| `resources/diagram/route_layer*.svg` | **Generated** route overlays — do not hand-edit; the next run overwrites them. Colour lives in the generator's `line_colour`. |
| `resources/diagram/markers*.svg` | Hand-authored glyph layers (one per route): the travelling arrowheads, the destination ring and star. |
| `resources/template/main.html`, `resources/css/theme_dark.css` | Shared container and theme. |
| `script/` | Source narration text, one file per route. |
| `audio/` | TTS-generated narration (output of `scene_00`, not published). |

## Rendering

```bash
# 1) Generate the narration once (only when a script changes). Needs ELEVENLABS_API_KEY.
#    Nothing consumes these MP3s yet — see the note above.
kinaigraph scene_00_tts_generation.yaml -outdir .

# 2) Render each route.
kinaigraph scene_summit.yaml -outdir ./out
kinaigraph scene_lake.yaml   -outdir ./out_lake
kinaigraph scene_rest.yaml   -outdir ./out_rest

# 3) Stitch the three into the final video.
kinaigraph scene_stitch.yaml -outdir ./out_full
```

To re-route a trail: repaint its trace, run
`./make_route_svg.py --route <name>` from `resources/diagram/`, and paste the per-leg
durations it prints into that scene's `LEG_n_MS` consts.

## Credits

**Map artwork** — generated with Google Gemini. The route overlays, marker glyphs and
callouts on top of it are Kinaigraph-authored SVG; the backdrop is the only generated
art in the example.

**Ambient audio** — "Birds Forest Nature" by *soundreality* on
[Pixabay](https://pixabay.com/), asset `445379`, under the
[Pixabay Content License](https://pixabay.com/service/license-summary/).

The audio file is **not committed**. The licence permits free use, modification and
commercial use without attribution, but forbids distributing the content "on a
Standalone basis … where no creative effort has been applied to the Content and it
remains in substantially the same form" — which is what shipping the raw MP3 in a
public repository would be. Download it from Pixabay and place it at
`resources/audio/soundreality-birds-forest-nature-445379.mp3`, keeping the filename so
the source stays traceable. Credit is not required by the licence; it is given here
because it costs nothing and the community asks for it.
