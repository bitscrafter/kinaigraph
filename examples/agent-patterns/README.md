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

**The palette is sequential, not categorical.** One hue walked across the rows,
rather than one colour per pattern. Different colours would say these are
different *kinds* of thing; one ramp says they are one thing increasing — and
what increases is complexity, which the axis label names as a cost. `dark`
brightens toward AGENTS and `paper` darkens; in both, further along means
further from the background.

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
