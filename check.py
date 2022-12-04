#!/usr/bin/env python3

import polib
import re
import sys

old = polib.pofile(sys.argv[1])
new = polib.pofile(sys.argv[2])

old = {(i.msgid, i.msgctxt): i.msgstr for i in old}
new = {(i.msgid, i.msgctxt): i.msgstr for i in new}

f = open('fix.html', 'w')
f.write('<style>table, td { white-space: nowrap; vertical-align: top; border: 1px solid black; border-collapse: collapse; padding: 5px; }</style><table>')

need_fix = False
def check(s, mark=lambda x: f'<span style="color:red">{x}</span>'):
    r = {}
    if s.endswith(' '): r['多余空格']=''; s = s[:-1]+mark('•')
    for i in ',.;:?!)，。；：？！）\n':
        if i+' ' in s: r['多余空格']=''; s = s.replace(i+' ', i+mark('•'))
    if '..' in s: r['英文省略号']=''; s = re.sub('([.]{2,})', mark(r'\1'), s)
    #if any([i in s for i in '‘’“”']): r['中文引号']=''; s = re.sub('([‘’“”])', mark(r'\1'), s)
    if r:
        f.write('<tr><td>'+'<br>'.join(r.keys())+'</td><td><pre>'+s.replace('\n', '<br>')+'</pre></td></tr>')
        global need_fix; need_fix = True

for k, v in new.items():
    if k in old and old[k] == v: continue # same
    check(v)

f.write('</table>'); f.close()
if not need_fix: import os; os.remove(f.name)
