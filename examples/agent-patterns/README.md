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
taxonomy. Its vocabulary is used as published: *gate*, *sectioning*, *voting*,
*ground truth*, *workflows offer predictability*.

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
| `resource/style/theme_flow.css` | The palette and type, in two themes. |
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

| kind | stroke | size | what it is |
| ---- | ------ | ---- | ---------- |
| model | `#f6f1ec` white, solid | 290×84 | an LLM invocation |
| code | `#d95926` orange, solid | 200×62 | explicitly *not* a model |
| outside | `#199e70` aqua, **dashed** | 200×62 | not part of the system you build |

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

⚠️ **The `LLM ` prefix on labels is ours, not the source's.** Its diagrams are
images and their box labels cannot be read from the page, so nothing here claims
to reproduce them. The prefix is added because a white box says "model call"
only to a reader who consulted the legend, and `WORKER 4` says it to nobody.

⚡ **The aggregator/synthesiser split is the source's, and it was invisible.**
Both were one size and one colour until the kinds existed, which drew them as
the same sort of thing. They are not: outputs are *"aggregated
programmatically"*, whereas the orchestrator *"synthesizes their results"* and
is a central LLM. So `AGGREGATOR` is **code** and `SYNTHESIZER` is a **model**,
and you can now see which is which without reading the narration.

`HUMAN` is dashed for the same reason `ENVIRONMENT` is — neither is something
you build. `ENVIRONMENT` keeps its own outsized geometry as the one deliberate
exception: it is a container, not a node.

⚠️ **A `code` box cannot carry two lines.** `AGGREGATOR` had an "in code"
subtitle that clipped its own bottom edge at 62 high. It was dropped rather than
made to fit — if the taxonomy is real, a box should not also have to spell out
what it is.

**The entry node never moves and never changes colour.** It is the head of every
topology in turn — augmented LLM, first call in the chain, router, input,
orchestrator, generator, agent — and it is the one shape that does not take the
complexity ramp. A constant that re-tinted itself every beat would be claiming
to be seven things.

**Renaming a node means having authored every name.** The entry node carries one
`text` element per beat, stacked at a single baseline, and the `clear_*` entries
swap which one is visible.

⚠️ The other way to author text is `animation.annotations` — a note whose words
come from a `type: text` asset. It is the better tool when the words belong to
the document rather than the drawing, but it cannot be used here: a text asset's
`font_color` is a literal in `defs`, where no style is in scope and `css()`
cannot reach it. This example declares two themes whose title ink sits at
opposite ends of the ramp, so one literal would be unreadable in one of them.
Text that must follow a theme belongs in the scene.

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
after any rewrite. 160 words lands at 73.9 s.

**A scene opens on its own.** Every `var()` in `flow.svg` is emitted with the
stylesheet's `dark` value as its fallback, so opening it in a browser, an editor
or a GitHub preview shows the dark theme rather than unstyled shapes. The scene
carries the *mapping*, the stylesheet carries the *values*, and the generator
emits both from one table so they cannot drift.

**Arial only, deliberately.** Nothing in the stylesheet may name a font that is
not installed by default on Windows, macOS and Linux — an example that renders
differently depending on who clones it is a broken example.

**The legend is authored in the document, not drawn.** Four `annotation` notes,
each a box painted like the kind it names, so the legend is a specimen rather
than a description of one. Changing a word is an edit to
`agent_patterns_brief.yaml` — no generator run, no SVG.

⛔ **Except the dash.** An annotation envelope has `fill`, `stroke`,
`stroke_width` and `opacity`, and no way to say `stroke-dasharray`. So the
`outside` chip carries the hue but not the whole signal: dashed on the stage,
solid in the legend.

⚠️ **A note's text colour cannot follow a theme.** `font_color` is a literal in
`defs`, where no style is in scope and `css()` cannot reach — the open finding
`css-var-unresolvable-outside-animation` names this exact position. It is only
safe here because the document declares one theme. The note's *box* is themed;
its words are not.

⚠️ **An annotation must be addressed or the compiler warns.** Declared and never
referenced, all four rendered correctly and still raised *"the generated element
is constructed but never animated"*. They are shown in `setup`.

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
