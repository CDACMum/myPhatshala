#!/usr/bin/env python3
"""Build the 'Worked examples' block for a lesson.
usage: mkworked.py SPEC.py OUT.html [--skeleton]
SPEC defines INTRO (html) and EXAMPLES = [dict(
    tag, title, problem (html), inp (text), approach [html,...], code (Java, public class Main),
    stdin='', tryit (html hint for the runner), notes [ "Phase :: note html", ... ] )]
The memory trace is recorded from the real JVM by tools/jtrace (JDI), so every stack frame,
local variable, heap object and printed line is exactly what Java does. notes[k] explains step k;
with --skeleton (or a count mismatch) the step list is printed so notes can be written.
"""
import sys, os, json, html, subprocess, tempfile, re

HERE = os.path.dirname(os.path.abspath(__file__))
JT = os.path.join(HERE, 'jtrace')
env = dict(os.environ, JAVA_TOOL_OPTIONS='')

def trace(code, stdin=''):
    d = tempfile.mkdtemp(prefix='wx')
    open(os.path.join(d, 'Main.java'), 'w').write(code)
    c = subprocess.run(['javac', '-g', '-Xlint:-options', 'Main.java'], cwd=d, capture_output=True, text=True, env=env)
    if c.returncode: sys.exit('compile error:\n' + c.stderr)
    sf = os.path.join(d, 'stdin.txt'); open(sf, 'w').write(stdin)
    # JDI occasionally drops early step events (a timing race). A bad run only ever loses steps,
    # so trace repeatedly and accept the longest step list once two runs agree on it.
    runs = []
    for attempt in range(12):
        r = subprocess.run(['java', '-Dstdout.encoding=UTF-8', '-Dfile.encoding=UTF-8', f'-Djtrace.boot={JT}', '-cp', JT, 'JTrace', d, sf],
                           capture_output=True, text=True, env=env, timeout=120, cwd=tempfile.mkdtemp(prefix='wxrun'))
        if r.returncode or not r.stdout.strip(): continue
        x = json.loads(r.stdout)
        if not x['steps'] or x['steps'][0]['line'] <= 0: continue   # breakpoint missed: invalid run
        runs.append(x)
        best = max(len(y['steps']) for y in runs)
        if len(runs) >= 3 and sum(1 for y in runs if len(y['steps']) == best) >= 2: break
    else:
        sys.exit('jtrace: could not get two agreeing complete traces')
    raw = next(x for x in runs if len(x['steps']) == best)
    real = subprocess.run(['java', '-cp', d, 'Main'], input=stdin, capture_output=True, text=True, env=env, cwd=tempfile.mkdtemp(prefix='wxreal'))
    return raw, real.stdout

def frame_label(f):
    return f['m']

def build_steps(raw, notes):
    steps, prev = [], {}
    for k, st in enumerate(raw['steps']):
        frames = [{"frame": frame_label(f), "vars": f["vars"]} for f in reversed(st["frames"])]
        top = st['frames'][0] if st['frames'] else None
        newVar = None
        if top:
            key = top['m']
            before = prev.get(key, {})
            for n, v in top['vars']:
                if before.get(n) != v and n != 'args':
                    newVar = n; break
        prev = {f['m']: dict(map(tuple, f['vars'])) for f in st['frames']}
        heap = [f"<b>static</b> " + html.escape(x) for x in st.get('statics', [])] + [f"<b>#{h['id']}</b> " + html.escape(h['d']) for h in st['heap']]
        step = {"line": st['line'], "stack": frames, "heap": heap}
        if newVar: step['newVar'] = newVar
        if st.get('out'): step['out'] = st['out']
        if st.get('crash'): step['crash'] = True
        steps.append(step)
    return steps

def skeleton(code, raw):
    lines = code.split('\n')
    prev = {}
    for k, st in enumerate(raw['steps']):
        ch = []
        for f in st['frames'][:1]:
            pv = prev.get(f['m'], {})
            for n, v in f['vars']:
                if pv.get(n) != v: ch.append(f'{n}={v}')
        prev = {f['m']: dict(map(tuple, f['vars'])) for f in st['frames']}
        depth = ' > '.join(f['m'].split('(')[0] for f in reversed(st['frames']))
        print(f"  [{k:2}] L{st['line']:<3} {lines[st['line']-1].strip()[:52]:<52} | {depth} | {', '.join(ch)[:70]} {('OUT ' + repr(st['out'])) if st.get('out') else ''}")

def main(spec, out, force_skel=False):
    g = {}; exec(open(spec, encoding='utf-8').read(), g)
    parts = [f'<h3 id="worked">Worked examples: real problems, solved and traced in memory</h3>\n  <p class="wx-intro">{g["INTRO"]}</p>']
    ok = True
    for n, ex in enumerate(g['EXAMPLES'], 1):
        code = ex['code'].strip('\n') + '\n'
        raw, real = trace(code, ex.get('stdin', ''))
        notes = ex.get('notes') or []
        if force_skel or len(notes) != len(raw['steps']):
            print(f"Example {n} '{ex['title']}': {len(raw['steps'])} steps, {len(notes)} notes")
            skeleton(code, raw); ok = False; continue
        steps = build_steps(raw, notes)
        for s, nt in zip(steps, notes):
            ph, _, tx = nt.partition('::')
            s['phase'] = ph.strip(); s['note'] = tx.strip()
        last = code.rstrip('\n').split('\n')
        steps.append({"line": len(last) - 1 if last[-1].strip() == '}' else len(last), "phase": "Program ends",
                      "note": ex.get('end', 'main returns, its frame is popped and the program ends.'), "stack": [], "heap": []})
        traced_out = ''.join(s.get('out', '') for s in steps)
        if traced_out.strip() != real.strip():
            sys.exit(f'trace output mismatch in example {n}:\n{traced_out!r}\n{real!r}')
        tracer = {"lang": "java", "code": code.rstrip('\n').split('\n'), "steps": steps}
        runner = {"lang": "java", "file": "Main.java", "tasks": [{"label": f"Run · {ex['title']}", "hint": ex.get('tryit', 'Press <b>Run</b>, then change the input values and run again.'), "code": code, **({"_stdin": ex['stdin']} if ex.get('stdin') else {})}]}
        appr = ''.join(f'<li>{a}</li>' for a in ex['approach'])
        parts.append(f'''  <article class="wx">
    <div class="wx__head"><span class="wx__num">Example {n}</span><span class="wx__tag">{ex['tag']}</span></div>
    <h4>{ex['title']}</h4>
    <div class="wx__problem"><p class="wx__label">Problem statement</p>{ex['problem']}</div>
    <div class="prob__io"><div><small>Input</small><pre>{html.escape(ex['inp'])}</pre></div><div><small>Expected output</small><pre>{html.escape(real.rstrip())}</pre></div></div>
    <div class="wx__approach"><p class="wx__label">Approach</p><ol>{appr}</ol></div>
    <p class="wx__label">Solution: run it live</p>
    <div class="runner">
    <script type="application/json">{json.dumps(runner, ensure_ascii=False)}</script>
    </div>
    <p class="wx__label">What happens in memory, step by step</p>
    <p class="wx__how">Recorded from the real JVM: press <b>Next</b> to execute one line at a time. Watch method calls push and pop frames on the stack, and objects (numbered #1, #2 …) appear on the heap.</p>
    <div class="tracer">
    <script type="application/json">{json.dumps(tracer, ensure_ascii=False)}</script>
    </div>
  </article>''')
    if not ok: sys.exit(1)
    open(out, 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
    print(f'worked examples: {len(g["EXAMPLES"])}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], '--skeleton' in sys.argv)
