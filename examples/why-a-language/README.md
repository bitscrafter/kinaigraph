# Why a Language — the case, in four scenes

The pitch: why explainer videos are worth making, what making them costs today,
what a language does about that cost, and what it opens up. 1920x1080, and not
one second of either cut is a length anyone chose — every scene is as long as the
lines spoken over it.

**Two cuts of the same argument, from the same drawings.**

| cut | length | how the voice works |
| --- | --- | --- |
| **brief** | 1:39 | names a CATEGORY and lets the boxes enumerate it · theme `paper` |
| **full** | 2:52 | names every box out loud · theme `depth` |

⚡ **They differ in the narration and in the theme, and in nothing else.** Same
artwork, same timeline shapes — the brief's lines are shorter and its scene 2
splits the shared band into three category waves; the full names every box and
takes `depth` rather than `paper`.

⚡ **EACH CUT IS SELF-SUFFICIENT.** Every line it speaks lives in its own script
and audio folder; every scene it rolls is its own document; its synthesis
document lists everything it needs. Two lines are word-for-word identical across
the cuts and are stored twice anyway — **a cut you can read and rebuild without
cross-referencing the other one is worth the duplication.** Only the drawings,
the themes and the template are shared, because those are not narration.

## Running it

Pick a cut; the five documents are the same shape either way.

```sh
CUT=brief          # or: CUT=full

kinaigraph scene_00_tts_$CUT.yaml         # once — needs ELEVENLABS_API_KEY, costs credits
kinaigraph scene_01_premise_$CUT.yaml
kinaigraph scene_02_challenge_$CUT.yaml
kinaigraph scene_03_benefits_$CUT.yaml
kinaigraph scene_04_possibilities_$CUT.yaml
kinaigraph scene_05_stitch_$CUT.yaml
open ./why_a_language_$CUT.mp4
```

⛔ **One synthesis document per cut, and it re-records everything it lists.**
`synthesis.context.status` is section-wide — there is no way to regenerate one
line without regenerating its neighbours in the same document.

The narration has to exist before any scene will render: every phase derives its
length from a clip's probed `.duration`, so without the audio there is nothing
for the timeline to measure.

⛔ **Never sweep this folder with `for y in scene_*.yaml`.** That pulls in all
three `scene_00` documents and re-records everything — it bills credits, and
every new length silently moves the timings the scenes measured against the
committed take. Use `ls scene_*.yaml | grep -v scene_00`.

| File | What it is |
| ---- | ---------- |
| `scene_00_tts_<cut>.yaml` | Synthesis. Every line that cut speaks. |
| `scene_0N_*_<cut>.yaml` | That cut's four scenes. |
| `scene_05_stitch_<cut>.yaml` | That cut in order. The only documents that write beside the document. |
| `resource/script/<cut>/` · `resource/audio/<cut>/` | That cut's lines and recordings. Nothing is shared. |
| `resource/scene/scene_0N_*.svg` | The artwork, shared by both cuts. Scenes 2 and 3 are **generated** — see *Editing it*. |
| `resource/style/theme_*.css` | Four themes — `paper` (the brief's), `depth` (the full's), `light`, `dark`. Values only, and all four declare an identical set of names. |
| `resource/scene/scene_00_cover.svg` | The wordmark. The first and last frame of both cuts, and nothing else. |
| `resource/scene/brand_layer.svg` | The brand mark, embedded as data. **Generated** — see *Editing it*. |
| `resource/image/bitscrafter_logo.png` | Source of truth for the mark. |
| `resource/video/` | Intermediates. Gitignored. |

## What this example is a good place to notice

**The brief cut names categories; the full cut names boxes.** Narration that
reads the screen aloud competes with the reader, who is faster — so the brief
says *"none of it is software"* and lets two boxes arrive saying which two. Scene
2's shared band comes in as three waves, one per category, and the difference in
runtime is 89 seconds.

Two rules make that work, and the compiler enforces the first:

- **The categories are a partition** — every box in exactly one. Two categories
  sharing a box and both writing its opacity over one window is rejected, naming
  the actor and both windows (§6.7.2).
- **No category spans both rows.** The band's rows are offset 200 under 320-wide
  boxes, so every adjacent row-A/row-B pair overlaps by 120 px — and two boxes
  that overlap *and travel together* cross each other on the way in. The box order
  in the generator is what keeps each wave inside one row.

**One clip per category, never fractions of one clip.** Each wave takes its length
from its own line, so re-recording one sentence moves one wave. Splitting a single
clip by thirds would tie the picture to where the sentences happen to fall in one
take — the trap `request-response` records against its six legs.

**It narrates per SCENE, not per clip — and that is the one place it parts company
with `request-response`.** There, each beat carries exactly one line, so a beat
can size ITSELF to its line and the stitch mixes at offset zero with no authored
offsets anywhere. Here every scene but the first carries several lines against
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

**Every duration in the four scenes is either a pad or a line.** Search them for
a number and you will find beat pads and fade lengths under a second — nothing
that paces a section.

⛔ **AND NO SCENE ENDS ON A HELD BLANK FRAME.** Every scene used to close on one
and the next opened on another; measured, the three cuts between scenes carried
1.7 s, 1.1 s and 2.8 s of nothing, and the brief spent 7.7 s on blank frames
altogether. The fades stay — cutting hard between them is jarring — but the held
frames after them are gone, which took the blank down to 3.7 s. Re-record one line and exactly one section
of one scene moves; everything after it slides by itself, because the stitch
chains by bookmark rather than by number.

**A scene opens on its own.** Each `<style>` block holds the MAPPING — which class
takes which property from which variable — while the two stylesheets hold the
VALUES. Every `var()` carries `theme_paper.css`'s value as its fallback, so
opening a scene SVG in a browser, an editor or a GitHub preview shows paper
rather than unstyled shapes; whenever a stylesheet is in scope, it wins.

⚠️ **THE DRAWINGS ARE SHARED BY BOTH CUTS AND THE CUTS SELECT DIFFERENT THEMES**,
so a fallback can only mirror ONE of them. It mirrors the brief's, because the
brief is the deliverable. That costs nothing at render time — a fallback is only
reached when NO stylesheet is in scope, and one always is — it decides only what
a scene file looks like opened on its own. Verified rather than assumed: the same
scene rendered under `dark` before and after repointing the fallbacks is
pixel-identical.

All four themes declare an identical set of names, and every name is read by at
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

**The brand mark is generated too.** `resource/scene/brand_layer.svg` embeds the
PNG as base64, because a scene SVG is inlined into the compiled page and a
relative `href` would resolve against wherever that page lands:

```sh
python3 resource/temp/make_brand_svg.py
```

⚠️ **The mark sits bottom CENTRE here, where every other example puts it bottom
right.** Measured against every drawn element, the bottom-right slot collides in
three of the four scenes — an icon in scene 1, the `Renders Locally` box in scene
3, and scene 4's bullseye ring. Bottom centre is clear of all of them.

⚠️ **One asset serves every theme.** The logo is light-on-transparent, drawn for
a dark canvas, so the light themes invert it (`--brand-mark-filter: invert(1)`)
rather than shipping a second file — the same treatment the architecture video
uses.

**Scenes 2 and 3 are generated; do not hand-edit them.** Both are regular grids,
and hand-editing a coordinate in a grid is how a grid stops being one. The box
tables, the geometry and the class-to-variable mapping all live in one script:

```sh
python3 resource/temp/make_scenes.py   # rewrites scene_02_challenge.svg AND scene_03_benefits.svg
```

It mirrors its icons from the shared catalog in the engine repo
(`tech-docs/internal/design/diagram/icon-catalog.svg`) — an icon edit belongs
upstream first — and it reads `theme_paper.css` to emit each `var()`'s fallback, so
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
regenerates every line that document lists and bills for all of them, even if you
edited one. That is why there are three of them rather than one.

`resource/temp/` is not published. It holds authoring scratch.
