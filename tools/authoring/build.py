#!/usr/bin/env python3
"""Build one lesson from its source folder and write the page into the site.
usage: build.py SRC_DIR SITE_ROOT
SRC_DIR holds:
  lesson.html  META header + body (gen.py macros) with placeholders
               {{ANIM2}} {{TRACER}} {{WORKED}} {{PRACTICE}}
  spec.py      ANIM2 (mkanim.Anim), ANIM2_HEADING, ANIM2_INTRO
               TRACE = dict(code, notes={line: "Phase :: html"}, stdin='', end='')
               WORKED_INTRO, EXAMPLES = [dict(tag, title, problem, inp, approach, code, notes={...}, tryit, stdin)]
               PRACTICE_INTRO, PROBLEMS = [dict(level, title, stmt, inp, code, explain, show=None, stdin='')]
               BLOCKS = {'KEY': html}  optional extra blocks that replace {{KEY}} in lesson.html
Traces are recorded from the real JVM (tools/authoring/jtrace). Each step gets the author's note for
its line (keys: line number, or (line, k) for the k-th time that line runs, 1-based), followed by an
automatic description of what changed (frames pushed/popped, variables, new heap objects, output).
A note written 'Phase :: = text' replaces the automatic description instead of adding to it.
"""
import sys, os, json, html, re, runpy, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mkworked, gen

env = dict(os.environ, JAVA_TOOL_OPTIONS='')
E = html.escape


def mname(m):
    return m.split('(')[0]


def cached_box(d):
    """True for wrapper objects that valueOf/autoboxing take from the JDK caches (Integer etc. -128..127)."""
    m = re.match(r'(Integer|Short|Long|Byte) (-?\d+)$', d)
    if m: return -128 <= int(m.group(2)) <= 127
    return bool(re.match(r'Boolean (true|false)$', d))


def auto(prev, st, src=None, nxt=None, seen=None):
    """Plain-language description of what changed between two recorded steps."""
    bits, phase = [], None
    pf, cf = (prev['frames'] if prev else []), st['frames']
    first = prev is None
    if first:
        mf = cf[-1] if cf else None
        if mf and mname(mf['m']) == 'main':
            pf = [{'m': mf['m'], 'vars': [v for v in mf['vars'] if v[0] == 'args'] if len(cf) == 1 else mf['vars']}]
        prev = {'frames': pf, 'heap': [h for h in st['heap'] if h['d'].startswith('String[0]')]}
    if len(cf) > len(pf) and '<clinit>' in cf[0]['m']:
        bits.append(f'First use of <code>{E(cf[0]["m"].split(".")[0])}</code>: the JVM initialises the class, setting up its static fields. This happens only once.')
        phase = 'Class init'
    elif len(cf) > len(pf):
        top = cf[0]
        ps = ', '.join(f'<code>{E(n)}</code> = {E(v)}' for n, v in top['vars'] if n != 'args')
        bits.append(f'<code>{E(mname(top["m"]))}()</code> is called: a new frame is pushed' + (f' with {ps}' if ps else '') + '.')
        phase = 'Call'
    elif len(cf) < len(pf):
        gone = [mname(f['m']) for f in pf[:len(pf) - len(cf)]]
        if any('<clinit>' in g for g in gone):
            bits.append('Class initialisation is finished.')
        else:
            bits.append(' and '.join(f'<code>{E(g)}()</code>' for g in gone) + (' returns' if len(gone) == 1 else ' return') + ' and its frame is popped.')
        phase = 'Return'
        if cf:
            before = dict(map(tuple, pf[len(pf) - len(cf)]['vars']))
            ch = [f'<code>{E(n)}</code> = {E(v)}' for n, v in cf[0]['vars'] if before.get(n) != v]
            if ch: bits.append('Back in <code>' + E(mname(cf[0]['m'])) + '()</code>: ' + ', '.join(ch) + '.')
    elif cf:
        before = dict(map(tuple, pf[0]['vars'])) if pf else {}
        ch = [f'<code>{E(n)}</code> = {E(v)}' for n, v in cf[0]['vars'] if n != 'args' and before.get(n) != v]
        if ch:
            bits.append('Now ' + ', '.join(ch) + '.')
            phase = 'Assign'
    ps = set(prev.get('statics', [])) if prev else set()
    for x in st.get('statics', []):
        if x not in ps and prev is not None and not first:
            bits.append(f'Static field <code>{E(x)}</code> (shared by the whole class).')
            phase = phase or 'Static'
    ph = {h['id'] for h in (prev['heap'] if prev else [])}
    pd = {h['id']: h['d'] for h in (prev['heap'] if prev else [])}
    upd = [h for h in st['heap'] if h['id'] in pd and pd[h['id']] != h['d'] and not h['d'].startswith('String')]
    for h in upd[:2]:
        bits.append(f'Object <b>#{h["id"]}</b> changes: {E(h["d"][:80])}.')
        phase = phase or 'Update'
    if seen is not None: ph |= seen
    new = [h for h in st['heap'] if h['id'] not in ph]
    if seen is not None: seen.update(h['id'] for h in st['heap'])
    for h in new[:3]:
        if cached_box(h['d']):
            bits.append(f'Object <b>#{h["id"]}</b> ({E(h["d"])}) is a <b>cached</b> object the JDK made at start-up: boxing small values reuses it instead of creating one.')
        else:
            bits.append(f'New object <b>#{h["id"]}</b> on the heap: {E(h["d"][:70])}.')
    if st.get('out'):
        o = st['out'].rstrip('\n').replace('\n', ' ⏎ ')
        bits.append(f'Prints <code>{E(o[:90])}</code>.')
        phase = phase or 'Print'
    if st.get('crash'):
        bits.append('An exception is thrown here.')
        phase = 'Exception'
    if not bits and src is not None:
        t = src.strip()
        m = re.match(r'(?:\}\s*else\s+)?(if|while)\s*\((.*)\)\s*\{$', t)
        if m and nxt is not None:
            ok = nxt['line'] == st['line'] + 1
            bits.append(f'The condition <code>{E(m.group(2))}</code> is checked: <b>{"true" if ok else "false"}</b>' +
                        (', so the block runs.' if ok else (', so the loop ends.' if m.group(1) == 'while' else ', so the block is skipped.')))
            phase = 'Check'
        elif t.startswith('for') and ':' in t:
            bits.append('No elements left, so the loop ends.'); phase = 'Loop ends'
        elif t.startswith('for'):
            bits.append('The loop condition is checked.'); phase = 'Check'
        elif re.match(r'^(public |private |protected )?[A-Z]\w*\([^)]*\)\s*(throws [\w, ]+)?\s*\{$', t):
            bits.append('The constructor starts. The new object already exists, with default values (0, null, false) in its fields.'); phase = 'Constructor'
        elif t.startswith('}') or t == '':
            bits.append('End of the block.'); phase = 'Step'
    return phase or 'Step', ' '.join(bits)


def traced_steps(code, notes, stdin='', end=None):
    raw, real = mkworked.trace(code, stdin)
    steps = mkworked.build_steps(raw, [])
    seen = {}
    prev = None
    src = code.split('\n')
    rs = raw['steps']
    seen_ids = set()
    used_keys = set()
    for k, (st, s) in enumerate(zip(rs, steps)):
        ln = st['line']; seen[ln] = seen.get(ln, 0) + 1
        nt = notes.get((ln, seen[ln]), notes.get(ln))
        used_keys.add((ln, seen[ln]) if (ln, seen[ln]) in notes else ln)
        ph, tx = auto(prev, st, src[ln - 1] if 0 < ln <= len(src) else None, rs[k + 1] if k + 1 < len(rs) else None, seen_ids)
        if nt:
            p2, _, t2 = nt.partition('::')
            if t2.strip().startswith('='): ph, tx = p2.strip(), t2.strip()[1:].strip()   # 'Phase :: = text' replaces the automatic note
            elif t2: ph, tx = p2.strip(), t2.strip() + (' ' + tx if tx else '')
            else: tx = p2.strip() + (' ' + tx if tx else '')
        for fr in s['stack']:
            fr['frame'] = fr['frame'].replace('.<clinit>()', ' (static init)').replace('.<clinit>', ' (static init)')
        s['phase'] = ph; s['note'] = tx or 'This line runs; nothing visible changes.'
        prev = st
    unused = [k for k in notes if k not in used_keys]
    if unused: print(f'  WARNING: notes never matched a step: {unused}')
    lines = code.rstrip('\n').split('\n')
    if len(steps) > 1 and not steps[-1].get('out') and steps[-1]['note'] == 'End of the block.':
        steps.pop()
    steps.append({"line": len(lines) - 1 if lines[-1].strip() == '}' else len(lines), "phase": "Program ends",
                  "note": end or '<code>main</code> returns, its frame is popped and the program ends.', "stack": [], "heap": []})
    tout = ''.join(s.get('out', '') for s in steps)
    if tout.strip() != real.strip():
        sys.exit(f'trace output mismatch:\n{tout!r}\n{real!r}')
    return steps, real, len(raw['steps'])


def tracer_html(code, steps, stdin=''):
    t = {"lang": "java", "code": code.rstrip('\n').split('\n'), "steps": steps}
    if stdin: t['_stdin'] = stdin
    return f'<div class="tracer">\n    <script type="application/json">{json.dumps(t, ensure_ascii=False)}</script>\n  </div>'


def worked_html(intro, examples):
    parts = [f'<h3 id="worked">Worked examples: real problems, solved and traced in memory</h3>\n  <p class="wx-intro">{intro}</p>']
    for n, ex in enumerate(examples, 1):
        code = ex['code'].strip('\n') + '\n'
        steps, real, k = traced_steps(code, ex.get('notes', {}), ex.get('stdin', ''), ex.get('end'))
        if not 6 <= k <= 40: print(f'  note: example {n} has {k} steps')
        runner = {"lang": "java", "file": "Main.java", "tasks": [{"label": f"Run · {ex['title']}", "hint": ex.get('tryit', 'Press <b>Run</b>, then change the input values and run again.'), "code": code, **({"_stdin": ex['stdin']} if ex.get('stdin') else {})}]}
        appr = ''.join(f'<li>{a}</li>' for a in ex['approach'])
        parts.append(f'''  <article class="wx">
    <div class="wx__head"><span class="wx__num">Example {n}</span><span class="wx__tag">{ex['tag']}</span></div>
    <h4>{ex['title']}</h4>
    <div class="wx__problem"><p class="wx__label">Problem statement</p>{ex['problem']}</div>
    <div class="prob__io"><div><small>Input</small><pre>{E(ex['inp'])}</pre></div><div><small>Expected output</small><pre>{E(real.rstrip())}</pre></div></div>
    <div class="wx__approach"><p class="wx__label">Approach</p><ol>{appr}</ol></div>
    <p class="wx__label">Solution: run it live</p>
    <div class="runner">
    <script type="application/json">{json.dumps(runner, ensure_ascii=False)}</script>
    </div>
    <p class="wx__label">What happens in memory, step by step</p>
    <p class="wx__how">Recorded from the real JVM: press <b>Next</b> to execute one line at a time. Watch method calls push and pop frames on the stack, and objects (numbered #1, #2 …) appear on the heap.</p>
    {tracer_html(code, steps, ex.get('stdin', ''))}
  </article>''')
    return '\n'.join(parts) + '\n'


def run(code, stdin=''):
    d = tempfile.mkdtemp(prefix='mpb')
    open(os.path.join(d, 'Main.java'), 'w').write(code)
    c = subprocess.run(['javac', 'Main.java'], cwd=d, capture_output=True, text=True, env=env)
    if c.returncode: sys.exit('COMPILE ERROR\n' + code[:300] + '\n' + c.stderr)
    r = subprocess.run(['java', 'Main'], cwd=d, input=stdin, capture_output=True, text=True, env=env, timeout=30)
    if r.returncode: sys.exit('RUN ERROR\n' + code[:300] + '\n' + r.stderr)
    return r.stdout.rstrip('\n')


def practice_html(intro, problems):
    out = ['  <h3 id="practice">Practice problems</h3>', f'  <p class="prob-intro">{intro}</p>', '  <div class="probs">']
    for p in problems:
        code = p['code'].strip('\n')
        res = run(code + '\n', p.get('stdin', ''))
        lines = res.split('\n'); show = p.get('show')
        box = '\n'.join(lines[:show] + ['…']) if show and len(lines) > show else res
        sd = f' data-stdin="{E(p["stdin"]).replace(chr(10), chr(92) + "n")}"' if p.get('stdin') else ''
        out.append(f'    <prob level="{p["level"]}" title="{E(p["title"])}">')
        out.append(f'      {p["stmt"]}')
        out.append(f'      <io><in>{E(p["inp"])}</in><out>{E(box)}</out></io>')
        out.append('      <sol>')
        out.append(f'        <div class="code" data-lang="java" data-file="Main.java"{sd}><pre><code>{E(code)}</code></pre><div class="output">{E(res)}</div></div>')
        out.append(f'        {p["explain"]}')
        out.append('      </sol>')
        out.append('    </prob>')
    out.append('  </div>\n')
    return '\n'.join(out) + '\n'


def main(src, root):
    spec = runpy.run_path(os.path.join(src, 'spec.py'))
    body = open(os.path.join(src, 'lesson.html'), encoding='utf-8').read()
    if '{{ANIM2}}' in body:
        a = spec['ANIM2']
        blk = (f'<!--ANIM2-->\n  <h3 id="animated-example">{spec.get("ANIM2_HEADING", "Watch it with an example")}</h3>\n'
               + (f'  <p class="anim-intro">{spec["ANIM2_INTRO"]}</p>\n' if spec.get('ANIM2_INTRO') else '') + '  ' + a.html() + '\n  <!--/ANIM2-->')
        body = body.replace('{{ANIM2}}', blk)
    if '{{TRACER}}' in body:
        t = spec['TRACE']; code = t['code'].strip('\n') + '\n'
        steps, real, k = traced_steps(code, t.get('notes', {}), t.get('stdin', ''), t.get('end'))
        print(f'  main tracer: {k} steps')
        body = body.replace('{{TRACER}}', tracer_html(code, steps, t.get('stdin', '')))
    if '{{WORKED}}' in body:
        body = body.replace('{{WORKED}}', worked_html(spec['WORKED_INTRO'], spec['EXAMPLES']))
    if '{{PRACTICE}}' in body:
        body = body.replace('{{PRACTICE}}', practice_html(spec['PRACTICE_INTRO'], spec['PROBLEMS']))
        n = len(spec['PROBLEMS'])
        body = body.replace('{{NPROB}}', str(n))
    for k, v in spec.get('BLOCKS', {}).items():   # extra lesson-specific html blocks: {{KEY}}
        body = body.replace('{{' + k + '}}', v)
    tmp = os.path.join(tempfile.mkdtemp(prefix='mpl'), 'lesson.html')
    open(tmp, 'w', encoding='utf-8').write(body)
    gen.main(tmp, root)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
