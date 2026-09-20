# Kinaigraph

**A declarative language for animation and motion graphics.** You author scenes in YAML that bring together your SVG artwork and narration scripts, declaring how they work together and what happens when. Kinaigraph does the tedious, exacting work: timing motion to narration, interpolating every frame, and keeping audio and video in sync — then renders the scene as a video file or live playback in the browser.

This repository is the public home for Kinaigraph. It will hold the **examples**, the
**binaries**, and the **documentation**.

## Status — pre-release (alpha)

Kinaigraph is early software, rolling out in stages:

- ✅ **Examples** — complete, compiler-validated example projects. Available now (below).
- ✅ **Binaries** — the Kinaigraph command-line tool that renders the examples. Available now, from [Releases](https://github.com/bitscrafter/kinaigraph/releases).
- 🔜 **Documentation** — a guide to authoring with Kinaigraph. Coming later.
- 🗓 **Releases expire** — every alpha release stops rendering on a date; `kinaigraph doctor`
  shows it. See [Each release expires](#each-release-expires).

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

⚠️ **You need an administrator account on the Mac.** Installing the media encoder uses
Homebrew, which requires one, and putting the binary on your `PATH` uses `sudo`. If the account you are using
cannot run `sudo`, stop here — the rest of this section will not work.

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

### 1. What Kinaigraph needs

Kinaigraph renders in a real browser and encodes with a real encoder, so two things must
already be on your machine before it can do anything.

**A browser** — Kinaigraph drives it to rasterize each frame.
[Google Chrome](https://www.google.com/chrome/) is the usual choice; Chromium and Edge also
work. Download and install it the ordinary way; there is no command-line route worth
preferring.

**A media encoder** — it encodes the frames into an MP4 and muxes the narration audio.
[`ffmpeg`](https://ffmpeg.org/) is the usual choice, by way of
[Homebrew](https://brew.sh/). If you do not have Homebrew:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then:

```sh
brew install ffmpeg
```

Homebrew will tell you to add its directory to your `PATH` and print the exact lines for your
shell. Do what it says — on Apple Silicon it installs to `/opt/homebrew/bin`, which is **not**
on a fresh account's `PATH`, and the encoder will be invisible until you add it.

### 2. Install Kinaigraph

Download the matching archive from
[Releases](https://github.com/bitscrafter/kinaigraph/releases), then:

```sh
tar -xzf kinaigraph-<version>-<your-arch>-apple-darwin.tar.gz
sudo mv kinaigraph /usr/local/bin/
```

If you would rather not use the command line to unpack it, double-click the `.tar.gz` in
Finder — macOS extracts it with Archive Utility — and then run the `sudo mv` line against
wherever it landed.

Two things are happening:

1. **Extract.** The archive holds the `kinaigraph` binary and this project's `LICENSE`.
2. **Move it onto your `PATH`.** `/usr/local/bin` is on the default macOS `PATH`, so after
   this you can type `kinaigraph` from any directory. That is the form every example in this
   repository uses; before this step you would have to type `./kinaigraph`.

`sudo` is needed even on an administrator account: `/usr/local/bin` is owned by `root`, and
being an administrator means you *may* use `sudo`, not that you own root's directories.

Now check the install:

```sh
kinaigraph --version
kinaigraph doctor
```

`--version` prints `kinaigraph` and the version — that tells you the binary is installed and
on your `PATH`.

`doctor` is the one that matters: it tells you whether Kinaigraph can actually do its job.
Under **Tools** you want all three found, each with a version and a path:

```text
    Tools
        Browser: Google Chrome 152.0.7977.83
            Authoritative: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
        Media Encoder: ffmpeg 9.0.1
            Authoritative: /opt/homebrew/bin/ffmpeg
        Media Inspector: ffprobe 9.0.1
            Authoritative: /opt/homebrew/bin/ffprobe
```

Your versions and paths will differ. What matters is that none of the three says `Not Found`.
If one does, `doctor` prints what it searched and a `Hint:` telling you what to do:

```text
        Media Encoder: Not Found
            Authoritative: None Identified
                Searched:
                    Platform
                        $PATH                    not found
                        Standard Locations       not found
                Hint: this machine has no media encoder; install one
            Alternatives: None Identified
```

That is almost always `ffmpeg` missing, or installed but not on your `PATH` — see step 1.
Fix it before going further; rendering will fail without it.

### Each release expires

Every alpha release carries the date it stops rendering. `doctor` shows it under
**Kinaigraph**, directly beneath the version:

```text
    Kinaigraph
        Version: 0.1.0-alpha.1
        Expires: 2026-12-31 (UTC)
```

In the last two weeks before that date every render prints a notice naming it. After it,
`kinaigraph run` and the compiler refuse with a message pointing at
[Releases](https://github.com/bitscrafter/kinaigraph/releases), and `doctor` says `expired`.
Nothing else changes: `--version`, `--help` and `doctor` keep working, and your documents are
untouched. Download a newer release and carry on.

### If macOS refuses to run it

You will probably not need this. A binary you downloaded through a browser carries a
**quarantine** flag, and the flag survives extraction — but macOS only enforces it when
something is launched through Finder (double-clicking it, or `open`). Typing `kinaigraph` in
Terminal is not blocked.

If you do launch it that way and macOS says *"cannot be opened because the developer cannot be
verified"*, clear the flag on the **extracted binary** — not on the `.tar.gz`:

```sh
xattr -dr com.apple.quarantine /usr/local/bin/kinaigraph
```

Kinaigraph is signed but not notarized during the alpha, which is why the flag matters at all.

### Verifying a download

Each archive ships a `.sha256` beside it:

```sh
shasum -a 256 -c kinaigraph-<version>-<your-arch>-apple-darwin.tar.gz.sha256
```

## Get the examples

The binary does not come with any scenes. The examples live in this repository — clone it:

```sh
git clone https://github.com/bitscrafter/kinaigraph.git
cd kinaigraph/examples
```

Or download the ZIP from the [repository page](https://github.com/bitscrafter/kinaigraph)
(**Code → Download ZIP**) and unpack it, if you would rather not use `git`.

### ⚠️ Most examples need a text-to-speech key

Kinaigraph times animation to narration, so most scenes here read an audio clip spoken by a
text-to-speech provider. Where that clip is committed you need nothing; where it is not,
rendering needs an [ElevenLabs](https://elevenlabs.io/) API key in `ELEVENLABS_API_KEY`, and
each synthesis run costs credits. The synthesis step is always its own document, named for
the cut it speaks.

**Every one of the 9 examples renders with no key.** Their narration is committed, so a
clone can render all of them with nothing but Kinaigraph installed. A key is only needed
to RE-record a line — each example's `narrate_*.yaml` does that, and costs credits.
The videos under `docs/video/` are the same, except where their recordings are committed.

## Using it

Render the self-contained scene:

```sh
cd kinaigraph/examples/infographic-atmosphere
kinaigraph infographic_atmosphere_teaser.yaml
open ./infographic_atmosphere_teaser.mp4
```

That is the whole loop: a scene file in, an MP4 out.

Outputs land in the folder containing the scene file, beside it. Paths *inside* a scene
resolve against that same folder, so what a scene writes is where the next scene looks for
it — which is why you `cd` into the example first.

`--outdir` moves that base somewhere else for one run, without editing the scene. You do
not need it for the loop above.

To render anything else, set `ELEVENLABS_API_KEY`, generate that example's narration once, and
then render its scenes:

```sh
export ELEVENLABS_API_KEY=...
kinaigraph narrate.yaml
kinaigraph scene_01_<name>.yaml
```

Each example's own README says what it shows and which scenes it has.

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
        --outdir <path> Where outputs are written.
                        Default: the folder containing <input.yaml>
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

Some examples tell their subject at more than one length, and the document's
suffix says which: **`_teaser`** under 30 seconds, **`_brief`** around a minute,
**`_long`** for the full-length telling. Each cut carries its own scripts and
recordings under `resource/script/<cut>/` and `resource/audio/<cut>/`, so you can
read or render one without the others.

Each example is a set of YAML **scene** files plus its resources — SVG artwork, CSS
themes, and narration scripts. Kinaigraph compiles a scene and renders it to an MP4
(and can also play it live in the browser).

Every one of them is about **somebody else's subject** — a map, an equation, a poster, a
life. For videos about Kinaigraph itself, see [Documentation videos](#documentation-videos)
below, whose sources are kept the same way.

| Example | What it shows | Watch |
| --- | --- | --- |
| [`request-response`](examples/request-response/) | A "Get User Profile" request walks a small system. One packet rides the drawn connectors through six legs, paced by distance so it holds one speed, with payload callouts that keep aiming at it as it travels. | [watch](https://youtu.be/PASTE) |
| [`wave-anatomy`](examples/wave-anatomy/) | `y = A · sin( B · (x − C) ) + D`, one beat per parameter. **No wave is pre-drawn anywhere** — every curve is generated from its own equation and sampled by the compiler. | [watch](https://youtu.be/PASTE) |
| [`hiking-trails`](examples/hiking-trails/) | Three routes across a cartoon map, with a marker that ducks behind the scenery. One route layer carries the drawn line, the travelled path and the distance the callout quotes. | [watch](https://youtu.be/PASTE) |
| [`milestone-ladder`](examples/milestone-ladder/) | One life as six milestones on a rising ladder. Glyphs ride the rail they draw; two themes, light and dark. | [teaser](https://youtu.be/PASTE) · [brief](https://youtu.be/PASTE) |
| [`life-lessons`](examples/life-lessons/) | Kinetic typography — quotes that fade in over paper texture, paced to spoken narration. The same two scenes in **English and Spanish**, sharing one paper, one stylesheet and one timeline: a localisation you can count rather than take on trust. | [English](https://youtu.be/PASTE) · [Spanish](https://youtu.be/PASTE) |
| [`course-welcome`](examples/course-welcome/) | The first half-minute of an online course: an instructor talks, blinks and breathes in the corner while the practicalities arrive beside her. Three mouth shapes and two eye states, swapped by pulses written against each other — the language has no concept of a face. | [watch](https://youtu.be/PASTE) |
| [`infographic-atmosphere`](examples/infographic-atmosphere/) | A narrated tour of **a picture that already existed** — a PNG poster nobody authored here. The language has no camera, so the picture moves instead, and callouts park in the frame while it pans beneath them. | [teaser](https://youtu.be/PASTE) · [brief](https://youtu.be/PASTE) |
| [`coffee-order`](examples/coffee-order/) | A café order as a **sequence diagram**, drawn as it is told. The one diagram whose vertical axis is time, so the drawing runs deeper than the frame and the camera walks down it. A mug rides every message, and during the `par` two are in flight at once. | [watch](https://youtu.be/PASTE) |
| [`agent-patterns`](examples/agent-patterns/) | Seven ways to put an agentic system together — one building block, five workflow patterns and one agent pattern, after Anthropic's *Building effective agents* — built one edge at a time on a single canvas. The stage rewires between beats, a ledger down the left keeps what each beat earned, and the closing frame shows all of it at once. | [watch](https://youtu.be/PASTE) |

Narration audio is generated from the scripts via text-to-speech, so a scene reads
its timing from the spoken lines. See each example's folder for its specific layout.

## Documentation videos

The videos that explain Kinaigraph are made with Kinaigraph, and their sources live under
[`docs/video/`](docs/video/) in the same shape as an example: scene files, artwork, a
stylesheet, and narration scripts with their recordings. Every recording is committed, so
both render from a clone with no key.

| Video | What it covers | Watch |
| --- | --- | --- |
| [`why-a-language`](docs/video/src/product/why-a-language/) | The case for Kinaigraph, in four scenes: why explainer videos are worth making, what making them costs today, what a language does about that cost, and what it opens up. Two cuts from one set of drawings — a **brief** that names a category and lets the boxes enumerate it, and a **long** that names every box — differing in narration and theme and in nothing else. | [brief](https://youtu.be/PASTE) · [long](https://youtu.be/PASTE) |
| [`structural_layers`](docs/video/src/architecture/structural_layers/) | How the engine itself is built: the ports, adapters, subsystems and layers, over one diagram. Three cuts of that diagram — a **teaser**, a **brief** that names each ring in a breath, and a **long** that gives every port and subsystem its own beat. | [teaser](https://youtu.be/PASTE) · [brief](https://youtu.be/PASTE) · [long](https://youtu.be/PASTE) |

Each piece is one folder with its cuts side by side. [`docs/video/README.md`](docs/video/README.md)
says which category a piece belongs to and how to render one.

## Feedback

Feedback is welcome through the repository's
[issue tracker](https://github.com/bitscrafter/kinaigraph/issues). The report that matters most
during the alpha is an example from this repository that rendered on one release and stops on the
next — that is the measure in [What ends the alpha](#what-ends-the-alpha). Include the output of
`kinaigraph --version` and `kinaigraph doctor`, the document you ran, and the command.

There is no support commitment while Kinaigraph is pre-release; see [LICENSE](LICENSE).

## License

Kinaigraph is pre-release software provided **as is**, for **non-commercial use**,
with no warranty and no support — use it at your own risk. The example projects may be
copied and modified for non-commercial purposes, with attribution.

See [LICENSE](LICENSE) for the full terms.

Copyright © 2026 José Luis Ríos Treviño. All rights reserved.
