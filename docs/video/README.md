# Documentation videos

The narrated videos that explain Kinaigraph are themselves made with Kinaigraph. This folder
holds their **sources** — the same YAML, SVG, scripts and audio a reader would write, kept here
so anyone can open one up and see how a finished piece is put together.

These are **videos about Kinaigraph itself**. The pieces under
[`../../examples/`](../../examples/) are something else: each one showcases what the language
can do in a domain — maps, mathematics, architecture diagrams, typography, a science poster —
and none of them is about Kinaigraph. If a piece explains the tool, it belongs here; if it
demonstrates the tool on somebody's subject, it belongs there.

## The categories

| category | answers | for |
| --- | --- | --- |
| `explainer` | what Kinaigraph is, and why it exists | someone deciding whether to look further — no prior knowledge assumed, and nothing to follow along with |
| `tutorial` | how to do one thing, start to finish | someone authoring, with the document open — a task, in order, with a result at the end |
| `architecture` | how the engine itself is built | a contributor, or a reader who wants to know what is under it |

An **explainer** may leave you unable to write a scene, and that is fine: it is there to make
you want to. A **tutorial** that leaves you without a rendered file has failed. Keep a piece to
one of the two — the register is different, and a video that switches halfway serves neither
reader.

## What is here

```text
docs/video/src/<category>/<name>/
├── <name>_long.yaml          the full-length telling
├── <name>_brief.yaml         a shorter cut of the same material
├── <name>_teaser.yaml        under 30 seconds
└── resource/
    ├── scene/                the SVG artwork the animation drives
    ├── style/                the stylesheet, one class per theme
    ├── template/             the page the scene is composed into
    ├── image/                logos and raster art
    ├── script/{long,brief,teaser}/   narration, one file per part
    └── audio/{long,brief,teaser}/    the recorded narration
```

The suffix names the cut's LENGTH, and the ladder is `teaser` → `brief` → `long`. `full` and
`detailed` are reserved for a different question — how much of a subject a piece covers — so a
long cut that is still an overview can say so later without the words being spent.

Each `resource/` subfolder is named for the **asset type** the language declares — `scene`,
`style`, `template`, `image` — so what a folder holds and what a document calls it are the same
word.

| category | piece | what it covers |
| --- | --- | --- |
| `architecture` | `structural_layers` | the ports, adapters, subsystems and layers the engine is built from |

## Rendering one

**No API key is needed.** The narration audio is committed here, so a clone can render these
without paying a text-to-speech provider for recordings that already exist. That is the one way
these differ from the examples, where narration is generated and ignored.

```sh
cd docs/video/src/architecture/structural_layers
kinaigraph structural_layers_long.yaml
open ./structural_layers_long.mp4
```

Outputs land beside the document. Rendering the long piece takes a few minutes — it drives a
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
