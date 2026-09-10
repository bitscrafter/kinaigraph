# Documentation videos

The narrated videos that explain Kinaigraph are themselves made with Kinaigraph. This folder
holds their **sources** — the same YAML, SVG, scripts and audio a reader would write, kept here
so anyone can open one up and see how a finished piece is put together.

This is **technical documentation about Kinaigraph**, not a tutorial and not an example gallery.
The pieces under [`../../examples/`](../../examples/) exist to be learned from; these exist to
explain the system, and happen to be readable for the same reason.

## What is here

```text
docs/video/src/<topic>/<name>/
├── <name>_full.yaml          the complete piece
├── <name>_brief.yaml         a shorter cut of the same material
├── <name>_teaser.yaml        ~30 seconds
└── resource/
    ├── scene/                the SVG artwork the animation drives
    ├── style/                the stylesheet, one class per theme
    ├── template/             the page the scene is composed into
    ├── image/                logos and raster art
    ├── script/{full,brief,teaser}/   narration, one file per part
    └── audio/{full,brief,teaser}/    the recorded narration
```

Each `resource/` subfolder is named for the **asset type** the language declares — `scene`,
`style`, `template`, `image` — so what a folder holds and what a document calls it are the same
word.

| topic | piece | what it covers |
| --- | --- | --- |
| `architecture` | `structural_layers` | the ports, adapters, subsystems and layers the engine is built from |

## Rendering one

**No API key is needed.** The narration audio is committed here, so a clone can render these
without paying a text-to-speech provider for recordings that already exist. That is the one way
these differ from the examples, where narration is generated and ignored.

```sh
cd docs/video/src/architecture/structural_layers
kinaigraph structural_layers_full.yaml
open ./structural_layers_full.mp4
```

Outputs land beside the document. Rendering the full piece takes a few minutes — it drives a
real browser frame by frame and then encodes what it captured. The `_brief` and `_teaser`
documents are the same diagram and the same theme, told shorter:

```sh
kinaigraph structural_layers_teaser.yaml   # ~30s, quickest to try
kinaigraph structural_layers_brief.yaml
```

### Changing the narration

Editing a `resource/script/**/part_*.txt` file does **not** change the video on its own — the
committed mp3 beside it is what gets mixed. To re-record, set `ELEVENLABS_API_KEY` and flip that
document's `synthesis.context.status` from `complete` to `active`:

```yaml
synthesis:
  context:
    status: active # was: complete
```

⚠️ **`status` applies to the whole section**, so this re-synthesises *every* part in the
document and bills for all of them, not just the one you edited.

## Installing Kinaigraph, and everything else

This page assumes you already have the `kinaigraph` binary on your `PATH`. The
[repository README](../../README.md) is the full version — what Kinaigraph needs, how to install
it, what to do if macOS refuses to run the download, and the complete
[command-line reference](../../README.md#command-line-reference).
