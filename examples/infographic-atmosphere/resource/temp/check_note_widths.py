#!/usr/bin/env python3
"""Fails if any callout line is too wide for its box.

    python3 resource/temp/check_note_widths.py

⛔ THE RENDER CANNOT TELL YOU THIS. A line too wide for the box WRAPS, and the
overflow is dropped without a word — so the frame shows a callout that looks
deliberate and says half of what was written. Counting the rendered lines does
not catch it either: a two-line note whose second line wraps still renders two
bands, the second being the first half of a sentence that now ends mid-word.

⚡ So the check is ARITHMETIC, not pixels: measure each line in the same font at
the same size and compare against the box's inner width. Chrome does the
measuring because it is what renders the video.
"""
import html, json, os, pathlib, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent.parent.parent
CHROME = os.environ.get("KINAIGRAPH_BROWSER",
                        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

def note_lines(doc):
    """Every callout line in a document, with the box geometry it must fit."""
    s = doc.read_text()
    def const(name):
        m = re.search(rf'^\s+{name}: (\d+)', s, re.M)
        assert m, f'{doc.name}: no {name}'
        return int(m.group(1))
    inner = const('NOTE_W') - 2 * const('NOTE_PAD')
    size = int(re.search(r'font_size: (\d+)', s).group(1))
    family = re.search(r'font_family: \'([^\']+)\'', s).group(1)
    out = []
    for name, body in re.findall(
            r'(\w+_text):\n            type: "text"\n            content: \|\n'
            r'((?:                [^\n]*\n)+)', s):
        for line in body.rstrip('\n').split('\n'):
            out.append((name, line[16:]))   # strip the YAML block indent only
    return out, inner, size, family

def measure(lines, size, family):
    svg = ''.join(
        f'<text class="n" y="{40 * (i + 1)}" xml:space="preserve">{html.escape(t)}</text>'
        for i, t in enumerate(lines))
    page = (f'<!doctype html><html><body style="margin:0">'
            f'<svg width="2000" height="{40 * len(lines) + 40}" xmlns="http://www.w3.org/2000/svg">'
            f'<style>.n{{font-family:{family};font-size:{size}px;white-space:pre}}</style>{svg}</svg>'
            '<script>const r=[];document.querySelectorAll("text")'
            '.forEach(t=>r.push(t.getBBox().width.toFixed(0)));'
            'document.title="W::"+r.join(",")</script></body></html>')
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(page)
        path = f.name
    dom = subprocess.run([CHROME, '--headless', '--disable-gpu',
                          '--virtual-time-budget=3000', '--dump-dom', f'file://{path}'],
                         capture_output=True, text=True).stdout
    os.unlink(path)
    m = re.search(r'W::([\d,]+)', dom)
    assert m, 'the browser returned no measurements'
    return [int(x) for x in m.group(1).split(',') if x]

bad = 0
for doc in sorted(HERE.glob('scene_01_*.yaml')):
    lines, inner, size, family = note_lines(doc)
    widths = measure([t for _, t in lines], size, family)
    print(f'{doc.name}  — inner width {inner}px, {size}px type')
    for (name, text), w in zip(lines, widths):
        over = w > inner
        bad += over
        mark = '  ⛔ OVERFLOWS — it will wrap and the remainder is dropped' if over else ''
        print(f'    {w:4d}px  {name:20s} {text.strip()[:44]!r}{mark}')
print(f'\n{bad} overflowing line(s)')
sys.exit(1 if bad else 0)
