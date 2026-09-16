# Life Lessons — Kinetic Typography, in Two Languages

Two short quote cards. Each fades a styled quote in over a paper texture, paced to a
spoken narration of the same line. It is the smallest complete Kinaigraph example: one
visual idea, one audio track, and nothing else.

Both scenes ship in **English and Spanish**, which is the second thing this example is
for — a localisation you can read as a directory rather than take on trust.

```sh
kinaigraph scene_01_gratitude_perspective_en.yaml
kinaigraph scene_01_gratitude_perspective_es.yaml
```

The recordings are committed, so a clone renders every scene with no key.

## The scenes

| Scene | Documents | The quote |
| ----- | --------- | --------- |
| 1 | `scene_01_gratitude_perspective_{en,es}.yaml` | *"Gratitude won't change your situation, but it will change your perspective."* |
| 2 | `scene_02_life_meaning_{en,es}.yaml` | *"The meaning of life isn't found in a destination, but in the path that leads there."* |

`scene_00_tts_{en,es}.yaml` are synthesis-only: each turns that language's scripts into
its narration MP3s. Run one when you change a script in that language — never both.

## A language is a dimension, like a cut

The suffix on a document names the language, and every resource kind that varies by
language has a subfolder for it. Everything that does not vary sits at the top of its
kind and is shared by both:

```text
life-lessons/
├── scene_00_tts_en.yaml                     scene_00_tts_es.yaml
├── scene_01_gratitude_perspective_en.yaml   …_es.yaml
├── scene_02_life_meaning_en.yaml            …_es.yaml
└── resource/
    ├── scene/
    │   ├── paper_background_medium.svg      shared — the paper both languages sit on
    │   ├── en/scene_0*.svg                  the quote, set in English
    │   └── es/scene_0*.svg                  the quote, set in Spanish
    ├── script/{en,es}/part_0*.txt
    ├── audio/{en,es}/part_0*.mp3
    ├── image/paper_texture_rough_01.{jpg,svg}   shared — the baked paper and its source
    └── style/theme_life_lessons.css         shared
```

⚡ **What localising actually costs is now countable.** A third language is two SVGs, two
scripts, two recordings and three documents copied with their paths changed — and
**nothing else**: not the paper, not the stylesheet, not a line of timeline. The shared
files outnumber the per-language ones.

⚠️ **The words live in the artwork, not in a `text` asset**, because these quotes are set
rather than typed — the line breaks and the centring are the design. That is what makes a
language a pair of SVGs instead of a string swap, and it is the honest cost of setting
type as artwork.

## What it shows

- **Layering with a 1×1 grid.** Both the background and the foreground sit in the single
  cell `[0, 0]` and z-stack in **declaration order** — background first, so it sits
  behind; foreground second, so the quote sits in front. There is no explicit z-index to
  keep in sync.
- **Styling in CSS, position in SVG.** Font, size and fill live in
  `resource/style/theme_life_lessons.css`, attached to the foreground scene as a
  `type: style` asset. Where the text sits stays in the SVG. Restyling the quote is a
  stylesheet edit; nothing about the animation moves — and both languages restyle at once,
  because they share the file.
- **A baked paper texture.** The background is an embedded JPEG rather than the raw
  SVG texture. The JPEG pre-smooths the paper's high-frequency noise, which the H.264
  encoder would otherwise spend its bitrate on.
- **Timing read from the voice.** The fade is expressed against the narration clip's
  probed duration, so re-recording a line re-fits the scene on the next render. The two
  languages differ in length for the same quote — 5.40 s against 3.83 s for the first —
  and neither document carries a number that had to change for that.

## Rendering it

You need Kinaigraph installed — see the [install instructions](../../README.md#install).
Run from this directory:

```sh
kinaigraph scene_01_gratitude_perspective_en.yaml
kinaigraph scene_02_life_meaning_en.yaml
kinaigraph scene_01_gratitude_perspective_es.yaml
kinaigraph scene_02_life_meaning_es.yaml
```

Paths inside a scene resolve against the scene file's own folder — which is this
directory, since the YAML sits at the top — so `file:` values need no `../`. The
deliverable lands beside the document; the silent intermediate goes to `resource/video/`.

Re-recording needs `ELEVENLABS_API_KEY`, and synthesis is a separate document on purpose:
re-rendering a scene must never re-synthesise audio that did not change.
