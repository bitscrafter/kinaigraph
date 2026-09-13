#!/usr/bin/env python3
"""Generates why-a-language's challenge and benefit scenes.

⚠️ THE GEOMETRY IS HERE, NOT IN THE SVG. Both scenes are regular grids of boxes,
and hand-editing a coordinate in a grid is how a grid stops being one. Edit the
tables below and re-run; nothing in the two generated files should ever be
edited directly.

    python3 resource/temp/make_scenes.py

⚠️ SYMBOLS ARE COPIED FROM THE SHARED CATALOG, which lives in the engine repo at
`tech-docs/internal/design/diagram/icon-catalog.svg`. An icon edit belongs
upstream first; this script only mirrors. Catalog ids carry hyphens and scene
ids may not, so every id is converted on the way in.

⚠️ EVERY var() IS EMITTED WITH THE DARK THEME'S VALUE AS ITS FALLBACK, read from
`resource/style/theme_dark.css` — so the two cannot drift, and a scene opened on
its own shows the dark theme rather than unstyled shapes.
"""
import re, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent.parent.parent      # the example root
CATALOG = pathlib.Path(
    "/Volumes/Samsung SSD 9100 PRO/_Dev/project/kinaigraph-suite/"
    ".worktrees/core-icon-catalog/tech-docs/internal/design/diagram/icon-catalog.svg")

FONT = 'Arial, "Liberation Sans", Helvetica, sans-serif'

# ── the dark theme is the source of every fallback ───────────────────────────
DARK = dict(re.findall(r'^\s*(--[a-z-]+):\s*(.+?);',
                       (HERE / "resource/style/theme_paper.css").read_text(), re.M))

def v(name):
    """A var() call carrying the theme's own value as its fallback."""
    assert name in DARK, f"{name} is not declared in theme_paper.css"
    return f"var({name}, {DARK[name]})"

# ── symbols ──────────────────────────────────────────────────────────────────
_CAT = CATALOG.read_text()
_SYM = {m.group(2): m.group(1)
        for m in re.finditer(r'(<symbol id="([^"]*)".*?</symbol>)', _CAT, re.S)}

def symbols(names):
    out = []
    for n in names:
        assert n in _SYM, f"{n} is not in the icon catalog"
        out.append(_SYM[n].replace(f'id="{n}"', f'id="{n.replace("-", "_")}"'))
    return "\n".join(out)

ICON_RULE = {
    "icon-fill":          ("fill",   "--icon-fill"),
    "icon-fill-light":    ("fill",   "--icon-fill-light"),
    "icon-fill-medium":   ("fill",   "--icon-fill-medium"),
    "icon-fill-dark":     ("fill",   "--icon-fill-dark"),
    "icon-stroke":        ("stroke", "--icon-stroke"),
    "icon-stroke-light":  ("stroke", "--icon-stroke-light"),
}

def icon_rules(names):
    """⚠️ Only the classes the MIRRORED SYMBOLS ACTUALLY CARRY. Emitting the whole
       vocabulary would leave rules no element in this scene reads, which is the
       dead-variable problem one level down."""
    carried = set()
    for n in names:
        for c in re.findall(r'class="([^"]*)"', _SYM[n]):
            carried.update(c.split())
    out = []
    for cls in ICON_RULE:                       # a stable order, not set order
        if cls not in carried: continue
        prop, var = ICON_RULE[cls]
        out.append(f"            .{cls} {{\n                {prop}: {v(var)};\n            }}")
    missing = carried - set(ICON_RULE)
    assert not missing, f"a mirrored symbol carries an unmapped class: {missing}"
    return "\n\n".join(out)

def sid(n):
    return n.replace("-", "_")

def esc(t):
    return t.replace("&", "&amp;")

# ════════════════════════════════════════════════════════════════════════════
# SCENE 2 — the challenge
# ════════════════════════════════════════════════════════════════════════════
# ⚠️ The common band is TWO ROWS (4 then 3) because seven boxes do not fit
# across 1920 at a width that leaves room for a label. The second row is
# centred against the first rather than left-aligned with it.
C_BOX_W, C_BOX_H = 320, 130          # common band
K_BOX_W, K_BOX_H = 320, 125          # the two comparison columns
C_ROW_A_Y, C_ROW_B_Y = 95, 245
K_TOP_Y, K_PITCH = 480, 148
TRAD_X, AI_X = 400, 1200

# ⚠️ THE ORDER IS THE CATEGORY ORDER, and it is load-bearing. Row A holds two
# categories side by side and row B holds the third whole, so NO CATEGORY SPANS
# BOTH ROWS. That matters because the rows are offset 200 under 320-wide boxes,
# so every adjacent row-A/row-B pair overlaps by 120 px — two boxes that overlap
# AND travel together cross each other on the way in. Measured: the original
# order put `Variations Resist` and `Re-Author` in one category, 120 px apart.
COMMON = [
    # (icon, line 1, line 2)                          — row A left: all hand work
    ("sync",         "Syncing",            "Animation & Audio"),
    ("street-cone",  "Labor Intensive",    "Repetitive Work"),
    #                                                 — row A right: never becomes software
    ("version",      "Hard to Version",    "Control"),
    ("pen2",         "Styling Drifts",     "Video to Video"),
    #                                                 — row B: does not survive change
    ("robotic-arm",  "Variations Resist",  "Automation"),
    ("clock",        "Stale Content",      "Heavy Re-work"),
    ("language",     "Re-Author",          "Every Language"),
]
TRADITIONAL = [
    ("adjustment",   "Manual Timeline",    "Adjustments"),
    ("animation",    "Tedious Keyframe",   "Animation"),
    ("qr-code",      "Asset Management",   "Overhead"),
    ("padlock",      "Proprietary Assets", "Locked to Vendor"),
]
AI = [
    ("die",           "Trial & Error",     "Uncertain Output"),
    ("square-ruler",  "Limited Precision", "& Control"),
    ("money-sack",    "Usage Costs",       "Scale"),
    ("video-composed","Binary Output",     "No Source"),
]

def scene2_style(used):
    return f"""        <style>
            /* ── Mapping only: class -> variable. The VALUES live in
                  ../style/theme_dark.css and ../style/theme_light.css. ───────
               Every var() carries the PAPER value as its fallback, so this
               file opened on its own shows paper rather than unstyled shapes. ⚠️ GENERATED — see resource/temp/make_scenes.py. */

            .canvas-bg {{
                fill: {v('--scene-background-color')};
            }}

            /* The icon catalog's vocabulary — only the classes this scene's
               own glyphs carry. */
{icon_rules(used)}

            /* The fifteen pain-point boxes. Fill and stroke are split across two
               classes because the same rect takes both and the icons reuse
               neither — `class="box-bg box-stroke"` is the whole mapping. */
            .box-bg {{
                fill: {v('--box-fill-color')};
            }}

            .box-stroke {{
                stroke: {v('--box-stroke-color')};
            }}

            /* A box's own two lines. Size and weight are authored here rather
               than per element: every one is the same label at the same rank. */
            .box-text {{
                fill: {v('--box-text-color')};
                font-family: {v('--diagram-font-family')};
                font-size: 22px;
                font-weight: bold;
                text-anchor: middle;
            }}

            /* The band heading and the two section headings. Size stays on the
               elements — 48 for the band, 42 for a section. */
            .text-primary {{
                fill: {v('--title-text-color')};
                font-family: {v('--diagram-font-family')};
            }}
        </style>"""

def chal_box(gid, x, y, w, h, icon, l1, l2):
    """⚠️ The text is anchored 35 RIGHT of centre, to clear the icon on the left.
       That asymmetry is why the usable label width is ~200 and not the box width."""
    ax = x + 195
    iy = y + (h - 55) // 2
    return (f'        <g id="{gid}">\n'
            f'            <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"'
            f' class="box-bg box-stroke" stroke-width="2"/>\n'
            f'            <use href="#{sid(icon)}" x="{x+20}" y="{iy}" width="55" height="55"/>\n'
            f'            <text x="{ax}" y="{y+h//2-4}" class="box-text">{esc(l1)}</text>\n'
            f'            <text x="{ax}" y="{y+h//2+24}" class="box-text">{esc(l2)}</text>\n'
            f'        </g>')

def build_scene_02():
    b = []
    # ── the shared band ──────────────────────────────────────────────────────
    b.append('    <g id="section_common">')
    b.append('        <text id="heading_common" x="960" y="62" font-size="48" font-weight="bold"'
             ' class="text-primary" text-anchor="middle">Common Challenges</text>')
    for i, (ic, l1, l2) in enumerate(COMMON[:4]):
        b.append(chal_box(f"common_{i+1}", 200 + i*400, C_ROW_A_Y, C_BOX_W, C_BOX_H, ic, l1, l2))
    for i, (ic, l1, l2) in enumerate(COMMON[4:]):
        b.append(chal_box(f"common_{i+5}", 400 + i*400, C_ROW_B_Y, C_BOX_W, C_BOX_H, ic, l1, l2))
    b.append('    </g>\n')
    # ── the two columns ──────────────────────────────────────────────────────
    for gid, heading, hx, col_x, rows in (
            ("section_traditional", "Traditional Editors", TRAD_X + K_BOX_W//2, TRAD_X, TRADITIONAL),
            ("section_ai",          "AI-Generated Videos", AI_X   + K_BOX_W//2, AI_X,   AI)):
        b.append(f'    <g id="{gid}">')
        b.append(f'        <text id="heading_{gid.split("_")[1]}" x="{hx}" y="445" font-size="42"'
                 f' font-weight="bold" class="text-primary" text-anchor="middle">{esc(heading)}</text>')
        for i, (ic, l1, l2) in enumerate(rows):
            b.append(chal_box(f"{gid.split('_')[1]}_{i+1}", col_x, K_TOP_Y + i*K_PITCH,
                              K_BOX_W, K_BOX_H, ic, l1, l2))
        b.append('    </g>\n')
    used = [r[0] for r in COMMON + TRADITIONAL + AI]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg id="challenge" width="1920" height="1080" viewBox="0 0 1920 1080"'
            ' xmlns="http://www.w3.org/2000/svg">\n'
            '    <!-- Background -->\n'
            '    <rect width="1920" height="1080" class="canvas-bg"/>\n\n'
            '    <defs>\n' + scene2_style(used) + "\n\n" + symbols(used) + '\n    </defs>\n\n'
            + "\n".join(b) + '</svg>\n')

# ════════════════════════════════════════════════════════════════════════════
# SCENE 3 — the benefits
# ════════════════════════════════════════════════════════════════════════════
# ⚠️ 5-3-5. The side columns hold five and the centre three, and the centre's
# three align with rows 2-4 of the sides so the whole thing reads as one grid
# with two holes rather than as three unrelated stacks.
B_W, B_H, B_PITCH, B_TOP = 500, 140, 175, 210
LEFT_X, MID_X, RIGHT_X = 80, 710, 1340

LEFT = [   # production
    ("eye",           "Consistent Styling", "Unified Visuals"),
    ("square-ruler",  "Precision Control",  "Time and Space"),
    ("audio",         "Narration-Paced",    "Re-Record and It Re-Fits"),
    ("pattern",       "Pattern Reuse",      "Source Structure"),
    ("puzzle",        "Composable",         "Assemble Assets"),
]
MID = [    # what the language IS
    ("source-code",   "Declarative Code",   "What, Not How"),
    ("deterministic", "Deterministic",      "Same Source, Same Output"),
    ("aiagent",       "AI-Authorable",      "LLM Writes the Source"),
]
RIGHT = [  # workflow
    ("version",           "Version Control", "Diff-Friendly Text"),
    ("lightning",         "Fast Iterations", "Edit and Regenerate"),
    ("robotic-arm",       "Scalable",        "Automate Creation"),
    ("language",          "Localization",    "One Source, Many Languages"),
    ("desktop_computer",  "Renders Locally", "No LLM at Render Time"),
]

def scene3_style(used):
    return f"""        <style>
            /* ── Mapping only: class -> variable. The VALUES live in
                  ../style/theme_dark.css and ../style/theme_light.css. ───────
               Every var() carries the PAPER value as its fallback. ⚠️ GENERATED
               — see resource/temp/make_scenes.py. */

            .canvas-bg {{
                fill: {v('--scene-background-color')};
            }}

            /* The icon catalog's vocabulary — only the classes this scene's
               own glyphs carry. */
{icon_rules(used)}

            /* The thirteen benefit boxes. Unlike scene 02's pain-point boxes
               these take fill and stroke from ONE class, because no icon here
               reuses either half. */
            .benefit-box {{
                fill: {v('--box-fill-color')};
                stroke: {v('--box-stroke-color')};
                stroke-width: 2;
                rx: 8;
            }}

            /* Three ranks of text: the scene heading, the line under it, and
               each box's own title over its supporting line. */
            .heading-text {{
                fill: {v('--title-text-color')};
                font-family: {v('--diagram-font-family')};
                font-size: 72px;
                font-weight: 700;
                text-anchor: middle;
            }}

            .subheading-text {{
                fill: {v('--title-text-color')};
                font-family: {v('--diagram-font-family')};
                font-size: 48px;
                font-weight: 500;
                text-anchor: middle;
            }}

            .title-text {{
                fill: {v('--title-text-color')};
                font-family: {v('--diagram-font-family')};
                font-size: 36px;
                font-weight: 600;
                text-anchor: middle;
            }}

            .subtitle-text {{
                fill: {v('--detail-text-color')};
                font-family: {v('--diagram-font-family')};
                font-size: 26px;
                font-weight: 400;
                text-anchor: middle;
            }}
        </style>"""

def ben_box(gid, x, y, icon, title, sub):
    return (f'    <g id="{gid}" transform="translate({x}, {y})">\n'
            f'        <rect class="benefit-box" width="{B_W}" height="{B_H}"/>\n'
            f'        <use href="#{sid(icon)}" x="30" y="45" width="50" height="50"/>\n'
            f'        <text x="280" y="62" class="title-text">{esc(title)}</text>\n'
            f'        <text x="280" y="100" class="subtitle-text">{esc(sub)}</text>\n'
            f'    </g>')

def build_scene_03():
    b = ['    <g id="heading">',
         '        <text x="960" y="92" class="heading-text">The Better Way</text>',
         '        <text x="960" y="160" class="subheading-text">Storytelling with Kinaigraph</text>',
         '    </g>\n']
    for i, (ic, t, s_) in enumerate(LEFT):
        b.append(ben_box(f"left_{i+1}", LEFT_X, B_TOP + i*B_PITCH, ic, t, s_))
    b.append("")
    for i, (ic, t, s_) in enumerate(MID):
        b.append(ben_box(f"center_{i+1}", MID_X, B_TOP + (i+1)*B_PITCH, ic, t, s_))
    b.append("")
    for i, (ic, t, s_) in enumerate(RIGHT):
        b.append(ben_box(f"right_{i+1}", RIGHT_X, B_TOP + i*B_PITCH, ic, t, s_))
    used = [r[0] for r in LEFT + MID + RIGHT]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg id="benefits" width="1920" height="1080" viewBox="0 0 1920 1080"'
            ' xmlns="http://www.w3.org/2000/svg">\n'
            '    <!-- Background -->\n'
            '    <rect width="1920" height="1080" class="canvas-bg"/>\n\n'
            '    <defs>\n' + scene3_style(used) + "\n\n" + symbols(used) + '\n    </defs>\n\n'
            + "\n".join(b) + '\n</svg>\n')

if __name__ == "__main__":
    out2 = HERE / "resource/scene/scene_02_challenge.svg"
    out3 = HERE / "resource/scene/scene_03_benefits.svg"
    out2.write_text(build_scene_02())
    out3.write_text(build_scene_03())
    print(f"wrote {out2.relative_to(HERE)}  ({len(COMMON)+len(TRADITIONAL)+len(AI)} boxes)")
    print(f"wrote {out3.relative_to(HERE)}  ({len(LEFT)+len(MID)+len(RIGHT)} boxes)")
    print(f"  scene 2 last column box ends at y={K_TOP_Y + 3*K_PITCH + K_BOX_H}")
    print(f"  scene 3 last column box ends at y={B_TOP + 4*B_PITCH + B_H}")
