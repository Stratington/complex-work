import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(sys.argv[sys.argv.index('--src') + 1]) if '--src' in sys.argv else ROOT / 'paper' / 'src'
SKIP = {'appendix-f.tex'}

TARGETS = set(re.findall(r'\\hypertarget\{([^}]+)\}',
                         (SRC / 'appendix-f.tex').read_text(encoding='utf-8')
                         + (SRC / 'appendix-b.tex').read_text(encoding='utf-8')))
NUM = r'\d+(?:\.\d+)?'
LINKED = re.compile(r'\\hyperlink\{[^}]*\}\{[^}]*\}|\\hypertarget\{[^}]*\}\{[^}]*\}|\\ref\{[^}]*\}')
missing = []


def link(target, text):
    if target not in TARGETS:
        missing.append(target)
        return text
    return f'\\hyperlink{{{target}}}{{{text}}}'


def outside_links(s, fn):
    out, pos = [], 0
    for m in LINKED.finditer(s):
        out.append(fn(s[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fn(s[pos:]))
    return ''.join(out)


def cite_notes(s):
    def note(m):
        body = outside_links(m.group(2), lambda c: re.sub(
            r'(?<![\d.])(' + NUM + r')(?![\d.])', lambda n: link('nss-' + n.group(1), n.group(1)), c))
        body = outside_links(body, lambda c: re.sub(
            r'Appendix~([AB])\b', lambda n: link('nss-app' + n.group(1), n.group(0)), c))
        return m.group(1) + body + m.group(3)
    return re.sub(r'(\\cite[a-z]*\*?\[)((?:[^\[\]]|\{[^}]*\})*)(\]\{pss2026\})', note, s)


def section_signs(s):
    def fn(c):
        def rep(m):
            if 'GOAL' in c[max(0, m.start() - 6):m.start()]:
                return m.group(0)
            return link('nss-' + m.group(1), '\\S' + m.group(1))
        return re.sub(r'\\S(' + NUM + r')(?![\d.])', rep, c)
    return outside_links(s, fn)


def clause_words(s):
    def rep(m):
        nums = re.sub(r'(?<![\d.])(\d+\.\d+)(?![\d.])', lambda n: link('nss-' + n.group(1), n.group(1)), m.group(2))
        return m.group(1) + nums
    return outside_links(s, lambda c: re.sub(
        r'(\b[Cc]lauses?[ ~])(\d+\.\d+(?:(?:,? (?:and |or |to )?|~)\d+\.\d+)*)', rep, c))


def spec_appendices(s):
    return outside_links(s, lambda c: re.sub(
        r'(?<!\{)Appendix~([AB])\b(?!\})', lambda m: link('nss-app' + m.group(1), m.group(0)), c))


def patterns(s):
    def fn(c):
        def rep(m):
            if c[m.end():m.end() + 12].startswith('\\hypertarget'):
                return m.group(0)
            return link('gp-' + m.group(1), m.group(0))
        return re.sub(r'(?<![{\-\w])GP-(\d\d)(?![\d}])', rep, c)
    return outside_links(s, fn)


def protect_captions(s):
    return '\n'.join(re.sub(r'(?<!\\protect)\\hyperlink', r'\\protect\\hyperlink', l) if '\\caption' in l else l
                     for l in s.split('\n'))


def process(text):
    new = protect_captions(patterns(spec_appendices(clause_words(section_signs(cite_notes(text))))))
    old_lines, new_lines = text.split('\n'), new.split('\n')
    return '\n'.join(o if o.lstrip().startswith('%') else n for o, n in zip(old_lines, new_lines))


def main():
    fix = '--fix' in sys.argv[1:]
    pending = 0
    for f in sorted(SRC.glob('*.tex')):
        if f.name in SKIP:
            continue
        old = f.read_text(encoding='utf-8')
        new = process(old)
        added = new.count('\\hyperlink') - old.count('\\hyperlink')
        if added:
            pending += added
            print(f'{f.name}: {added} unlinked reference(s)')
            if fix:
                f.write_text(new, encoding='utf-8')
    if missing:
        sys.exit('link_refs: references without a target: ' + ', '.join(sorted(set(missing))))
    if pending and not fix:
        sys.exit(1)
    print('fixed' if fix and pending else 'all resolvable references are linked')


if __name__ == '__main__':
    main()
