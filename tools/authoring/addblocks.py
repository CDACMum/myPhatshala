#!/usr/bin/env python3
"""Add worked examples (and optionally practice problems) to an already-built lesson page.
usage: addblocks.py PAGE.html SPEC.py
SPEC defines WORKED_INTRO, EXAMPLES (same format as build.py) and optionally PRACTICE_INTRO, PROBLEMS.
Worked examples go at the end of part 8 (after the main tracer); practice goes in part 9 before the
scenarios heading. The table of contents and the practice chip are updated. Refuses to add a block twice."""
import sys, os, re, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build

LV = {'easy': 'Easy', 'medium': 'Medium', 'business': 'Business problem'}


def finish_practice(body):
    cnt = [0]
    def prob(g):
        cnt[0] += 1
        return (f'<article class="prob"><div class="prob__head"><span class="prob__num">P{cnt[0]}</span>'
                f'<span class="prob__tag prob__tag--{g[1]}">{LV[g[1]]}</span><h4>{g[2]}</h4></div>')
    body = re.sub(r'<prob level="(easy|medium|business)" title="([^"]+)">', prob, body)
    body = body.replace('</prob>', '</article>')
    body = re.sub(r'<io>\s*<in>(.*?)</in>\s*<out>(.*?)</out>\s*</io>', lambda g: f'<div class="prob__io"><div><small>Input</small><pre>{g[1]}</pre></div><div><small>Expected output</small><pre>{g[2]}</pre></div></div>', body, flags=re.S)
    return body.replace('<sol>', '<details class="prob__sol"><summary>Show solution and explanation</summary>').replace('</sol>', '</details>')


def main(page, specf):
    s = open(page, encoding='utf-8').read()
    spec = runpy.run_path(specf)
    if spec.get('EXAMPLES'):
        if 'id="worked"' in s: sys.exit('already has worked examples')
        blk = build.worked_html(spec['WORKED_INTRO'], spec['EXAMPLES'])
        i = s.index('<section class="part" id="tracer">')
        j = s.index('</section>', i)
        s = s[:j].rstrip() + '\n\n' + blk.rstrip() + '\n' + s[j:]
        s = s.replace('<li><a href="#tracer">Line by line</a></li>',
                      '<li><a href="#tracer">Line by line</a></li>\n      <li><a href="#worked">Worked examples</a></li>', 1)
    if spec.get('PROBLEMS'):
        if 'id="practice"' in s: sys.exit('already has practice problems')
        blk = finish_practice(build.practice_html(spec['PRACTICE_INTRO'], spec['PROBLEMS']))
        k = s.index('<h3 id="scenarios"')
        s = s[:k] + blk.lstrip('\n') + '\n  ' + s[k:]
        s = s.replace('<li><a href="#quiz">Quiz and revision</a></li>',
                      '<li><a href="#quiz">Quiz and revision</a></li>\n      <li><a href="#practice">Practice problems</a></li>', 1)
        n = len(spec['PROBLEMS'])
        s = re.sub(r'(<div class="lesson-meta">.*?)(</div>)', lambda g: g[1] + f'<span>{n} practice problems</span>' + g[2], s, count=1)
    open(page, 'w', encoding='utf-8').write(s)
    print('updated', page)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
