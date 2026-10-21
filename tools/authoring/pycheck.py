#!/usr/bin/env python3
"""Check a generated Python-track lesson page: python3 tools/authoring/pycheck.py PAGE [PAGE...]
Checks: JSON blocks parse; quiz answers in range; every SVG is well-formed XML;
anim frame count == caption count and data-on ranges stay inside it; tags balance."""
import sys, re, json, html
from html.parser import HTMLParser
import xml.dom.minidom as md
VOID={'br','img','meta','link','input','hr','source','wbr','path','rect','circle','line','polyline','polygon','ellipse','stop','use'}
class Bal(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append((t,s.getpos()))
    def handle_startendtag(s,t,a): pass
    def handle_endtag(s,t):
        if t in VOID: return
        if s.st and s.st[-1][0]==t: s.st.pop()
        else: s.err.append(f'</{t}> at {s.getpos()} but open {s.st[-1] if s.st else None}'); 
allok=True
for page in sys.argv[1:]:
    s=open(page,encoding='utf-8').read(); errs=[]
    for i,j in enumerate(re.findall(r'<script type="application/json">(.*?)</script>',s,re.S)):
        try:
            d=json.loads(j)
            if isinstance(d,dict) and 'questions' in d:
                for q in d['questions']:
                    if not 0<=q.get('answer',0)<len(q.get('options',[])): errs.append('quiz answer out of range: '+q['q'][:40])
        except Exception as e: errs.append(f'JSON block {i}: {e}')
    for i,svg in enumerate(re.findall(r'<svg.*?</svg>',s,re.S)):
        x=re.sub(r'&(?!amp;|lt;|gt;|quot;|#)', '&amp;', svg)  # html entities like &nbsp; would fail anyway
        try: md.parseString(svg.replace('&nbsp;','&#160;'))
        except Exception as e: errs.append(f'SVG {i} not XML: {e}')
    for m in re.finditer(r'<div class="anim[^"]*" data-frames="(\d+)".*?<!--END-->|<div class="anim[^"]*" data-frames="(\d+)"',s,re.S):
        pass
    parts=re.split(r'(?=<div class="anim[ "])',s)[1:]
    for k,p in enumerate(parts):
        n=int(re.search(r'data-frames="(\d+)"',p).group(1))
        p=p[:p.find('</ol>',p.rfind('class="caps"'))] if 'class="caps"' in p else p
        for ol in re.findall(r'<ol class="caps"[^>]*>(.*?)$|<ol class="caps"[^>]*>(.*?)</ol>',p+'</ol>',re.S):
            pass
        caps=re.findall(r'<ol class="caps"[^>]*>(.*?)(?:</ol>|$)',p,re.S)
        for c in caps:
            cnt=c.count('<li>')
            if cnt!=n: errs.append(f'anim {k}: {n} frames but {cnt} captions')
        for r in re.findall(r'data-on="([^"]*)"',p):
            for part in r.split(','):
                for v in part.split('-'):
                    if v and int(v)>n: errs.append(f'anim {k}: data-on {r} > {n}')
    b=Bal(); b.feed(re.sub(r'<script.*?</script>','',s,flags=re.S)); errs+=b.err[:5]
    if b.st: errs.append(f'unclosed: {b.st[-3:]}')
    print(('✓ ' if not errs else '✗ ')+page+(' ('+str(len(errs))+' problems)' if errs else ''))
    for e in errs[:12]: print('   ',e)
    allok&=not errs
sys.exit(0 if allok else 1)
