#!/usr/bin/env python3
"""Build a 'modifier lab' (.modlab) block: one member declared with each access modifier in turn,
used from several places in a multi-package project. Every result is produced by the real javac/java:
for each modifier, each user file is compiled together with the declaring file; the files that compile
are then wired into app/Main.java, compiled and run, and the real output is shown.

usage (from a lesson spec.py):
    from mkmodlab import modlab
    html = modlab(decl_file, files, users, intro_per_mod, mods=('public ', 'protected ', '', 'private '))
  files : {path: java source with {MOD} where the modifier goes}
  users : [dict(file, who, where, use, call)]   one per place that uses the member (decl_file may be one)
"""
import os, subprocess, tempfile, html, re

E = html.escape
env = dict(os.environ, JAVA_TOOL_OPTIONS='')


def _javac(d, files):
    c = subprocess.run(['javac', '-Xlint:-options', '-d', 'out'] + files, cwd=d, capture_output=True, text=True, env=env)
    return c.returncode, c.stderr.replace('Picked up JAVA_TOOL_OPTIONS: \n', '').strip()


def _write(d, path, src):
    p = os.path.join(d, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(src)


def _main(ok_users):
    imps = sorted({u['cls'] for u in ok_users})
    body = ''.join(f'        {u["call"]}\n' for u in ok_users)
    return ('package app;\n\n' + ''.join(f'import {c};\n' for c in imps) +
            '\npublic class Main {\n    public static void main(String[] args) {\n' + body + '    }\n}\n')


def run_mod(decl, files, users, mod):
    res = []
    for u in users:
        d = tempfile.mkdtemp(prefix='ml')
        for f in {decl, u['file']}: _write(d, f, files[f].replace('{MOD}', mod))
        rc, err = _javac(d, sorted({decl, u['file']}))
        # keep only the first line of each error (the message), and the caret line is noise here
        msg = re.sub(r'^\S+?/(\w+\.java)', r'\1', err.split('\n')[0]) if rc else ''
        res.append(dict(u, ok=rc == 0, err=msg))
    ok = [r for r in res if r['ok']]
    d = tempfile.mkdtemp(prefix='mlall')
    for f in {decl} | {r['file'] for r in ok}: _write(d, f, files[f].replace('{MOD}', mod))
    main = _main(ok); _write(d, 'app/Main.java', main)
    srcs = [os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs if f.endswith('.java')]
    rc, err = _javac(d, srcs)
    if rc: raise SystemExit('modlab: wiring failed\n' + err)
    out = subprocess.run(['java', '-cp', 'out', 'app.Main'], cwd=d, capture_output=True, text=True, env=env).stdout
    lines = {}
    for line in out.splitlines():
        lines[line.split('.')[0]] = line
    for r in res:
        if r['ok']: r['printed'] = lines.get(r['n'], '')
    return res, main, out


def modlab(decl, files, users, why, mods=('public ', 'protected ', '', 'private '), title='Choose the access level of <code>ifsc</code>:'):
    for u in users:
        u['cls'] = u['file'][:-5].replace('/', '.')
    panels, bar, summary = [], [], []
    for mod in mods:
        name = mod.strip() or 'default'
        res, main, out = run_mod(decl, files, users, mod)
        bar.append(f'<button type="button" role="tab" data-mod="{name}">{name}</button>')
        decl_line = next(l for l in files[decl].replace('{MOD}', mod).split('\n') if 'ifsc =' in l).strip()
        rows = []
        for r in res:
            if r['ok']:
                rows.append(f'<li class="modlab__row ok"><span class="mk" aria-label="compiles">✓</span><span class="who">{r["who"]} <small>({r["where"]})</small></span>'
                            f'<code class="use">{E(r["use"])}</code><span class="res">compiles · prints: {E(r["printed"].split(": ", 1)[-1])}</span></li>')
            else:
                rows.append(f'<li class="modlab__row no"><span class="mk" aria-label="compile error">✗</span><span class="who">{r["who"]} <small>({r["where"]})</small></span>'
                            f'<code class="use">{E(r["use"])}</code><span class="res">javac: {E(r["err"])}</span></li>')
        n_ok = sum(r['ok'] for r in res)
        summary.append((name, res, n_ok))
        panels.append(f'''<div class="modlab__panel" role="tabpanel" data-mod="{name}">
      <h4><code>{E(decl_line)}</code></h4>
      <span class="modlab__score">{n_ok} of {len(res)} places compile</span>
      <ol class="modlab__rows">{''.join(rows)}</ol>
      <p class="modlab__why">{why[name]}</p>
      <div class="code" data-lang="java" data-file="app/Main.java (only the classes that compile)" data-run="skip"><pre><code>{E(main.rstrip())}</code></pre><div class="output">{E(out.rstrip())}</div></div>
    </div>''')
    head = ''.join(f'<th><code>{n}</code></th>' for n, _, _ in summary)
    body = ''
    for i, u in enumerate(users):
        cells = ''.join(f'<td>{"✓" if res[i]["ok"] else "✗"}</td>' for _, res, _ in summary)
        body += f'<tr><td>{u["who"]} <small>({u["where"]})</small></td>{cells}</tr>'
    body += '<tr><td><b>Lines printed</b></td>' + ''.join(f'<td><b>{k}</b></td>' for _, _, k in summary) + '</tr>'
    table = (f'<div class="table-wrap"><table class="compare modlab__sum"><thead><tr><th>Who uses <code>ifsc</code></th>{head}</tr></thead>'
             f'<tbody>{body}</tbody></table></div>')
    lab = (f'<div class="modlab">\n    <div class="modlab__bar" role="tablist"><b>{title}</b>{"".join(bar)}</div>\n    '
           + '\n    '.join(panels) + '\n  </div>')
    return lab, table
