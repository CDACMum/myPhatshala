#!/usr/bin/env python3
"""Insert (or replace) an "animated example" block in a lesson's Real-world part.
usage: addanim.py SITE_ROOT REL_LESSON_DIR SPEC.py
SPEC.py builds an mkanim.Anim called A and may set HEADING and INTRO (html).
The block sits between <!--ANIM2--> markers, so running again replaces it."""
import sys, os, re, runpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
root, rel, spec = sys.argv[1], sys.argv[2].strip('/'), sys.argv[3]
g = runpy.run_path(spec)
A = g['A']
head = g.get('HEADING', 'Watch it with an example')
intro = g.get('INTRO', '')
block = (f'<!--ANIM2-->\n  <h3 id="animated-example">{head}</h3>\n'
         + (f'  <p class="anim-intro">{intro}</p>\n' if intro else '')
         + '  ' + A.html() + '\n  <!--/ANIM2-->')
p = os.path.join(root, rel, 'index.html')
s = open(p, encoding='utf-8').read()
if '<!--ANIM2-->' in s:
    s = re.sub(r'<!--ANIM2-->.*?<!--/ANIM2-->', lambda m: block, s, flags=re.S)
else:
    i = s.index('<section class="part" id="real-world">')
    j = s.index('</h2>', i) + 5
    m = re.match(r'\s*<p>.*?</p>', s[j:], re.S)        # keep the part's intro paragraph first
    if m: j += m.end()
    s = s[:j] + '\n  ' + block + s[j:]
open(p, 'w', encoding='utf-8').write(s)
print('animated example added:', rel, A.frames, 'frames')
