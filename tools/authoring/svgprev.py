#!/usr/bin/env python3
"""Render every inline SVG of a lesson page to PNG (light theme) for visual checking, frame by frame.
usage: svgprev.py PAGE.html OUT_DIR
Animations become one sheet: one row per frame, one column per view. Needs ImageMagick `convert` and Pillow."""
import sys, os, re, subprocess, tempfile
TMP = tempfile.mkdtemp(prefix='svgprev_')
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
VARS = {'paper': '#F5FAF7', 'paper-2': '#E9F3EE', 'card': '#FFFFFF', 'ink': '#1B2433', 'ink-2': '#4A5568', 'ink-3': '#7A8496',
        'line': '#D5E6DD', 'green': '#2F7D5B', 'red': '#D64545', 'green-soft': '#DDEFE6', 'blue': '#2E5AAC', 'blue-soft': '#E1E9F7',
        'board': '#1F2B26', 'chalk': '#EDEBE3', 'saffron-soft': '#FCE6D6', 'violet': '#6B4FBB', 'violet-soft': '#ECE6FA'}
CLS = {'s-card': 'fill:var(--paper-2);stroke:var(--line);stroke-width:1.5', 's-card2': 'fill:var(--card);stroke:var(--line);stroke-width:1.5',
       's-board': 'fill:var(--board)', 's-ink': 'fill:var(--ink)', 's-ink2': 'fill:var(--ink-2)', 's-ink3': 'fill:var(--ink-3)',
       's-chalk': 'fill:#EDEBE3', 's-kw': 'fill:#F5A15C', 's-str': 'fill:#9FD3B8', 's-acc': 'fill:var(--track)',
       's-acc-stroke': 'stroke:var(--track);fill:none;stroke-width:2.5', 's-green': 'fill:var(--green)', 's-blue': 'fill:var(--blue)',
       's-red': 'fill:#D64545', 's-wire': 'stroke:var(--line);stroke-width:2.5;fill:none;stroke-dasharray:5 5',
       's-line': 'stroke:var(--ink-3);stroke-width:1.5;fill:none', 's-soft-green': 'fill:var(--green-soft)',
       's-soft-blue': 'fill:var(--blue-soft)', 's-soft-acc': 'fill:var(--saffron-soft)', 's-violet': 'fill:var(--violet)', 's-soft-violet': 'fill:var(--violet-soft)', 's-wm': 'fill:var(--ink-3);opacity:.35;font-size:9px'}


def in_range(spec, f):
    for part in spec.split(','):
        a, _, b = part.partition('-')
        lo = int(a); hi = lo if '-' not in part else (10 ** 6 if b == '' else int(b))
        if lo <= f <= hi: return True
    return False


def resolve(v, track):
    v = re.sub(r'color-mix\(in srgb,\s*([^ ]+) (\d+)%,[^)]*\)', lambda m: m.group(1), v)
    v = v.replace('var(--track,#E8772E)', track).replace('var(--track)', track)
    return re.sub(r'var\(--([\w-]+)\)', lambda m: VARS.get(m.group(1), '#888'), v)


def flatten(el, track, frame, inherit_mono=False):
    for ch in list(el):
        on = ch.get('data-on')
        if on and frame is not None and not in_range(on, frame):
            el.remove(ch); continue
        if on and frame is None and on not in ('1', '1-') and not on.startswith('1-') and not in_range(on, 1):
            el.remove(ch); continue
        pos = ch.get('data-pos')
        if pos and frame:
            import json
            p = None
            for k, val in sorted(json.loads(pos).items(), key=lambda x: int(x[0])):
                if int(k) <= frame: p = val
            if p: ch.set('transform', f'translate({p})')
        style = ''
        mono = inherit_mono
        for c in (ch.get('class') or '').split():
            if c in CLS: style += CLS[c] + ';'
            if c == 'mono': mono = True
        style += ch.get('style') or ''
        for decl in style.split(';'):
            if ':' in decl:
                k, v = [x.strip() for x in decl.split(':', 1)]
                ch.set(k, resolve(v, track))
        for a in ('class', 'style', 'data-on', 'data-pos'):
            ch.attrib.pop(a, None)
        tag = ch.tag.split('}')[-1]
        if tag in ('text', 'tspan', 'g'):
            ch.set('font-family', 'DejaVu Sans Mono' if mono else 'DejaVu Sans')
        flatten(ch, track, frame, mono)


def render(svg_src, track, frame, out):
    root = ET.fromstring(svg_src)
    flatten(root, track, frame)
    vb = [float(x) for x in root.get('viewBox').split()]
    root.set('width', str(int(vb[2] * 2))); root.set('height', str(int(vb[3] * 2)))
    bg = ET.Element(f'{{{NS}}}rect', {'x': str(vb[0]), 'y': str(vb[1]), 'width': str(vb[2]), 'height': str(vb[3]), 'fill': '#FFFFFF'})
    root.insert(0, bg)
    tmp = os.path.join(TMP, 'prev.svg')
    open(tmp, 'w').write(ET.tostring(root, encoding='unicode'))
    try:
        import cairosvg  # used when available (faster, more faithful); ImageMagick otherwise
        cairosvg.svg2png(url=tmp, write_to=out); os.remove(tmp); return
    except ImportError:
        pass
    r = subprocess.run(['convert', 'msvg:' + tmp, out], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit('render failed: ' + r.stderr[:300])
    os.remove(tmp)


def main():
    page, outd = sys.argv[1], sys.argv[2]
    os.makedirs(outd, exist_ok=True)
    s = open(page, encoding='utf-8').read()
    track = re.search(r'--track:(#[0-9A-Fa-f]{6})', s).group(1)
    s = re.sub(r'<script type="application/json">.*?</script>', '', s, flags=re.S)
    # animations
    n = 0
    for m in re.finditer(r'<div class="anim[^"]*" data-frames="(\d+)".*?</div>\s*</div>\s*</div>', s, re.S):
        n += 1
        frames = int(m.group(1))
        svgs = re.findall(r'<svg.*?</svg>', m.group(0), re.S)
        rows = []
        for f in range(1, frames + 1):
            ims = []
            for k, sv in enumerate(svgs):
                p = os.path.join(TMP, f'a{n}_{f}_{k}.png'); render(sv, track, f, p); ims.append(Image.open(p))
            rows.append(ims)
        w = sum(i.width for i in rows[0]) + 10 * (len(rows[0]) + 1); h = sum(r[0].height for r in rows) + 10 * (frames + 1)
        sheet = Image.new('RGB', (w, h), '#999999'); y = 10
        for f, r in enumerate(rows, 1):
            x = 10
            for im in r: sheet.paste(im, (x, y)); x += im.width + 10
            ImageDraw.Draw(sheet).text((12, y + 2), str(f), fill='#000')
            y += r[0].height + 10
        sheet.save(os.path.join(outd, f'anim{n}.png'))
        s = s.replace(m.group(0), '')
    # remaining static svgs (scenes, use-case art); skip tiny icons
    k = 0
    for sv in re.findall(r'<svg viewBox="0 0 (\d+) (\d+)".*?</svg>', s, re.S):
        pass
    for mm in re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)"[^>]*>.*?</svg>', s, re.S):
        if int(mm.group(1)) <= 64: continue
        k += 1
        render(mm.group(0), track, None, os.path.join(outd, f'static{k}.png'))
    print('rendered', n, 'animations and', k, 'static pictures into', outd)


if __name__ == '__main__':
    main()
