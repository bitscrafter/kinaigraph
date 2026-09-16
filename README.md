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

Kinaigraph times animation to narration, so most scenes here read an audio clip that is
**generated from a script**, not committed. Rendering those needs an
[ElevenLabs](https://elevenlabs.io/) API key in `ELEVENLABS_API_KEY`, and each synthesis run
costs credits. Every example has a `scene_00_tts_generation.yaml` that does that step.

**Two examples render with no key** — `milestone-ladder` and `hiking-trails` both ship
their narration, so every input they use is already in this repository. Start there.

## Using it

Render the self-contained scene:

```sh
cd kinaigraph/examples/milestone-ladder
kinaigraph milestone_ladder_teaser.yaml
open ./milestone_ladder_teaser.mp4
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
kinaigraph scene_00_tts_generation.yaml
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

Each example is a set of YAML **scene** files plus its resources — SVG artwork, CSS
themes, and narration scripts. Kinaigraph compiles a scene and renders it to an MP4
(and can also play it live in the browser).

| Example | What it shows |
| --- | --- |
| [`why-a-language`](examples/why-a-language/) | The pitch, in four scenes: why explainer videos are worth making, what making them costs today, what a language does about that cost, and what it opens up. Shipped as **two cuts from one set of drawings** — a 1:39 whose voice names a category and lets the picture enumerate it, and a 2:52 that names every box aloud. **Not one duration in either is a number anyone chose.** |
| [`microservices-flow`](examples/microservices-flow/) | A narrated walkthrough of a request moving through a microservices architecture — animation paced to narration, animated diagrams, and compile-time theming (the same scene re-rendered in light and dark). |
| [`request-response`](examples/request-response/) | The same request, authored **twice** — once with hand-measured timings, once with action bookmarks and `pace_by: distance`. The two disagree, and the shorter one is the correct one. |
| [`wave-anatomy`](examples/wave-anatomy/) | `y = A · sin( B · (x − C) ) + D`, one beat per parameter. **No wave is drawn anywhere** — every curve is generated from its own equation and sampled by the compiler. |
| [`hiking-trails`](examples/hiking-trails/) | Three routes across a cartoon map, with a marker that ducks behind the scenery. One route layer carries the drawn line, the travelled path and the distance the callout quotes. |
| [`milestone-ladder`](examples/milestone-ladder/) | One life as six milestones on a rising ladder. Glyphs ride the rail they draw; two themes, light and dark. |
| [`life-lessons-en`](examples/life-lessons-en/) · [`life-lessons-es`](examples/life-lessons-es/) | Kinetic typography — quotes that fade in over paper texture, paced to spoken narration. The same two scenes in English and Spanish, which is what a localization actually costs. |
| [`kinaigraph-avatar`](examples/kinaigraph-avatar/) | A rigged picture-in-picture presenter: blinks, mouth shapes and a speech bubble, driven from one narration. |

Narration audio is generated from the scripts via text-to-speech, so a scene reads
its timing from the spoken lines. See each example's folder for its specific layout.

## License

Kinaigraph is pre-release software provided **as is**, for **non-commercial use**,
with no warranty and no support — use it at your own risk. The example projects may be
copied and modified for non-commercial purposes, with attribution.

See [LICENSE](LICENSE) for the full terms.

Copyright © 2026 José Luis Ríos Treviño. All rights reserved.
