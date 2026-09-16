# Life Lessons (English) — Kinetic Typography

Two short quote cards. Each fades a styled quote in over a paper texture, paced to a
spoken narration of the same line. This is the smallest complete Kinaigraph example:
one visual idea, one audio track, and nothing else.

The Spanish edition, [`life-lessons-es`](../life-lessons-es/), is the same two scenes
with Spanish scripts, artwork and voice — a useful side-by-side if you want to see what
changes when a project is localized.

## The scenes

| Scene | File | The quote |
| ----- | ---- | --------- |
| 1 | `scene_01_gratitude_perspective.yaml` | *"Gratitude won't change your situation, but it will change your perspective."* |
| 2 | `scene_02_life_meaning.yaml` | *"The meaning of life isn't found in a destination, but in the path that leads there."* |

`scene_00_tts_generation.yaml` is synthesis-only: it turns the scripts under `resource/script/`
into the narration MP3s the scenes read. Run it once, and again whenever a script
changes.

## What it shows

- **Layering with a 1×1 grid.** Both the background and the foreground sit in the single
  cell `[0, 0]` and z-stack in **declaration order** — background first, so it sits
  behind; foreground second, so the quote sits in front. There is no explicit z-index to
  keep in sync.
- **Styling in CSS, position in SVG.** Font, size and fill live in
  `resource/style/theme_life_lessons.css`, attached to the foreground scene as a
  `type: style` asset. Where the text sits stays in the SVG. Restyling the quote is a
  stylesheet edit; nothing about the animation moves.
- **A baked paper texture.** The background is an embedded JPEG rather than the raw
  SVG texture. The JPEG pre-smooths the paper's high-frequency noise, which the H.264
  encoder would otherwise spend its bitrate on.
- **Timing read from the voice.** The fade is expressed against the narration clip's
  probed duration, so re-recording a line re-fits the scene on the next render.

## Layout

```text
scene_00_tts_generation.yaml      narration synthesis (run first)
scene_01_gratitude_perspective.yaml
scene_02_life_meaning.yaml
resource/script/                           the spoken lines, one .txt per scene
resource/
  style/theme_life_lessons.css    how the quote is styled
  scene/*.svg                     the quote artwork, one per scene
  image/*                         paper textures
```

## Rendering it

You need Kinaigraph installed — see the [install instructions](../../README.md#install).
Run from this directory:

```sh
kinaigraph scene_00_tts_generation.yaml --outdir ./out    # once, to synthesize narration
kinaigraph scene_01_gratitude_perspective.yaml --outdir ./out
kinaigraph scene_02_life_meaning.yaml --outdir ./out
```

Paths inside a scene resolve against the scene file's own folder — which is this
directory, since the YAML sits at the top — so `file:` values need no `../`. Outputs
resolve against whatever you pass as `--outdir`.

Synthesis calls a text-to-speech provider and needs `ELEVENLABS_API_KEY` in the
environment. It is a separate file from the scenes on purpose: re-rendering a scene must
never re-synthesize audio that did not change.
