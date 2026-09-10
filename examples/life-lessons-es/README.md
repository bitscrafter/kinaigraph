# Life Lessons (Spanish) — Kinetic Typography

Two short quote cards, in Spanish. Each fades a styled quote in over a paper texture,
paced to a spoken narration of the same line.

This is the localized twin of [`life-lessons-en`](../life-lessons-en/): the same two
scenes, the same layering and styling, with Spanish scripts, artwork and voice. Reading
the two side by side shows what a localization actually costs in Kinaigraph — the
scripts, the foreground SVGs that carry the words, and the voice; not the timing, which
is derived, and not the layout.

## The scenes

| Scene | File | The quote |
| ----- | ---- | --------- |
| 1 | `scene_01_gratitude_perspective.yaml` | *"La gratitud no cambia tu situación, pero sí tu perspectiva."* |
| 2 | `scene_02_life_meaning.yaml` | *"El sentido de la vida no se encuentra en un destino, sino en el camino que lleva a él."* |

`scene_00_tts_generation.yaml` is synthesis-only: it turns the scripts under `resource/script/`
into the narration MP3s the scenes read. Run it once, and again whenever a script
changes.

## What it shows

- **Layering with a 1×1 grid.** Both the background and the foreground sit in the single
  cell `[0, 0]` and z-stack in **declaration order** — background first, so it sits
  behind; foreground second, so the quote sits in front.
- **Styling in CSS, position in SVG.** Font, size and fill live in
  `resource/style/theme_life_lessons.css`, attached to the foreground scene as a
  `type: style` asset. Where the text sits stays in the SVG.
- **A baked paper texture.** The background is an embedded JPEG rather than the raw SVG
  texture, which pre-smooths noise the H.264 encoder would otherwise spend bitrate on.
- **Timing read from the voice.** The fade is expressed against the narration clip's
  probed duration — and this is what makes localization cheap. A Spanish line is not the
  same length as its English original, and nothing had to be re-timed by hand for that.

## Layout

```text
scene_00_tts_generation.yaml      narration synthesis (run first)
scene_01_gratitude_perspective.yaml
scene_02_life_meaning.yaml
resource/script/                           the spoken lines, one .txt per scene
resource/
  css/theme_life_lessons.css      how the quote is styled
  foreground/*.svg                the quote artwork, one per scene
  backgrounds/*                   paper textures
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
never re-synthesize audio that did not change. The voice identifiers used are listed in
`resource/temp/elevenlabs_voices.txt`.
