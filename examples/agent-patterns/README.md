# Agent Patterns — five workflows, one agent

Seven ways to put an agentic system together, built one edge at a time on a
single canvas. The stage rewires; the ledger down the left keeps what each beat
earned; the closing frame is all of it at once.

## Where this comes from

The patterns, their names, their order and the passage that ends the piece are
from **["Building effective agents"](https://www.anthropic.com/engineering/building-effective-agents)**
— Anthropic, by Erik S. and Barry Zhang, 19 December 2024.

⚠️ The page carries two titles: its headline is *"Building effective agents"* and its
`<title>` metadata is *"Building Effective AI Agents"*. This example uses the headline,
because that is what a reader sees and what the article is cited as.

The post's own structure is one building block, five workflow patterns and one
agent pattern, and this example follows it exactly rather than inventing a
taxonomy. Words taken as published: *gate*, *sectioning*, *voting*, *ground
truth*, *stopping condition*, *pause … at checkpoints*, and the closing
quotation.

⚠️ **Words that are ours** — because a viewer cannot tell them apart on screen,
they are listed here: *decided at run time*, *tool call* (the source has "tool
call results"), *more complexity*, and the node name `WORKER`, which comes from
the prose *"delegates them to worker LLMs"* and not from the diagram, whose
boxes read `LLM Call 1/2/3`.

⚠️ **The diagrams here are redrawn, not reproduced.** The post's own images are
Anthropic's; these are new drawings in this repository's flow-diagram language.
The pattern names are vocabulary and are used as such. The one direct quotation is
the closing frame — the source's complete summary instruction, three sentences, not
a fragment of it — attributed on screen.

⚠️ **Not affiliated with, or endorsed by, Anthropic.** The quotation is used for
commentary under fair use; attribution is not itself a copyright permission, and
nothing in this repository's LICENSE grants you rights over the quoted sentences.

## Running it

```sh
kinaigraph narrate_brief.yaml        # once — needs ELEVENLABS_API_KEY, costs credits
kinaigraph agent_patterns_brief.yaml
open ./agent_patterns_brief.mp4
```

The narration has to exist before the animation will render: every beat derives
its length from its own clip's probed `.duration`, so without the audio there is
nothing for the timeline to measure.

| File | What it is |
| ---- | ---------- |
| `narrate_brief.yaml` | Synthesis only. Turns the scripts into one clip each. |
| `agent_patterns_brief.yaml` | The piece. Animation plus the composition that mixes the narration onto it. |
| `resource/scene/flow.svg` | The ledger, the seven topologies and the closing frame — all on one canvas. |
| `resource/scene/brand_layer.svg` | The brand mark, embedded as base64 data. |
| `resource/image/bitscrafter_logo.png` | The mark as a raster, before embedding. |
| `resource/style/theme_flow.css` | The palette and type. One theme. |
| `resource/script/part_NN_*.txt` | The narration, one file per beat. |
| `resource/audio/part_NN_*.mp3` | The recordings, once generated. |

## The beats

Each one adds an edge class the one before it lacked, in the source's own order —
*"progressively increase complexity, from simple compositional workflows to
autonomous agents."*

⚠️ **The order is not a ranking, and the piece has to work to say so.** The
source is explicit that *"These building blocks aren't prescriptive"*, and its
recommendation runs the other way: *"add multi-step agentic systems only when
simpler solutions fall short."* Seven rows arriving one after another on a
brightening ramp reads as a ladder whatever the author intended, so the axis is
labelled **MORE COMPLEXITY, MORE COST**, the masthead carries the source's
instruction for all 74 seconds, and the agent beat is the one beat that names
its own downside.

| Beat | Pattern | What it adds |
| ---- | ------- | ------------ |
| `atom` | Augmented LLM | The building block: retrieval, tools, memory |
| `chain` | Prompt chaining | The sequential edge, and a gate that can stop it |
| `route` | Routing | The **exclusive** branch — one lane runs, two go quiet |
| `parallel` | Parallelization | Concurrency, and a join |
| `orchestrate` | Orchestrator–workers | A lane count nobody wrote down |
| `evaluate` | Evaluator–optimizer | The first arrow that points backwards |
| `agent` | Agents | The loop closes on the world, and pauses for a human — at higher cost, and risking compounding errors |

## What this example is a good place to notice

**No timeline entry does arithmetic.** Each beat lists its ledger deposit first
and gives it the clip's own duration, so the beat is exactly as long as its line
with nothing subtracted to get there. Everything else in the beat waits on one
named move — `MOVE_2`, `MOVE_3_HEAD` — and those six names are derived from two
numbers. A beat reads top to bottom as a list of things that happen, in order.

**The build is the argument.** The patterns are not seven topics; they are the
same few parts rewired, and they sit in an order. A tour would have shown seven
pictures. This shows one picture seven times, and each transition is a single
new idea rather than a new drawing.

**Four kinds of node, and the drawing means it.** A reader who sees two stroke
colours and several box sizes will infer a taxonomy whether or not one was
intended, so every box declares a *kind* and takes that kind's stroke and size
from one table. There is no size argument at any call site.

| kind | stroke | what it is |
| ---- | ------ | ---------- |
| model | `#f6f1ec` white | an LLM invocation |
| augmentation | `#3987e5` blue | retrieval, tools, memory |
| code | `#d95926` orange | explicitly *not* a model |
| outside | `#199e70` aqua, **dashed** | not part of the system you build |
| *(terminal)* | neutral pill | where things enter and leave |

⚡ **Three of these are the source's own, which I only confirmed late.** Its
diagrams are images, so the labels are not in the page text — but the PNG can be
downloaded and read, and it uses three colours: **green** `LLM Call`, **purple**
`Aggregator` / `Gate`, and **pink pills** for `In` / `Out` / `Exit`. Our
model / code / terminal split is that split.

⚠️ **The fourth, `augmentation`, is ours.** The source colours `Retrieval`,
`Tools` and `Memory` the *same purple* as `Gate` and `Aggregator` — it has no
separate kind for them. Splitting them out is a refinement the prose supports
(*"augmentations such as retrieval, tools, and memory"* against *"programmatic
checks"*), but it is not the article's taxonomy and should not be read as one.

**Model is achromatic because it is the default.** Most boxes are model calls;
the two hues mark what *isn't* one. Colouring the common case and leaving the
exceptions plain would be the wrong way round.

⛔ **There is no `entry` kind, and there was.** It painted the head of every
pattern white while the identical thing one box along was blue — `LLM CALL 1`
white, `LLM CALL 2` not — because *entry* is a **role**, where the pattern
starts, and a role does not belong in the channel that carries **type**. The
head now takes its own kind, and its persistence is carried by the one thing
that always carried it: it never moves.

⚡ **Parallelization is the one pattern whose head is not a model.** The source
fans out from the input, so that beat's head is `IN`, a code box, and the
persistent box steps aside for it. That is also most of what separates the two
fan-out diagrams — see below.

⚠️ **`WORKER` is ours; the other node names are the source's.** Its
diagrams are images, but they download and read: `Orchestrator`,
`Synthesizer`, `Aggregator`, `Gate`, `In`, `Out`, `Exit` and `LLM Call
Router` are its own box labels. `WORKER` comes from the prose -
*"delegates them to worker LLMs"* - because the diagram's boxes there read
`LLM Call 1/2/3`.

⚡ **The aggregator/synthesiser split is the source's, and it was invisible.**
Both were one size and one colour until the kinds existed, which drew them as
the same sort of thing. They are not: outputs are *"aggregated
programmatically"*, whereas the orchestrator *"synthesizes their results"* and
is a central LLM. So `AGGREGATOR` is **code** and `SYNTHESIZER` is a **model**,
and you can now see which is which without reading the narration.

`HUMAN` is dashed for the same reason `ENVIRONMENT` is — neither is something
you build. `ENVIRONMENT` keeps its own outsized geometry as the one deliberate
exception: it is a container, not a node.

⚠️ **`AGGREGATOR` has no subtitle and should not regain one.** It said
"in code" until the kinds existed. The colour says that now and the badge
says it again; a third statement of the same fact would be the box
apologising for its own kind.

**The head of the pattern never moves.** It is the head of every topology in
turn - augmented LLM, first call in the chain, router, orchestrator, generator,
agent - and in six of the seven it is an ordinary model box. Its persistence is
carried by position alone: it is the only box that is in the same place in every
beat.

**Renaming a node means having authored every name.** The entry node carries one
`text` element per beat, stacked at a single baseline, and the `clear_*` entries
swap which one is visible.

⚠️ **A note's words cannot follow a theme, and that is worth knowing even
though it does not bite here.** `animation.annotations` is the better tool when
words belong to the document rather than the drawing, but a note's text comes
from a `type: text` asset whose `font_color` is a literal in `defs`, where no
style is in scope and `css()` cannot reach it - the open finding
`css-var-unresolvable-outside-animation` names that exact position. With one
theme declared, a literal is safe; with two it would be unreadable in one of
them. The note's *box* is themed either way, since `fill` and `stroke` on the
annotation envelope do resolve `css()`.

**Solid edges draw and dashed edges fade — and here that carries meaning.**
`reveal` works by arc-length dash offset, the same attribute a dashed stroke
already uses, so a dashed path revealed renders **nothing**, silently. Rather
than merely survive that, the piece spends it: an edge whose existence is fixed
when the diagram is drawn **draws itself**, and an edge the running system
decides on **arrives**. The orchestrator's fan-out and the agent's human
checkpoint are the two that arrive.

**The synthesiser lands after the fourth worker, and that is not a flourish.**
It sits at the centre of however many lanes exist, so there is no place to put
it until the count is known. Watching a fourth lane appear mid-sentence is what the source means by
a central LLM that *"dynamically breaks down tasks"*; on paper it is a fourth box.

**The router is a model box, and the source's diagram agrees.** Its routing
figure draws `LLM Call Router` in the same green as every other call. The prose
is broader — *"classification can be handled accurately, either by an LLM or a
more traditional classification model/algorithm"* — so the diagram commits to
the LLM realisation and so do we. The alternative has no cell in this taxonomy:
a traditional classifier is neither an LLM nor "explicitly not a model".

**Routing draws all three lanes and then dims two.** The content of routing is
that the other lanes *do not run*. Drawing only the chosen lane would have shown
a chain. They dim to `DIM_TO` rather than to zero, because a router that erased
the alternatives would be a gate.

**Every beat deposits a miniature, and that is why this is a video.** A still
diagram cannot accumulate. The closing frame reads as an argument only because
the viewer watched each row being earned, one at a time — which is the one thing
the source post, being a page, cannot do.

**Two encodings, two channels, two regions.** Colour and lightness were both
carrying *which row is this*, which left nothing to say *what a box is*. They
are split now and nothing crosses over: the **ledger** — rail ticks and
miniatures — is a warm-neutral **lightness** ramp, because it is an axis and
axes should be recessive; the **stage** is **hue**, and every colour there names
a kind. So colour = what a box is, lightness = how complex the row is.

⚡ **The two chromatic hues were computed, not chosen.** Any two kinds can share
a frame, so this is an *all-pairs* case. Orange / aqua: CVD ΔE **9.4**,
normal-vision ΔE **26.5**, both ≥3:1 on the surface. White measures **16.9:1**
against the surface and ≥3:1 against both hues.

⚠️ **Two earlier palettes failed the validator, which is why it gets run.**
Blue / aqua / violet — violet against blue at ΔE 9.8 normal-vision, under the 15
floor. And yellow beside orange at ΔE 10.6 normal-vision, CVD 4.8: a yellow
`model` forces `code` off orange entirely.

⚠️ **The ramp's dim end has a floor.** A first ramp starting `#3a352f` measured
**1.56:1** against the background, under the 2:1 minimum — the step existed and
could not be seen. It starts at `#544c43` and measures 2.25:1.

**One theme.** `paper` was declared and never rendered — the document captures
`theme: dark` — so every claim about it was untested. An unexercised theme in a
published example is a liability, not a feature. Its values are now at `:root`
rather than under a theme selector, which is also what lets `css()` reach them.

**The scripts are a word budget.** A beat is as long as its own sentence by
construction, so the length of the piece is decided in `resource/script/` and
nowhere else — there is no edit in which to trim it.

⚠️ **Word count alone predicts badly.** Measured across one synthesis, the voice
ran between **0.371 and 0.557 seconds per word** depending on punctuation — a
50% spread, which is the difference between 74 and 89 seconds over a piece this
long. Budget with each line's own measured rate, not an average, and re-measure
after any rewrite. The nine scripts run 165 words and the piece renders
74.1 s.

**A scene opens on its own.** Every `var()` in `flow.svg` is emitted with the
stylesheet's `dark` value as its fallback, so opening it in a browser, an editor
or a GitHub preview shows the dark theme rather than unstyled shapes. The scene
carries the *mapping*, the stylesheet carries the *values*, and the generator
emits both from one table so they cannot drift.

**Arial only, deliberately.** Nothing in the stylesheet may name a font that is
not installed by default on Windows, macOS and Linux — an example that renders
differently depending on who clones it is a broken example.

**Every box says what it is, so there is no legend.** The icon marks the
TYPE and the classifier word beside it names that type, while the box's
own name in the middle says which one - `ORCHESTRATOR` is an instance of
LLM, `MEMORY` an instance of AUGMENTATION. Nothing has to be looked up, so
nothing has to be listed.

⚠️ **This example therefore uses no `annotation.note`.** It carried a
four-chip legend built from notes until the badges made it redundant, and
that was the repository's one demonstration of the feature. If it should
demonstrate one, the better showcase is a *pointered* callout - a note
with a leader line tracking an actor, which a static legend never
exercised.

**The source's own division is on the ledger.** Three brackets — BUILDING BLOCK,
WORKFLOWS, AGENT — because that split is the article's section headings, not a
reading of them, and it used to live only in the narration. A viewer who joins
late, or watches without sound, could not see it anywhere in the frame.

**Names are the contract.** Every pattern carries a slug — `orchestrate` — and
it is the SVG id suffix (`g-orchestrate`, `rail-orchestrate`, `mini-orchestrate`,
`lbl-entry-orchestrate`), the timeline bookmark, *and* the script filename
suffix (`part_06_orchestrate.txt`). Re-order the piece and nothing can silently
pair a line with the wrong topology.

## Editing it

⚠️ **The topologies overlap on the canvas.** `chain` puts a node at x=1240 and
`route` puts one at x=1330. They collide in the artwork and only the timeline
keeps them apart, which is why every beat is preceded by its own `clear_*` entry
taking the previous group to zero *before* the next one starts. There is no
crossfade anywhere in the piece. Add one and two patterns will be on screen at
the same time, partly on top of each other.

⚠️ **`flow.svg` is not legible as a still.** All seven topologies are on one
canvas, so opening it shows them piled up. Use `resource/helper/make_beat_previews.py`
to rasterise one beat at a time; a layout mistake is invisible until the beats
are separated.

⚠️ **No `.edge` may ever carry a `stroke-dasharray`.** `reveal` drives that same
attribute, so a dashed shaft that gets revealed renders nothing at all, and
nothing warns you. If an edge needs to be dashed, it belongs in a `*_body` or
`*_fan_*` group and it fades.

⚠️ **Change `DRAW_MS` or `FADE_MS` and every move moves.** The six `MOVE_*`
constants are derived from those two, and they are the only offsets in the
document. That is deliberate — retiming the piece should be two numbers, not
forty — but it does mean a longer `DRAW_MS` pushes the last move later in every
beat at once. Three moves plus a head is about 2.5 s; keep it well inside the
shortest clip.

⚠️ **`synthesis.context.status` is section-wide.** Re-running `narrate_brief.yaml`
regenerates every clip and bills for every clip, even if you edited one line.

⚠️ **An action's window is `hold.before + duration + hold.after`.** A beat is as
long as its longest actor's window, which is why each beat lists its deposit
first and gives it the clip's duration — that one line sets the beat's length,
and nothing else in the beat may run past it.
