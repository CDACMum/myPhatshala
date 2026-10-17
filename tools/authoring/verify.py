#!/usr/bin/env python3
"""Verify a generated lesson page.
usage: verify.py SITE_ROOT REL_LESSON_DIR [--shots]
Checks: JSON blocks parse; quiz answers valid; anim frames == caption count;
every Java program (code blocks with 'class Main', runner tasks, tracer) compiles/runs;
printed outputs match the page; browser checks (no JS errors, no horizontal scroll).
Runner task extra keys: "_expect": "ok" (default) | "compile-error" | "exception";  "_stdin": "text"
Code block attrs: data-check="skip" to skip output comparison (machine-dependent output); data-run="skip" for multi-file snippets.
"""
import sys, os, re, json, html, subprocess, tempfile, asyncio

root, rel = sys.argv[1], sys.argv[2].strip('/')
shots = '--shots' in sys.argv
SHOTS = os.environ.get('MPSHOTS', '/tmp/mpshots')
page = os.path.join(root, rel, 'index.html')
s = open(page, encoding='utf-8').read()
ok = True
def bad(msg):
    global ok; ok = False; print('  ✗', msg)

env = dict(os.environ, JAVA_TOOL_OPTIONS='')
def run_java(code, stdin='', fname=None):
    d = tempfile.mkdtemp(prefix='mpj')
    cls = re.search(r'public\s+(?:final\s+)?class\s+(\w+)', code)
    name = fname or (cls.group(1) if cls else 'Main')
    open(os.path.join(d, name + '.java'), 'w').write(code)
    c = subprocess.run(['javac', '-Xlint:-options', name + '.java'], cwd=d, capture_output=True, text=True, env=env)
    cerr = c.stderr.replace('Picked up JAVA_TOOL_OPTIONS: \n', '')
    if c.returncode != 0: return 'compile-error', cerr
    r = subprocess.run(['java', name], cwd=d, input=stdin, capture_output=True, text=True, env=env, timeout=30)
    err = r.stderr.replace('Picked up JAVA_TOOL_OPTIONS: \n', '')
    return ('ok' if r.returncode == 0 else 'exception'), r.stdout + (('\n' + err) if r.returncode else '')

def text_of(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h))

# JSON blocks
blocks = []
for m in re.finditer(r'<script type="application/json">(.*?)</script>', s, re.S):
    try: blocks.append(json.loads(m.group(1)))
    except Exception as ex: bad(f'JSON parse: {ex}')
runner = [b for b in blocks if isinstance(b, dict) and 'tasks' in b]
tracer = [b for b in blocks if isinstance(b, dict) and 'steps' in b]
quiz = [b for b in blocks if isinstance(b, list)]
for q in (quiz[0] if quiz else []):
    if not (0 <= q['answer'] < len(q['options'])): bad('quiz answer index: ' + q['q'])
print(f'  quiz {len(quiz[0]) if quiz else 0} Qs, runner tasks {sum(len(r["tasks"]) for r in runner)}, tracers {len(tracer)}')
if not quiz or not (6 <= len(quiz[0]) <= 8): bad('quiz must have 6-8 questions')
n_scn = s.count('<article class="scn">')
if not 4 <= n_scn <= 6: bad(f'scenarios count {n_scn}')
n_prob = s.count('<article class="prob">')
if n_prob and not 5 <= n_prob <= 15: bad(f'practice problems count {n_prob}')
if n_prob: print(f'  practice problems {n_prob}')

# anim frames vs captions
for part in s.split('<div class="anim" data-frames="')[1:]:
    n = int(part[:part.index('"')]); seg = part[:part.index('</section>')]
    for caps in re.findall(r'<ol class="caps" hidden>(.*?)</ol>', seg, re.S):
        k = caps.count('<li>')
        if k != n: bad(f'anim frames {n} but captions {k}')
    for on in re.findall(r'data-on="([^"]+)"', seg):
        for piece in on.split(','):
            for v in re.findall(r'\d+', piece):
                if not 1 <= int(v) <= n: bad(f'data-on {on} outside 1..{n}')

for m in re.finditer(r'<[^>]*data-on="[^"]*"[^>]*>', s):
    if re.search(r'style="[^"]*(?<!fill-)(?<!stroke-)opacity', m.group(0)) or re.search(r'\sopacity="', m.group(0)):
        bad('data-on element has its own opacity (breaks show/hide): ' + m.group(0)[:90])

# code blocks
for m in re.finditer(r'<div class="code" data-lang="java"([^>]*)><pre><code>(.*?)</code></pre>(?:<div class="output">(.*?)</div>)?', s, re.S):
    attrs, code, out = m.group(1), html.unescape(m.group(2)), m.group(3)
    if 'class ' not in code or 'main' not in code or 'data-run="skip"' in attrs: continue
    sm = re.search(r'data-stdin="([^"]*)"', attrs)
    stdin = html.unescape(sm.group(1)).replace('\\n', '\n') if sm else ''
    st, got = run_java(code, stdin)
    exp_err = 'data-expect="compile-error"' in attrs
    if exp_err:
        if st != 'compile-error': bad('code block expected compile error')
        continue
    if 'data-expect="exception"' in attrs:
        if st != 'exception': bad('code block expected exception')
    elif st != 'ok': bad(f'code block {st}: {got[:300]}'); continue
    if out is not None and 'data-check="skip"' not in attrs:
        if text_of(out).strip() != got.strip(): bad(f'output mismatch\n--- page:\n{text_of(out).strip()}\n--- real:\n{got.strip()}')
for r in runner:
    for t in r['tasks']:
        st, got = run_java(t['code'], t.get('_stdin', ''), r.get('file','Main.java')[:-5])
        exp = t.get('_expect', 'ok')
        if st != exp: bad(f'runner "{t["label"]}": expected {exp}, got {st}: {got[:300]}')
for t in tracer:
    code = '\n'.join(t['code'])
    if 'class ' in code and 'main' in code:
        st, got = run_java(code, t.get('_stdin', ''))
        want = ''.join(x.get('out', '') for x in t['steps'])
        if t.get('_expect', 'ok') != st: bad(f'tracer program {st}: {got[:200]}')
        elif got.split('\nException')[0].strip() != want.strip() and not t.get('_nocheck'):
            bad(f'tracer output mismatch\n--- tracer:\n{want}\n--- real:\n{got}')
    for x in t['steps']:
        ln = x['line']; L = len(t['code'])
        for v in (ln if isinstance(ln, list) else [ln]):
            if not 1 <= v <= L: bad(f'tracer line {v} out of range')

# browser
from playwright.async_api import async_playwright
URL = 'http://localhost:8765/' + rel + '/'
# flags visible inline text (code, b, small, a, span) whose colour is too close to its effective background
CONTRAST_JS = r'''() => {
 const rgb = s => { const n=(s.match(/[\d.]+/g)||[]).map(Number); if(s.startsWith('color(')){ const a=n.slice(0,3).map(v=>v*255); if(n.length>3)a.push(n[3]); return a;} return n; };
 const lum = c => { const a=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}); return .2126*a[0]+.7152*a[1]+.0722*a[2]; };
 const bgOf = el => { for(let e=el;e;e=e.parentElement){ const c=rgb(getComputedStyle(e).backgroundColor); if(c.length>=3 && (c.length<4||c[3]>0.5)) return c; } return [255,255,255]; };
 const out=[];
 document.querySelectorAll('main code, main b, main strong, main small, main a, main em, main p, main li').forEach(el=>{
   if(el.closest('svg,.anim,pre,[hidden]')||!el.offsetParent||!el.textContent.trim()) return;
   const f=rgb(getComputedStyle(el).color), b=bgOf(el);
   const L1=lum(f),L2=lum(b), r=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
   if(r<2.8) out.push(el.tagName+':'+el.textContent.trim().slice(0,20)+' '+r.toFixed(2));
 });
 return out; }'''
async def browse():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, t in [(1280, 'light'), (1280, 'dark'), (390, 'light'), (390, 'dark')]:
            pg = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=t)
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(500)
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            if sw > w: bad(f'horizontal scroll at {w} {t}: {sw}')
            if errs: bad(f'JS errors {w} {t}: {errs}')
            lowc = await pg.evaluate(CONTRAST_JS)
            if lowc: bad(f'low-contrast text {w} {t}: {lowc[:5]}')
            if shots and (w, t) in [(1280, 'dark'), (390, 'light')]:
                tag = f'{w}{t[0]}'
                if await pg.locator('.scene').count():
                    await pg.locator('.scene').first.screenshot(path=f'{SHOTS}/scene_{tag}.png')
                a = pg.locator('.anim').first
                await a.scroll_into_view_if_needed(); await a.locator('[data-a=reset]').click()
                n = int(await a.get_attribute('data-frames'))
                for f in range(1, n + 1):
                    await pg.wait_for_timeout(900)
                    await a.locator('.anim__views').screenshot(path=f'{SHOTS}/anim_{tag}_{f}.png')
                    if f < n: await a.locator('[data-a=next]').click()
            await pg.close()
        await b.close()
os.makedirs(SHOTS, exist_ok=True)
if shots:
    for f in os.listdir(SHOTS): os.remove(SHOTS + '/' + f)
asyncio.run(browse())
if shots:
    from PIL import Image
    for tag in ['1280d', '390l']:
        fs = sorted([f for f in os.listdir(SHOTS) if f.startswith(f'anim_{tag}_')], key=lambda x: int(x.split('_')[-1][:-4]))
        if not fs: continue
        ims = [Image.open(SHOTS + '/' + f) for f in fs]
        if tag == '1280d':  # grid 2 columns
            W = ims[0].width; H = max(i.height for i in ims); rows = (len(ims) + 1) // 2
            c = Image.new('RGB', (W * 2, H * rows), 'white')
            for i, im in enumerate(ims): c.paste(im, ((i % 2) * W, (i // 2) * H))
            c = c.resize((c.width * 6 // 10, c.height * 6 // 10))
        else:
            W = sum(i.width for i in ims); H = max(i.height for i in ims)
            c = Image.new('RGB', (W, H), 'white'); x = 0
            for im in ims: c.paste(im, (x, 0)); x += im.width
            c = c.resize((c.width // 2, c.height // 2))
        c.save(f'{SHOTS}/ALL_{tag}.png'); print('  shots ' + SHOTS + '/ALL_' + tag + '.png', c.size)
print('  RESULT:', 'PASS' if ok else 'FAIL')
