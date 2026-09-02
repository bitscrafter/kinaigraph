# Bio Journey — a life told in three beats

A short narrated portrait: a title card, a career timeline, and a world map where two
planes leave the same city at once because the subject has not decided where she is
going next.

The piece is **P.15** in the showcase plan. Its headline capability is
narration-driven timing; the map is the closer, and it earns its seconds on a
capability the other examples do not show: **two riders sharing one origin**, both in
the air at the same time.

⚠️ Unlike the other showcase examples, this one carries **no on-screen capability
legend** — no `note` anywhere, by owner decision. The piece is a portrait, and a panel
of engine commentary in the corner reads as an intrusion on it. The consequence for the
plan is that P.15 no longer demonstrates `note`; that capability needs another host.

## Status

| Beat | Scene | Built | What it is |
| ---- | ----- | ----- | ---------- |
| 1 | `scene_01_intro.yaml` | ✅ | The title card. Four elements cascading in reading order. |
| 2 | `scene_02_timeline.yaml` | ✅ | The career timeline. Four stations, spaced by where the sentences land. |
| 3 | `scene_03_map.yaml` | ✅ | The flight map. Austin to Honolulu and Austin to Paris, concurrently. |
| — | `scene_stitch.yaml` | ✅ | All three rolled into one 30-second piece. |

`scene_00_tts_generation.yaml` is synthesis-only — it generates the narration MP3s
under `audio/` from the scripts under `script/`. `scene_stitch.yaml` chains the three
clips; it carries no mixes, because each beat already mixed its own narration and a
full `roll:` plays a clip whole.

The stitched piece is **30.2 seconds**, inside the locked 25–35s budget, from 70 words
of script. Rendered with real narration:

| Beat | Narration | Clip |
| ---- | --------- | ---- |
| 1 intro | 4.040s | 4.767s |
| 2 timeline | 15.000s | 15.733s |
| 3 map | 8.916s | 9.633s |
| **full** | | **30.167s** |

Every clip is its line plus 700 ms — a head margin of quiet before the first word and a
tail after the last. That is the invariant to check after any timing change: a clip
equal to `narration.duration` means the tail is being truncated, because the line starts
one margin in.

## ⚠️ This example is built for a named person first

It is a portrait of a real person, written as an example. **Two files hold every
personal detail, and nothing else refers to them:**

- `resources/foreground/intro_card.svg` — the name, the role, the two meta lines
- `script/beat_01_intro.txt` — the narration that says the name

To genericise it for publication, change those two and re-run `scene_00`. Everything
else in the piece is about cities and timing.

That is why the directory is **deliberately uncommitted** for now. Nothing under
`examples/` is published until it is added to git.

## How the capabilities show up

- **Two riders, one origin.** Both flights are chained off one bookmark as
  **separate timeline entries**, because actions inside a single entry sequence. That
  is what concurrency looks like structurally, and it is why the two planes can be
  over the Pacific and the Atlantic in the same frame.
- **Move along a computed path.** Neither arc is drawn by hand. Both are true great
  circles between city coordinates, sampled and projected by
  `resources/diagram/make_map_svg.py`. The arc you see and the arc a plane rides are
  one path, so a city cannot drift from its route.
- **Orientation from the tangent.** `orient: auto` turns each plane onto its heading.
  The glyph is authored pointing +x at rest — the engine's zero rotation — so there is
  no per-asset correction anywhere.
- **One pace, two durations.** Both flights divide the same `PACE_PX_PER_S`. Paris
  takes longer than Honolulu because its arc is longer, which is geometry rather than
  two authored numbers that have to keep agreeing.
- **Per-flight arrival.** Each ring pulses off its **own** flight's bookmark, not off
  a shared one, so Honolulu lands and finishes pulsing while Paris is still over
  Newfoundland.
- **Steps spaced by the script, not by equal division.** Beat 2's four stations hold
  22%, 13%, 30% and 35% of the line, because its sentences are 9, 5, 12 and 14 words
  long. Equal quarters is the obvious first move and it is wrong for any script with a
  lead-in, a quick middle and a closing clause.
- **Narration-driven timing.** Every beat's closing dwell is
  `narration.duration - <the rigid parts>`: the flights are rigid (distance over
  pace) and whatever the voice leaves over lands on the beat where someone is reading.
  All three beats currently land within one frame of their line. Re-record and
  re-render; the beat re-fits.

## Files

| Path | What |
| ---- | ---- |
| `resources/diagram/ne_110m_land.geojson` | Source land geometry. Natural Earth 1:110m, public domain. |
| `resources/diagram/make_map_svg.py` | Projects the land, computes both great circles, prints the city positions and arc lengths. |
| `resources/diagram/world_map.svg` | **Generated** backdrop — do not hand-edit. |
| `resources/diagram/flights_layer.svg` | **Generated** route overlay — do not hand-edit. |
| `resources/diagram/markers_flights.svg` | Hand-authored glyphs: city dots, labels, arrival rings, the two planes. |
| `resources/diagram/preview_map.py` | Dev aid. Renders a still composite of the three map layers without running the engine. |
| `resources/foreground/intro_card.svg` | The title card. **Holds personal details.** |
| `resources/foreground/timeline_card.svg` | The career timeline: axis segments, four stations, the dashed tail. |
| `resources/css/theme_bio.css` | Shared palette and typography for all beats. |
| `resources/template/main.html` | Shared HTML container. |
| `script/` | Source narration, one file per beat. |
| `audio/` | TTS narration (output of `scene_00`, not published). |

To re-frame the map or move a city: edit `LON_MIN`/`LAT_MAX` or the `CITIES` table in
`make_map_svg.py`, re-run it, then paste the printed city positions into
`markers_flights.svg` and the printed `FLIGHT_*_PX` figures into `scene_03_map.yaml`.
Those two paste-acrosses are required: a marker layer is hand-authored, and there is
no `.length` on a path for a scene to divide by.

## Rendering

```bash
# 1) Generate the map layers (only when the projection or a city changes).
./resources/diagram/make_map_svg.py

# 2) Generate the narration (only when a script changes). Needs ELEVENLABS_API_KEY.
#    Every run costs credits.
kinaigraph scene_00_tts_generation.yaml --outdir .

# 3) Render the three beats, then stitch. All four share ONE outdir: every capture
#    names a distinct file under out/video/, so nothing collides.
kinaigraph scene_01_intro.yaml    --outdir ./out
kinaigraph scene_02_timeline.yaml --outdir ./out
kinaigraph scene_03_map.yaml      --outdir ./out
kinaigraph scene_stitch.yaml      --outdir ./out    # -> out/video/bio_journey_full.mp4
```

The stitch must run last: it probes each clip's duration at compile time, so a missing
beat fails there rather than silently at playback.

Step 2 is not optional: each scene probes its line's `.duration` at compile time to
size itself, so a missing MP3 is a compile error rather than a silent clip.

The committed narration was generated from these scripts with the voice named in
`scene_00_tts_generation.yaml`. Beat 2's step fractions were then **measured** against
that take with `silencedetect` and confirmed to land within 53 ms — see that scene's
header before rewriting its script.

## The jet bed

Beat 3 has a sound-effect slot that is **wired but commented out**, in both the
`jet_bed` asset and its `mix` entry in `scene_03_map.yaml`. Uncomment both once the
file is in place at `resources/audio/`.

Source it from [Freesound](https://freesound.org/) filtered to **CC0** — a steady jet
or cabin ambience, not a doppler flyby. Two reasons for CC0 specifically: it is
redistributable, so unlike the Pixabay track in `hiking-trails` the file can be
committed and a clone reproduces the example without a manual download; and a bed
sits under a nine-second beat without fighting the narration, which owns it.

Verify the licence on the individual file at download time — Freesound mixes CC0,
CC-BY and CC-BY-NC.

## Credits

**Map geometry** — [Natural Earth](https://www.naturalearthdata.com/) 1:110m land,
public domain. No attribution is required; it is given because it costs nothing. The
land silhouette, graticule, routes and markers are all Kinaigraph-authored SVG derived
from it — there is no generated art in this example.

**Narration** — ElevenLabs TTS, generated from the scripts under `script/`.
