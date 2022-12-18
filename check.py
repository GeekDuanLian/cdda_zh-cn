#!/usr/bin/env python3

import polib
import re
import sys

old = polib.pofile(sys.argv[1])
new = polib.pofile(sys.argv[2])

old = {(i.msgid, i.msgctxt): i.msgstr_plural[0] if i.msgstr_plural else i.msgstr for i in old}
new = {(i.msgid, i.msgctxt): i.msgstr_plural[0] if i.msgstr_plural else i.msgstr for i in new}

f = open('fix.html', 'w')
f.write('<style>table, td { white-space: nowrap; vertical-align: top; border: 1px solid black; border-collapse: collapse; padding: 5px; } span { background-color: aqua }</style><table>')

need_fix = False
def check(s, mark=lambda x: f'<span>{x}</span>'):
    r = {}; s = s.replace('<', '\x00')
    en = ',.;:?!()<>[]'
    zh = '，。；：？！（）《》【】'
    enq = '\'"'
    zhq = '‘’“”'
    sym = '{}@#$%^&*-_=+|`~\\/\n\x00'
    for i in en+zh+enq+zhq+sym:
        if i+' ' in s : r['多余空格']=''; s = s.replace(i+' ', i+mark(' '))
        if ' '+i in s : r['多余空格']=''; s = s.replace(' '+i, mark(' ')+i)
        if i not in '\n?!？！' and (i:=i+i) in s: r['重复符号']=''; s = s.replace(i, mark(i))
    for a, b in zip(en+''.join([i*2 for i in enq])+'.', zh+zhq+'…'):
        if (i:=a+b) in s: r['重复符号']=''; s = s.replace(i, mark(i))
        if (i:=b+a) in s: r['重复符号']=''; s = s.replace(i, mark(i))
    if s.  endswith(' '): r['多余空格']=''; s = s[:-1]+mark(' ')
    if s.startswith(' '): r['多余空格']=''; s = mark(' ')+s[1:]
    if '\xa0' in s: r['非法空格']=''; s = s.replace('\xa0', mark(r'\xa0'))
    #if any([i in s for i in zhq]): r['中文引号']=''; s = re.sub(f'([{zhq}])', mark(r'\1'), s)
    if r: f.write('<tr><td>'+'<br>'.join(r.keys())+'</td><td><pre>'+s.replace('\x00', '&lt;').replace('\n', '<br>')+'</pre></td></tr>'); global need_fix; need_fix = True

for k, v in new.items():
    if k in old and old[k] == v: continue # same
    if v: check(v)

f.write('</table>'); f.close()
if not need_fix: import os; os.remove(f.name)
