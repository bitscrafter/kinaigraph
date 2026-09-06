# Kinaigraph

**A declarative language for animation and motion graphics.** You author scenes in YAML that bring together your SVG artwork and narration scripts, declaring how they work together and what happens when. Kinaigraph does the tedious, exacting work: timing motion to narration, interpolating every frame, and keeping audio and video in sync — then renders the scene as a video file or live playback in the browser.

This repository is the public home for Kinaigraph. It will hold the **examples**, the
**binaries**, and the **documentation**.

## Status — pre-release (alpha)

Kinaigraph is early software, rolling out in stages:

- ✅ **Examples** — complete, compiler-validated example projects. Available now (below).
- ✅ **Binaries** — the Kinaigraph command-line tool that renders the examples. Available now, from [Releases](https://github.com/bitscrafter/kinaigraph/releases).
- 🔜 **Documentation** — a guide to authoring with Kinaigraph. Coming later.

Until the authoring guide lands, the examples are the documentation: each carries a
README describing what it shows and how to render it.

### What ends the alpha

The `-alpha` is dropped when the authoring language goes one full release without a change
that stops an existing example in this repository from rendering. The condition is about
the **language**, not the tool: what an alpha warns you about is that a scene you write may
need editing to keep working across a release. The examples below are the measure — every
release renders all of them end to end — so this is something you can check rather than
something we judge.

## Install

macOS only, for now. Two builds are published with every release:

| your Mac | download |
| --- | --- |
| Apple Silicon (M1 and later) | `kinaigraph-<version>-aarch64-apple-darwin.tar.gz` |
| Intel | `kinaigraph-<version>-x86_64-apple-darwin.tar.gz` |

If you are not sure which you have, ask the machine — `uname -m` prints `arm64` on Apple
Silicon and `x86_64` on Intel:

```sh
uname -m
```

Download the matching archive from [Releases](https://github.com/bitscrafter/kinaigraph/releases),
then:

```sh
tar -xzf kinaigraph-<version>-<your-arch>-apple-darwin.tar.gz
xattr -dr com.apple.quarantine kinaigraph
sudo mv kinaigraph /usr/local/bin/
```

Three things are happening there, and the middle one is the surprising one:

1. **Extract.** The archive holds the `kinaigraph` binary and this project's `LICENSE`.
2. **Clear the quarantine flag.** macOS marks anything a browser downloaded, and refuses
   to run it unsigned — *"cannot be opened because the developer cannot be verified."*
   The command above clears that flag, and it is applied to the **extracted binary**, not
   to the `.tar.gz`. (Kinaigraph is signed but not notarized during the alpha.)
3. **Move it onto your `PATH`.** `/usr/local/bin` is on the default macOS `PATH`, so after
   this you can type `kinaigraph` from any directory. That is the form every example in
   this repository uses.

Verify the install:

```sh
kinaigraph --version
```

It should print `kinaigraph` followed by the version you downloaded.

### Verifying a download

Each archive ships a `.sha256` beside it:

```sh
shasum -a 256 -c kinaigraph-<version>-<your-arch>-apple-darwin.tar.gz.sha256
```

### What else you need

Kinaigraph renders in a real browser and encodes with a real encoder, so two things must
already be on your machine:

- **[Google Chrome](https://www.google.com/chrome/)** — Kinaigraph drives it to rasterize
  each frame. Chromium and Edge also work.
- **[`ffmpeg`](https://ffmpeg.org/)** — used to encode the frames into an MP4 and to mux
  the narration audio. `brew install ffmpeg` is the usual route.

Run `kinaigraph doctor` to see what Kinaigraph found and what it could not:

```sh
kinaigraph doctor
```

## Using it

Compile and render a scene by naming its YAML file:

```sh
kinaigraph scene_01_flow.yaml --outdir ./out
```

`--outdir` is where the outputs are written; it defaults to `./out`. Paths *inside* a
scene resolve against that scene's own folder, so run Kinaigraph from the example's root.

### Command-line reference

`kinaigraph --help` prints:

```text
Usage
    kinaigraph [run] <input.yaml> [--outdir <path>]
    kinaigraph doctor [<input.yaml>]

Commands
    run                 Compile and render a document. The default — a bare
                        path is a run.
        <input.yaml>    The document to compile.
        --outdir <path> Where outputs are written. Default: ./out
    doctor              Report dependency resolution.
        <input.yaml>    Optional. Also report what this document declares
                        and whether it will resolve.

Options
    --help              Print this and exit.
    --version           Print the version and exit.

Environment
    KINAIGRAPH_BROWSER          Browser executable — Chrome, Chromium, or Edge
    KINAIGRAPH_MEDIA_ENCODER    ffmpeg executable
    KINAIGRAPH_MEDIA_INSPECTOR  ffprobe executable
    KINAIGRAPH_WEB_RUNTIME_HOME Browser runtime assets
```

`kinaigraph --version` prints the tool's name and version on one line, for example
`kinaigraph 0.1.0-alpha.1`.

The four environment variables are overrides. You do not need to set any of them: a
released build carries its own browser runtime, and finds Chrome and `ffmpeg` on your
`PATH`. Set one only when you want a specific executable used.

## Examples

Each example is a set of YAML **scene** files plus its resources — SVG artwork, CSS
themes, and narration scripts. Kinaigraph compiles a scene and renders it to an MP4
(and can also play it live in the browser).

| Example | What it shows |
| --- | --- |
| [`microservices-flow`](examples/microservices-flow/) | A narrated walkthrough of a request moving through a microservices architecture — animation paced to narration, animated diagrams, and compile-time theming (the same scene re-rendered in light and dark). |
| [`service-interaction`](examples/service-interaction/) | The same request, authored **twice** — once with hand-measured timings, once with action bookmarks and `pace_by: distance`. The two disagree, and the shorter one is the correct one. |
| [`wave-anatomy`](examples/wave-anatomy/) | `y = A · sin( B · (x − C) ) + D`, one beat per parameter. **No wave is drawn anywhere** — every curve is generated from its own equation and sampled by the compiler. |
| [`hiking-trails`](examples/hiking-trails/) | Three routes across a cartoon map, with a marker that ducks behind the scenery. **None of the route geometry is authored** — the trails were painted by hand and traced. |
| [`bio-journey`](examples/bio-journey/) | A narrated portrait in three beats: a title card, a career timeline, and a world map. Narration-driven timing throughout. |
| [`life-lessons-en`](examples/life-lessons-en/) · [`life-lessons-es`](examples/life-lessons-es/) | Kinetic typography — quotes that fade in over paper texture, paced to spoken narration. The same two scenes in English and Spanish, which is what a localization actually costs. |
| [`kinaigraph-avatar`](examples/kinaigraph-avatar/) | A rigged picture-in-picture presenter, exported from a Claude Design session. |

Narration audio is generated from the scripts via text-to-speech, so a scene reads
its timing from the spoken lines. See each example's folder for its specific layout.

## License

Kinaigraph is pre-release software provided **as is**, for **non-commercial use**,
with no warranty and no support — use it at your own risk. The example projects may be
copied and modified for non-commercial purposes, with attribution.

See [LICENSE](LICENSE) for the full terms.

Copyright © 2026 José Luis Ríos Treviño. All rights reserved.
