#!/usr/bin/env python3
"""Small helper for writing one-view "animated example" blocks (story animations) in Python.

    from mkanim import Anim
    a = Anim("Paying a canteen bill with UPI", frames=5)
    a.box(20, 40, 120, 50, "Riya's phone", fill="soft-blue", stroke="blue")
    a.text(80, 120, "₹60 sent", on="2-", cls="green", bold=True, anchor="middle")
    a.arrow(140, 65, 300, 65, on="2-", color="track")
    a.token(150, 52, 70, 26, "₹60", pos={1: "0,0", 2: "150,0"}, fill="soft-acc", stroke="track")
    a.caps(["caption frame 1", "...", ...])        # one per frame, html allowed
    html = a.html()

Elements with on="2-4" | "3" | "2,5" | "3-" show only on those frames; pos moves an element per frame.
Colours are theme-aware (light/dark): fill = card|card2|board|soft-blue|soft-green|soft-acc|none,
stroke/colour = blue|green|track|red|line|ink, text cls = ink|ink2|ink3|chalk|kw|str|acc|green|blue|red.
"""
import html as _h, math

STROKE = {'blue': 'var(--blue)', 'green': 'var(--green)', 'track': 'var(--track)', 'red': '#D64545',
          'line': 'var(--line)', 'ink': 'var(--ink-3)', 'ink2': 'var(--ink-2)'}
FILL = {'card': 's-card', 'card2': 's-card2', 'board': 's-board', 'soft-blue': 's-soft-blue',
        'soft-green': 's-soft-green', 'soft-acc': 's-soft-acc'}


def _a(on=None, pos=None, extra=''):
    s = ''
    if on: s += f' data-on="{on}"'
    if pos: s += " data-pos='" + '{' + ','.join(f'"{k}":"{v}"' for k, v in pos.items()) + "}'"
    return s + extra


class Anim:
    def __init__(self, title, frames, w=360, h=240, tag='Animated example', label=None, delay=4600):
        self.title, self.frames, self.w, self.h, self.tag = title, frames, w, h, tag
        self.label = label or title
        self.delay = delay
        self.out, self._caps, self._stack = [], [], []

    def _emit(self, s):
        self.out.append('  ' * (len(self._stack) + 5) + s)

    # ---- grouping -------------------------------------------------------
    class _G:
        def __init__(self, a, on, pos):
            self.a, self.on, self.pos = a, on, pos
        def __enter__(self):
            self.a._emit(f'<g{_a(self.on, self.pos)}>'); self.a._stack.append(1); return self.a
        def __exit__(self, *x):
            self.a._stack.pop(); self.a._emit('</g>')

    def g(self, on=None, pos=None):
        return Anim._G(self, on, pos)

    # ---- shapes ---------------------------------------------------------
    def box(self, x, y, w, h, label=None, fill='card2', stroke='line', on=None, pos=None, rx=8,
            size=11, cls='ink', bold=False, mono=False, sub=None, sw=1.5, pulse=False):
        f = FILL.get(fill, '')
        st = f'stroke:{STROKE.get(stroke, stroke)};stroke-width:{sw}' + (';fill:none' if fill == 'none' else '')
        inner = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{f}" style="{st}"/>'
        if label is not None:
            ty = y + h / 2 + size * 0.36 - (size * 0.62 if sub else 0)
            inner += self._t(x + w / 2, ty, label, cls, size, 'middle', bold, mono)
            if sub:
                inner += self._t(x + w / 2, ty + size * 1.3, sub, 'ink2', size - 1.5, 'middle', False, mono)
        cl = ' class="pulse"' if pulse else ''
        self._emit(f'<g{cl}{_a(on, pos)}>{inner}</g>' if (on or pos or pulse) else inner)

    def _t(self, x, y, s, cls, size, anchor, bold, mono):
        c = f's-{cls}' + (' mono' if mono else '')
        b = ' font-weight="700"' if bold else ''
        a = f' text-anchor="{anchor}"' if anchor != 'start' else ''
        return f'<text x="{x:g}" y="{y:g}" font-size="{size}"{a}{b} class="{c}">{s}</text>'

    def text(self, x, y, s, on=None, cls='ink', size=11, anchor='start', bold=False, mono=False, pos=None):
        t = self._t(x, y, s, cls, size, anchor, bold, mono)
        if on or pos: t = t.replace('<text ', f'<text{_a(on, pos)} ', 1)
        self._emit(t)

    def lines(self, x, y, rows, on=None, cls='ink', size=11, gap=None, anchor='start', mono=False, bold=False):
        gap = gap or size * 1.45
        with self.g(on):
            for i, r in enumerate(rows):
                self.text(x, y + i * gap, r, cls=cls, size=size, anchor=anchor, mono=mono, bold=bold)

    def arrow(self, x1, y1, x2, y2, on=None, color='track', sw=2, dash=False, bend=0, head=True):
        col = STROKE.get(color, color)
        if bend:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
            cx, cy = mx - dy / L * bend, my + dx / L * bend
            d = f'M{x1:g} {y1:g} Q{cx:g} {cy:g} {x2:g} {y2:g}'; ax, ay = x2 - cx, y2 - cy
        else:
            d = f'M{x1:g} {y1:g} L{x2:g} {y2:g}'; ax, ay = x2 - x1, y2 - y1
        L = math.hypot(ax, ay) or 1; ux, uy = ax / L, ay / L
        hx1, hy1 = x2 - 8 * ux + 4.5 * uy, y2 - 8 * uy - 4.5 * ux
        hx2, hy2 = x2 - 8 * ux - 4.5 * uy, y2 - 8 * uy + 4.5 * ux
        da = ';stroke-dasharray:5 4' if dash else ''
        s = f'<path d="{d}" style="stroke:{col};stroke-width:{sw};fill:none{da}"/>'
        if head: s += f'<path d="M{hx1:.1f} {hy1:.1f} L{x2:g} {y2:g} L{hx2:.1f} {hy2:.1f}" style="stroke:{col};stroke-width:{sw};fill:none;stroke-linecap:round;stroke-linejoin:round"/>'
        self._emit(f'<g{_a(on)}>{s}</g>' if on else s)

    def token(self, x, y, w, h, label, pos, on=None, fill='soft-acc', stroke='track', size=10.5, cls='ink',
              bold=True, mono=False, rx=13):
        self.box(x, y, w, h, label, fill=fill, stroke=stroke, on=on, pos=pos, rx=rx, size=size, cls=cls,
                 bold=bold, mono=mono, sw=2)

    def circle(self, cx, cy, r, fill='soft-blue', stroke='blue', on=None, label=None, size=11, cls='ink', bold=True):
        s = f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{FILL.get(fill, "")}" style="stroke:{STROKE.get(stroke, stroke)};stroke-width:1.6"/>'
        if label: s += self._t(cx, cy + size * .36, label, cls, size, 'middle', bold, False)
        self._emit(f'<g{_a(on)}>{s}</g>' if on else s)

    def raw(self, svg, on=None):
        self._emit(f'<g{_a(on)}>{svg}</g>' if on else svg)

    def note(self, s_by_frame, y=None, size=11, cls='ink2'):
        """One line of narration at the bottom, a different one per frame: dict {frame: text}."""
        y = y or self.h - 26
        for f, s in s_by_frame.items():
            self.text(self.w / 2, y, s, on=str(f), cls=cls, size=size, anchor='middle')

    def caps(self, caps):
        self._caps = caps

    # ---- output ---------------------------------------------------------
    def html(self):
        assert len(self._caps) == self.frames, f'{self.title}: {self.frames} frames but {len(self._caps)} captions'
        caps = '\n'.join(f'          <li>{c}</li>' for c in self._caps)
        body = '\n'.join(self.out)
        return f'''<div class="anim anim--one" data-frames="{self.frames}" data-delay="{self.delay}">
    <div class="anim__title">{self.title} <span>{self.frames} steps</span></div>
    <div class="anim__views">
      <div class="view view--story">
        <span class="view__tag">{self.tag}</span>
        <svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{_h.escape(self.label)}">
{body}
          <text x="{self.w - 6}" y="{self.h - 5}" text-anchor="end" class="s-wm">myphatshala.in</text>
        </svg>
        <ol class="caps" hidden>
{caps}
        </ol>
      </div>
    </div>
  </div>'''


def two_view(title, see, behind):
    """Part 5 'See it happen' block from two Anim objects with the same frame count:
    `see` is the 'What you see' view, `behind` the 'Behind the screen' view. Use via BLOCKS in spec.py."""
    assert see.frames == behind.frames, 'both views need the same number of frames'
    for a in (see, behind):
        assert len(a._caps) == a.frames, f'{a.title}: {a.frames} frames but {len(a._caps)} captions'
    def view(a, cls, tag):
        caps = '\n'.join(f'          <li>{c}</li>' for c in a._caps)
        body = '\n'.join(a.out)
        return f'''      <div class="view view--{cls}">
        <span class="view__tag">{tag}</span>
        <svg viewBox="0 0 {a.w} {a.h}" role="img" aria-label="{_h.escape(a.label)}">
{body}
          <text x="{a.w - 6}" y="{a.h - 5}" text-anchor="end" class="s-wm">myphatshala.in</text>
        </svg>
        <ol class="caps" hidden>
{caps}
        </ol>
      </div>'''
    return f'''<div class="anim" data-frames="{see.frames}">
    <div class="anim__title">{title} <span>{see.frames} steps</span></div>
    <div class="anim__views">
{view(see, 'see', 'What you see')}
{view(behind, 'behind', 'Behind the screen')}
    </div>
  </div>'''
