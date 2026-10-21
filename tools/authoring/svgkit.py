"""Small helpers for writing lesson animations (authoring time only).

A lesson's build script (src/.../<lesson>/_body.py) imports this, assembles body.html
with real-time scenario animations, and writes the file. pylesson.py then reads body.html.
"""
import html as _html

E = _html.escape
TONES = {
    'blue': ('s-soft-blue', 'var(--blue)'), 'green': ('s-soft-green', 'var(--green)'),
    'acc': ('s-soft-acc', 'var(--track)'), 'red': ('s-soft-acc', '#D64545'),
    'amber': ('s-soft-acc', '#E0A100'), 'violet': ('s-soft-violet', 'var(--violet)'),
    'card': ('s-card2', 'var(--line)'),
}
FILL = {'blue': 'var(--blue)', 'green': 'var(--green)', 'acc': 'var(--track)', 'red': '#D64545',
        'amber': '#E0A100', 'violet': 'var(--violet)', 'grey': 'var(--line)', 'ink': 'var(--ink)'}
TXT = {'blue': 's-blue', 'green': 's-green', 'acc': 's-acc', 'red': 's-red', 'violet': 's-violet',
       'ink': 's-ink', 'ink2': 's-ink2', 'ink3': 's-ink3', 'amber': 's-acc'}


def t(x, y, s, size=9, cls='ink', anchor='middle', bold=False, mono=False, extra=''):
    import re as _re
    s = _re.sub(r'&(?![a-zA-Z#][a-zA-Z0-9]*;)', '&amp;', str(s))
    s = _re.sub(r'<(?=[\s=\d])', '&lt;', s)
    c = TXT.get(cls, cls) + (' mono' if mono else '')
    w = ' font-weight="700"' if bold else ''
    a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
    return f'<text x="{x}" y="{y}"{a} font-size="{size}"{w} class="{c}"{extra}>{s}</text>'


def box(x, y, w, h, tone='card', rx=6, sw=None):
    cls, st = TONES[tone]
    s = f';stroke-width:{sw}' if sw else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}" style="stroke:{st}{s}"/>'


def fill(x, y, w, h, color='acc', rx=4, opacity=None):
    o = f';opacity:{opacity}' if opacity is not None else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="fill:{FILL.get(color, color)}{o}"/>'


def label_box(x, y, w, h, lines, tone='card', size=9, bold_first=True, cls='ink'):
    """A box with 1-3 centred lines of text."""
    out = box(x, y, w, h, tone)
    n = len(lines)
    lh = size + 4
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, ln in enumerate(lines):
        out += t(x + w / 2, round(y0 + i * lh, 1), ln, size if i == 0 else size - 0.6,
                 cls if i == 0 else 'ink2', bold=(bold_first and i == 0))
    return out


def arrow(x1, y1, x2, y2, color='ink3', w=1.8, dash=False):
    import math
    c = FILL.get(color, 'var(--line)') if color != 'ink3' else 'var(--line)'
    if color == 'ink3':
        c = '#8A94A0'
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - 7 * math.cos(ang - 0.45), y2 - 7 * math.sin(ang - 0.45)
    hx2, hy2 = x2 - 7 * math.cos(ang + 0.45), y2 - 7 * math.sin(ang + 0.45)
    d = ';stroke-dasharray:4 3' if dash else ''
    return (f'<path d="M{x1} {y1}L{x2} {y2}" style="fill:none;stroke:{c};stroke-width:{w}{d}"/>'
            f'<path d="M{round(hx1,1)} {round(hy1,1)}L{x2} {y2}L{round(hx2,1)} {round(hy2,1)}" style="fill:none;stroke:{c};stroke-width:{w}"/>')


def cap(l1, l2='', tone='blue', y=170, h=44, w=340, x=10):
    """The explanation strip at the bottom of a one-view frame."""
    out = box(x, y, w, h, tone)
    import re as _re
    for ln, sz in ((l1, 9.4), (l2, 8.8)):
        plain = _re.sub(r'<[^>]+>', '', ln)
        if len(plain) * sz * (0.6 if ln is l1 else 0.53) > w - 8:
            print('WARN caption too wide:', plain)
    if l2:
        out += t(x + w / 2, y + h / 2 - 3, l1, 9.4, bold=True) + t(x + w / 2, y + h / 2 + 12, l2, 8.8, 'ink2')
    else:
        out += t(x + w / 2, y + h / 2 + 3, l1, 9.4, bold=True)
    return out


def frame(i, content):
    return f'<g data-on="{i}">{content}</g>'


def bars(rows, x=120, y=36, w=190, h=14, gap=22, label_x=14, value_x=348):
    """rows: [(label, percent, color, right_text)]"""
    out = ''
    for k, (lab, p, col, rt) in enumerate(rows):
        yy = y + k * gap
        out += t(label_x, yy + 11, lab, 8.8, anchor='start')
        out += f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="4" class="s-card2"/>'
        ww = round(w * min(p, 100) / 100)
        if ww:
            out += fill(x, yy, ww, h, col)
        out += t(value_x, yy + 11, rt, 8.6, 'ink', anchor='end', bold=True)
    return out


WM1 = '<text x="354" y="221" text-anchor="end" class="s-wm">myphatshala.in</text>'
WM2 = '<text x="352" y="244" text-anchor="end" class="s-wm">myphatshala.in</text>'


def anim_one(badge, title, intro, panel_title, aria, frames, caps, delay=5000, hid=None, static=''):
    n = len(frames)
    assert n == len(caps), (title, n, len(caps))
    body = static + ''.join(frame(i + 1, f) for i, f in enumerate(frames))
    lis = '\n'.join(f'          <li>{c}</li>' for c in caps)
    idattr = f' id="{hid}"' if hid else ''
    return f'''
  <span class="live">{badge}</span>
  <h3{idattr}>{title}</h3>
  <p class="anim-intro">{intro}</p>
  <div class="anim anim--one" data-frames="{n}" data-delay="{delay}">
    <div class="anim__title">{panel_title} <span>{n} steps</span></div>
    <div class="anim__views">
      <div class="view view--story">
        <span class="view__tag">Animated example</span>
        <svg viewBox="0 0 360 226" role="img" aria-label="{E(aria)}">
          {body}
          {WM1}
        </svg>
        <ol class="caps" hidden>
{lis}
        </ol>
      </div>
    </div>
  </div>
'''


def anim_two(title, panel, see_aria, behind_aria, see_frames, behind_frames, see_caps, behind_caps,
             see_static='', behind_static=''):
    n = len(see_frames)
    assert n == len(behind_frames) == len(see_caps) == len(behind_caps), title
    sf = see_static + ''.join(frame(i + 1, f) for i, f in enumerate(see_frames))
    bf = behind_static + ''.join(frame(i + 1, f) for i, f in enumerate(behind_frames))
    l1 = '\n'.join(f'          <li>{c}</li>' for c in see_caps)
    l2 = '\n'.join(f'          <li>{c}</li>' for c in behind_caps)
    return f'''  <div class="anim" data-frames="{n}">
    <div class="anim__title">{panel} <span>{n} steps</span></div>
    <div class="anim__views">
      <div class="view view--see">
        <span class="view__tag">What you see</span>
        <svg viewBox="0 0 360 250" role="img" aria-label="{E(see_aria)}">
          {sf}
          {WM2}
        </svg>
        <ol class="caps" hidden>
{l1}
        </ol>
      </div>
      <div class="view view--behind">
        <span class="view__tag">Behind the screen</span>
        <svg viewBox="0 0 360 250" role="img" aria-label="{E(behind_aria)}">
          {bf}
          {WM2}
        </svg>
        <ol class="caps" hidden>
{l2}
        </ol>
      </div>
    </div>
  </div>
'''


def scene(aria, content, caption):
    return f'''    <div class="scene">
      <svg viewBox="0 0 640 170" role="img" aria-label="{E(aria)}">
        {content}
        <text x="320" y="158" text-anchor="middle" font-size="10.5" class="s-ink2">{caption}</text>
        <text x="632" y="168" text-anchor="end" class="s-wm">myphatshala.in</text>
      </svg>
    </div>'''


def table(head, rows, minw=560, cls='compare'):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'''  <div class="table-wrap">
  <table class="{cls}" style="min-width:{minw}px">
    <thead><tr>{th}</tr></thead>
    <tbody>{tr}</tbody>
  </table>
  </div>'''


def facts(rows):
    return '  <table class="facts">\n' + '\n'.join(f'    <tr><th>{a}</th><td>{b}</td></tr>' for a, b in rows) + '\n  </table>'


def terms(rows):
    return '  <div class="terms">\n' + '\n'.join(f'    <div class="term"><b>{a}</b><span>{b}</span></div>' for a, b in rows) + '\n  </div>'


def cards(rows):
    return '  <div class="cards">\n' + '\n'.join(f'    <div class="card"><h4>{a}</h4><p>{b}</p><span class="tag">{c}</span></div>' for a, b, c in rows) + '\n  </div>'


def stepper(steps):
    """steps: [(title, html_inner, behind)]"""
    out = '  <ol class="stepper">\n'
    for ti, inner, behind in steps:
        out += f'    <li><h4>{ti}</h4>\n      {inner}\n      <span class="behind">{behind}</span></li>\n'
    return out + '  </ol>'


def code(lang, file, src, output=None):
    o = f'<div class="output">{E(output)}</div>' if output is not None else ''
    return f'<div class="code" data-lang="{lang}" data-file="{file}"><pre><code>{E(src)}</code></pre>{o}</div>'


def usecase(art, title, text, flow):
    f = '<i>→</i>'.join(f'<span class="java">{x[1:]}</span>' if x.startswith('*') else f'<span>{x}</span>' for x in flow)
    return f'''  <div class="usecase">
    <div class="uc-art"><svg viewBox="0 0 120 90">{art}</svg></div>
    <div><h4>{title}</h4>
      <p>{text}</p>
      <div class="uc-flow">{f}</div></div>
  </div>'''


def def_block(formal, simple):
    return f'''  <div class="def">
    <div class="def__formal"><small>Formal definition (write this in exams)</small>
      <p>{formal}</p></div>
    <div class="def__simple"><small>In simple words</small>
      <p>{simple}</p></div>
  </div>'''


def part(n, pid, label, h2, inner):
    return f'''<!-- ======================= PART {n} ======================= -->
<section class="part" id="{pid}">
  <span class="part-label"><b>{n}</b> {label}</span>
  <h2>{h2}</h2>
{inner}
</section>
'''


def scn(tag, level, title, situation, look, answer, avoid):
    return f'''    <article class="scn">
      <div class="scn__head"><span class="scn__tag">{tag}</span><span class="scn__tag scn__tag--level">{level}</span></div>
      <h4>{title}</h4>
      <p class="scn__situation">{situation}</p>
      <p class="scn__look"><b>The interviewer is checking:</b> {look}</p>
      <details><summary>Show a strong answer</summary><div class="scn__answer">
        {answer}
        <p class="scn__avoid"><b>Avoid:</b> {avoid}</p>
      </div></details>
    </article>
'''


def run_code(src):
    """Run Python and return its stdout (for outputs shown inside the stepper)."""
    import subprocess, sys
    p = subprocess.run([sys.executable, '-c', src], capture_output=True, text=True, timeout=30)
    if p.returncode:
        raise SystemExit(p.stderr)
    return p.stdout.rstrip('\n')
