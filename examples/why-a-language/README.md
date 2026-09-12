# Why a Language — the case, in four scenes

The pitch: why explainer videos are worth making, what making them costs today,
what a language does about that cost, and what it opens up. Just under four
minutes, 1920x1080, and not one second of it is a length anyone chose — every
scene is as long as the lines spoken over it.

This is the FULL cut. A shorter one may follow; it would be a second deliverable
rather than a replacement.

## Running it

```sh
kinaigraph scene_00_tts_generation.yaml   # once — needs ELEVENLABS_API_KEY, costs credits
kinaigraph scene_01_premise.yaml
kinaigraph scene_02_challenge.yaml
kinaigraph scene_03_benefits.yaml
kinaigraph scene_04_possibilities.yaml
kinaigraph scene_05_stitch.yaml
open ./why_a_language.mp4
```

The narration has to exist before any scene will render: every phase derives its
length from a clip's probed `.duration`, so without the audio there is nothing
for the timeline to measure.

⛔ **Never sweep this folder with `for y in scene_*.yaml`.** That pulls in
`scene_00`, which re-records all thirteen lines — it bills credits, and every new
length silently moves the timings the four scenes measured against the committed
take. Use `ls scene_*.yaml | grep -v scene_00`.

| File | What it is |
| ---- | ---------- |
| `scene_00_tts_generation.yaml` | Synthesis only. Turns thirteen scripts into thirteen clips. |
| `scene_01_premise.yaml` … `scene_04_possibilities.yaml` | The four scenes. Each is an animation plus the composition that mixes its own lines onto it. |
| `scene_05_stitch.yaml` | The four in order. The only document that writes beside the document. |
| `resource/scene/scene_0N_*.svg` | The artwork, one file per scene. Scenes 2 and 3 are **generated** — see *Editing it*. |
| `resource/style/theme_dark.css` · `theme_light.css` | The palette and type. Values only. |
| `resource/script/scene_NN_MM_*.txt` | The narration, one file per line. |
| `resource/audio/scene_NN_MM_*.mp3` | The recordings, once generated. |
| `resource/video/` | Intermediates. Each scene writes a silent capture and a narrated one here; gitignored. |

## What this example is a good place to notice

**It narrates per SCENE, not per clip — and that is the one place it parts company
with `request-response`.** There, each beat carries exactly one line, so a beat
can size ITSELF to its line and the stitch mixes at offset zero with no authored
offsets anywhere. Here scenes 2, 3 and 4 carry three, four and five lines against
sections of one picture: a line belongs to a *moment inside* its scene, not to the
whole of it. So each scene keeps its own `composition`, and each mix rides a
`span.from: "animation::<bookmark>.start"` — the bookmark of the moment it
describes, resolved in the document that owns it. `milestone-ladder` has the same
shape for the same reason.

Which idiom applies is decided by one question: does this clip have exactly one
thing to say? The stitch is still offset-free either way.

**Every challenge on screen has an answer on screen.** That is the only rule
governing what earns a box in scenes 2 and 3, and it is worth checking rather than
taking on trust: syncing is answered by Narration-Paced, usage costs by Renders
Locally, styling drift by Consistent Styling, re-authoring per language by
Localization, and a binary output by AI-Authorable. The pairing is what stops the
two scenes drifting into unrelated lists — add a pain without an answer and the
argument has a hole in it; add an answer to a pain nobody named and it reads as a
feature nobody asked for.

**Nothing in scene 2 is positioned by this repository.** The ten pain-point boxes
are drawn where they belong in the SVG. The document pushes each one off its mark
at t=0 with an instant `move`, then hands it back with `restore` — no checkpoint,
which targets the drawing's own initial values. Move a box in the artwork and the
slide follows it; there is no coordinate here to forget to update. The three
sections leave from three different edges, and that is an argument rather than
variety: the two columns being compared enter from opposite sides, and the row
they share enters from underneath both.

**Every duration in the four scenes is either a margin or a line.** Search them
for a number and you will find video margins, beat pads, and fade lengths under a
second — nothing that paces a section. Re-record one line and exactly one section
of one scene moves; everything after it slides by itself, because the stitch
chains by bookmark rather than by number.

**A scene opens on its own.** Each `<style>` block holds the MAPPING — which class
takes which property from which variable — while the two stylesheets hold the
VALUES. Every `var()` carries `theme_dark.css`'s value as its fallback, so opening
a scene SVG in a browser, an editor or a GitHub preview shows the dark theme
rather than unstyled shapes; whenever a stylesheet is in scope, it wins.

The two themes declare an identical set of names, and every name is read by at
least one scene. Swapping them is a one-line edit to each document's `style`
asset.

**The scenes used to carry their own palettes, and could not.** All four held four
copies of the whole palette — two `@media (prefers-color-scheme)` tiers plus
`html.dark-mode` / `html.light-mode` overrides. A variable defined only under a
media query has no determinable cascade at compile time, so `css()` reading one
fails outright. The copies had also drifted: scene 1 alone gave its secondary text a
different value from the one scenes 3 and 4 agreed on, in both palettes.

**Arial only, deliberately.** Nothing may name a font that is not installed by
default on Windows, macOS and Linux — an example that renders differently
depending on who clones it is a broken example. Liberation Sans, the Linux
default, is metric-compatible with Arial, so a fallback shifts no layout. The
artwork asked for `'Segoe UI'` first, which is a Windows font: everywhere else it
resolved to something with different advance widths and every heading came out a
different size. The two mathematical `ƒ` glyphs inside the icons keep a serif
face, spelled out the same way — Times New Roman with Liberation Serif behind it.

## Editing it

**Scenes 2 and 3 are generated; do not hand-edit them.** Both are regular grids,
and hand-editing a coordinate in a grid is how a grid stops being one. The box
tables, the geometry and the class-to-variable mapping all live in one script:

```sh
python3 resource/temp/make_scenes.py   # rewrites scene_02_challenge.svg AND scene_03_benefits.svg
```

It mirrors its icons from the shared catalog in the engine repo
(`tech-docs/internal/design/diagram/icon-catalog.svg`) — an icon edit belongs
upstream first — and it reads `theme_dark.css` to emit each `var()`'s fallback, so
the fallbacks cannot drift from the theme. It also emits **only** the icon classes
its own glyphs carry, so a scene never defines a rule nothing in it reads.

**SVG ids use underscores, and so does everything that names them.** Asset names,
group names, bookmark labels and timeline keys must match
`^[a-zA-Z_][a-zA-Z0-9_]*$`; ids may legally carry hyphens, but these files
converted theirs so the timeline can reference an element by its bare id and avoid
a bridging actor declaration per element.

⚠️ **A renamed id can break a stylesheet silently.** Scene 1's four theme blocks
selected its root by id, that id was rewritten underneath them, and every one of
them stopped matching — with no `var()` fallbacks behind them, the scene rendered
with no fill at all and no error. The fallbacks are what turn that class
of mistake into something you can see.

⚠️ **Two writers cannot both dictate one property at overlapping times.** The
precursor dimmed the last topic ring and faded it out from the same instant —
`1.0 -> 0.5` and `0.5 -> 0` over one window. That is rejected now, and it was
never coherent. Scene 4 drops the dim and ends on `opacity: 0` with no `from`,
which runs each ring from wherever it actually is: the last one from full, the
other three from half.

⚠️ **`synthesis.context.status` is section-wide.** Re-running the TTS document
regenerates all thirteen clips and bills for all thirteen, even if you edited one
line.

`resource/temp/` is not published. It holds authoring scratch.
