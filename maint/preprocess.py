#!/usr/bin/env python

import argparse
import enum
import io
import re
import sys
from pathlib import Path

import ruamel.yaml


parser = argparse.ArgumentParser(description='Preprocess my text.')
parser.add_argument('--lang')
parser.add_argument('--format')
parser.add_argument('--book-version')
parser.add_argument('--process-meta', action='append',
                    help='file to process as metadata')
parser.add_argument('--process-template', action='append',
                    help='file to process as template')
parser.add_argument('--no-process', action='append',
                    help='files to not process')
parser.add_argument('--align', action=argparse.BooleanOptionalAction)
parser.add_argument('process', nargs='+', help='files to process')
args = parser.parse_args()
assert args.lang in ('en', 'ru')
assert args.format in ('epub', 'fb2', 'pdf', '80column.txt', 'freeflow.txt')


def read_files(filelist, separator='\n\n'):
    return separator.join([Path(fname).read_text() for fname in filelist])


def yaml(text):
    return ruamel.yaml.YAML().load(io.StringIO(text))


meta = yaml(read_files(args.process_meta or []))
if lang := meta.get('lang'):
    if '-' in lang:
        meta['language'], meta['region'] = lang.split('-', 1)
del lang
if args.book_version:
    meta['subtitle'] = args.book_version
tmpl = read_files(args.process_template or [])
for k, v in meta.items():
    tmpl = tmpl.replace(f'${k}$', v)
print(tmpl)

for fname in args.no_process or []:
    with open(fname) as f:
        s = f.read()
    print(s)

if args.format in ('epub', 'fb2'):
    print(f'{meta['title']}\n{meta['subtitle']}\n{meta['author']}\n\n')
    print(f'{meta['include-before']}\n#pagebreak()\n')

if args.format in ('80column.txt', 'freeflow.txt'):
    print(meta['title'])
    print(meta['subtitle'])
    print(meta['author'])
    print()
    print()
    print(meta['include-before'].replace(' \\\n', '\n'))
    print()

s = read_files(args.process, separator='\n#pagebreak()\n\n')

s = s.replace('\n// ltex: enabled=false\n%', ' ')
s = s.replace('%\n// ltex: enabled=true\n', ' ')
s = s.replace('\n// ltex: enabled=true\n', '\n')
s = s.replace('\n// ltex: enabled=false\n', '\n')
s = s.replace('\n// ltex: language=ru-RU\n', '\n')
s = s.replace('\n// ltex: language=en-GB\n', '\n')

if args.align:
    assert args.format == 'pdf'
    s = s.replace('\n. . . // page\n', '#pagebreak()\n\n. . .\n')
    s = re.sub(r'\n\n\. \. \. // (.*)',
               lambda m: '\n' + '\\\n' * (int(m.group(1))) + '\n\n. . .',
               s, flags=re.MULTILINE)
    s = re.sub(r'// align: (.*)', r'\1', s, flags=re.MULTILINE)
else:
    s = re.sub(r'\n// align: .*', '// align', s, flags=re.MULTILINE)
    s = re.sub(r'\n\. \. \. // (.*)\n', '\n. . .\n', s, flags=re.MULTILINE)
if args.format == 'pdf':
    if args.align:
        s = s.replace('\n\n. . .\n',
                      '\n\n#horizontalrule\n')
    else:
        s = s.replace('\n. . .\n', '\n#horizontalrule\n')
elif args.format in ('epub', 'fb2'):
    s = s.replace('\n. . .\n', '\n#line()\n')  # pandoc mismatch
else:
    s = s.replace('\n. . .\n', '\n* * *\n')  # pandoc mismatch

if args.format in ('epub', 'fb2', 'pdf'):
    if args.lang == 'ru':
        s = re.sub(r'(^|\s+)--(\s+|$)', r'\1---\2', s)
        s = re.sub(r'^--- ', r'---~', s, flags=re.MULTILINE)

SegmentKind = enum.Enum(
    'SegmentKind',
    ('NONE', 'NORMAL', 'SPEECH', 'SPEECHTAIL', 'SPEECHHEAD', 'SPEECHBOTH')
)
segments = []  # [(kind: SegmentKind, segment_body: list(str))]
kind, acc = SegmentKind.NORMAL, []
speechmarker = '"'
if args.lang == 'ru':
    speechmarker = '---~' if args.format in ('epub', 'fb2', 'pdf') else '-- '
for ln in s.split('\n'):  # categorize into just SPEECH and NORMAL so far
    if ln.startswith(speechmarker):
        if acc:
            segments.append((kind, acc))
        kind, acc = SegmentKind.SPEECH, []
        if args.lang == 'ru' and args.format == 'pdf':
            ln = ln.removeprefix(speechmarker)
    elif kind == SegmentKind.NORMAL and ln.startswith('%' + speechmarker):
        ln = ln.removeprefix('%')
    elif kind == SegmentKind.SPEECH and ln.startswith(' '):
        pass
    elif (kind == SegmentKind.SPEECH and
          (ln.startswith('.') and not ln.startswith('...'))):
        acc[-1] += '\\'
        ln = ln.removeprefix('.')
    else:
        if acc:
            segments.append((kind, acc))
        kind, acc = SegmentKind.NORMAL, []
    acc.append(ln)
if acc:
    segments.append((kind, acc))

segments = [(kind, '\n'.join(segment)) for kind, segment in segments]

stub = [(SegmentKind.NORMAL, '')]
segments = [s if s[1] else (SegmentKind.NONE, s[1]) for s in segments]

segments_ = []
for prev, curr, next in zip(stub + segments[:-1],
                            segments,
                            segments[1:] + stub):
    contents = curr[1]
    match prev[0], curr[0], next[0]:
        case SegmentKind.NONE, SegmentKind.SPEECH, SegmentKind.NONE:
            kind = SegmentKind.SPEECHBOTH
        case SegmentKind.NONE, SegmentKind.SPEECH, _:
            kind = SegmentKind.SPEECHHEAD
        case _, SegmentKind.SPEECH, SegmentKind.NONE:
            kind = SegmentKind.SPEECHTAIL
        case _:
            kind = curr[0]
    segments_.append((kind, contents))
segments = segments_

if args.format == 'pdf':
    s = '\n'.join(f'#speechnorm[{seg}]' if kind == SegmentKind.SPEECH else
                  f'#speechhead[{seg}]' if kind == SegmentKind.SPEECHHEAD else
                  f'#speechtail[{seg}]' if kind == SegmentKind.SPEECHTAIL else
                  f'#speechboth[{seg}]' if kind == SegmentKind.SPEECHBOTH else
                  seg
                  for kind, seg in segments)
elif args.format in ('epub', 'fb2'):
    s = ''.join(f'\n{seg}\n\n' if kind == SegmentKind.SPEECH else
                f'\n\n{seg}\n\n' if kind == SegmentKind.SPEECHHEAD else
                f'\n{seg}\n\n\n' if kind == SegmentKind.SPEECHTAIL else
                f'\n\n{seg}\n\n\n' if kind == SegmentKind.SPEECHBOTH else
                f'{seg}\n'
                for kind, seg in segments)
    s = re.sub(r'\n\n+#line\(\)\n\n+', '\n\n#line()\n\n', s)
    if args.format == 'fb2':
        s = re.sub(r'\n\n\n\n+', '\n\n#linebreak()\n\n', s)
    elif args.format == 'epub':
        s = re.sub(r'\n\n\n\n+', '\n\n#linebreak()\n', s)
    s = re.sub(r'\n\n+', '\n\n', s)
elif args.format in ('80column.txt', 'freeflow.txt'):
    if args.format == '80column.txt':
        s = '\n'.join(seg for _, seg in segments)
    elif args.format == 'freeflow.txt':
        s = ''.join(f'#@#{seg}#@#' if kind == SegmentKind.SPEECH else
                    f'#@#{seg}' if kind == SegmentKind.SPEECHHEAD else
                    f'{seg}#@#' if kind == SegmentKind.SPEECHTAIL else
                    f'#@#{seg}#@#' if kind == SegmentKind.SPEECHBOTH else
                    '#@##@##@#' if kind == SegmentKind.NONE else
                    f'{seg}\n'
                    for kind, seg in segments)
    s = s.replace(' \\\n', '\n')
    if args.format == '80column.txt':
        for line in s.split('\n'):
            assert len(line) <= 80, line
    elif args.format == 'freeflow.txt':
        s = s.replace('\n', ' ')
        s = re.sub(r' +', r' ', s)
        s = s.replace('#@#' * 4, '\n\n')
        s = s.replace('#@#' * 3, '\n\n')
        s = s.replace('#@#' * 2, '\n')
        s = s.replace('#@#' * 1, '\n')
        s = s.replace(' \n', '\n')
        s = s.lstrip()
print(s)
