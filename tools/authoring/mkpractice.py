#!/usr/bin/env python3
"""Build a practice-problems HTML snippet from a spec, running every solution to capture real output.
usage: mkpractice.py SPEC.py OUT.html
SPEC.py defines INTRO (html) and PROBLEMS = [dict(level, title, stmt, inp, code, explain, show=None)]
show: max output lines in the Expected output box (rest replaced by …)."""
import sys, os, html, subprocess, tempfile, runpy
spec = runpy.run_path(sys.argv[1])
env = dict(os.environ, JAVA_TOOL_OPTIONS='')
def run(code, stdin=''):
    d = tempfile.mkdtemp(prefix='mpp')
    open(os.path.join(d, 'Main.java'), 'w').write(code)
    c = subprocess.run(['javac', 'Main.java'], cwd=d, capture_output=True, text=True, env=env)
    if c.returncode: sys.exit('COMPILE ERROR\n' + code[:200] + '\n' + c.stderr)
    r = subprocess.run(['java', 'Main'], cwd=d, input=stdin, capture_output=True, text=True, env=env, timeout=30)
    if r.returncode: sys.exit('RUN ERROR\n' + r.stderr)
    return r.stdout.rstrip('\n')
e = html.escape
out = ['  <h3 id="practice">Practice problems</h3>', f'  <p class="prob-intro">{spec["INTRO"]}</p>', '  <div class="probs">']
for p in spec['PROBLEMS']:
    code = p['code'].strip('\n')
    res = run(code + '\n', p.get('stdin', ''))
    lines = res.split('\n'); show = p.get('show')
    box = '\n'.join(lines[:show] + ['…']) if show and len(lines) > show else res
    out.append(f'    <prob level="{p["level"]}" title="{e(p["title"])}">')
    out.append(f'      {p["stmt"]}')
    out.append(f'      <io><in>{e(p["inp"])}</in><out>{e(box)}</out></io>')
    out.append('      <sol>')
    out.append(f'        <div class="code" data-lang="java" data-file="Main.java"><pre><code>{e(code)}</code></pre><div class="output">{e(res)}</div></div>')
    out.append(f'        {p["explain"]}')
    out.append('      </sol>')
    out.append('    </prob>')
out.append('  </div>\n')
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
print('practice problems:', len(spec['PROBLEMS']))
