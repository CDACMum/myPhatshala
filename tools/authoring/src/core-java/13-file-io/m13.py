"""Helpers for Module 13 specs: code blocks whose output comes from a real run, runners and quizzes as JSON."""
import subprocess, tempfile, os, json, html

ENV = dict(os.environ, JAVA_TOOL_OPTIONS='')


def run(code, stdin=''):
    d = tempfile.mkdtemp(prefix="m13")
    open(os.path.join(d, 'Main.java'), 'w').write(code)
    c = subprocess.run(['javac', 'Main.java'], cwd=d, capture_output=True, text=True, env=ENV)
    if c.returncode:
        raise SystemExit('compile error in code block:\n' + c.stderr + '\n' + code)
    r = subprocess.run(['java', 'Main'], cwd=d, input=stdin, capture_output=True, text=True, env=ENV, timeout=60)
    if r.returncode:
        raise SystemExit('code block failed:\n' + r.stderr + '\n' + code)
    return r.stdout


def code(src, skip=False, out=None):
    """A runnable .code block. Output is taken from a real run. skip=True marks timing/scheduling-dependent
    output (data-check="skip"); then `out` may give a representative real output to show."""
    src = src.strip('\n')
    got = run(src + '\n')
    shown = out if (skip and out is not None) else got
    attr = ' data-check="skip"' if skip else ''
    return (f'<div class="code" data-lang="java" data-file="Main.java"{attr}><pre><code>{html.escape(src, quote=False)}</code></pre>'
            f'<div class="output">{html.escape(shown.rstrip(), quote=False)}</div></div>')


def snippet(src, lang='java', file='Main.java'):
    return f'<div class="code" data-lang="{lang}" data-file="{file}"><pre><code>{html.escape(src.strip(), quote=False)}</code></pre></div>'


def runner(tasks):
    """tasks: list of dict(label, hint, code, _expect?, _stdin?)"""
    for t in tasks:
        t['code'] = t['code'].strip('\n') + '\n'
    return '<div class="runner">\n    <script type="application/json">' + json.dumps(
        {"lang": "java", "file": "Main.java", "tasks": tasks}, ensure_ascii=False, indent=1) + '</script>\n  </div>'


def quiz(qs):
    return '<div class="quiz">\n    <script type="application/json">' + json.dumps(qs, ensure_ascii=False, indent=1) + '</script>\n  </div>'
