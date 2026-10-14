import re
import sys

SPECIAL = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
           '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\^{}'}


def esc(s):
    return ''.join(SPECIAL.get(c, c) for c in s)


PRINCIPLES = {'Component-Oriented Decomposition': 'COD', 'Layered System Architecture': 'LSA',
              'Integrated Modularity First': 'IMF', 'Verification-First Engineering': 'VFE',
              'Specifications as Contracts': 'SaC'}
CLAUSE = r'\\S(\d+(?:\.\d+)?)'
GOAL = re.compile(r'GOAL ' + CLAUSE + r'(?:(?:, | and | to )' + CLAUSE + r')*')


def target(name, text=''):
    return r'\hypertarget{' + name + '}{' + text + '}'


def link(name, text):
    return r'\hyperlink{' + name + '}{' + text + '}'


def refs(t):
    parts, pos = [], 0
    for m in GOAL.finditer(t):
        parts += [(t[pos:m.start()], True), (m.group(0), False)]
        pos = m.end()
    parts.append((t[pos:], True))
    out = []
    for seg, live in parts:
        if live:
            seg = re.sub(CLAUSE, lambda m: link('nss-' + m.group(1), m.group(0)), seg)
            seg = re.sub(r'\bAppendix ([AB])\b', lambda m: link('nss-app' + m.group(1), m.group(0)), seg)
            seg = re.sub(r'\bGP-(\d\d)\b', lambda m: link('gp-' + m.group(1), m.group(0)), seg)
            seg = re.sub(r'\b(COD|LSA|IMF|VFE|SaC)\b', lambda m: link('gp-' + m.group(1), m.group(0)), seg)
        out.append(seg)
    return ''.join(out)


def plain(s, linked):
    t = esc(s)
    t = re.sub(r'§(?=[A-Za-z])', r'\\S{}', t).replace('§', r'\S')
    return refs(t) if linked else t


def inline(s, linked=False):
    s = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', s)
    s = re.sub(r'\[\[([^\]]+)\]\]', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    out, pos = [], 0
    for m in re.finditer(r'`([^`]+)`|\*\*(.+?)\*\*', s):
        out.append(plain(s[pos:m.start()], linked))
        if m.group(1) is not None:
            out.append(r'\texttt{' + plain(m.group(1), False) + '}')
        else:
            out.append(r'\textbf{' + inline(m.group(2), linked) + '}')
        pos = m.end()
    out.append(plain(s[pos:], linked))
    return ''.join(out)


def table(rows, linked):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    n = len(head)
    widths = [max(len(r[i]) for r in cells if i < len(r)) for i in range(n)]
    total = sum(widths)
    shares = [max(0.12, w / total) for w in widths]
    spec = ' '.join('p{%.3f\\textwidth}' % (0.9 * x / sum(shares)) for x in shares)
    lines = [r'\end{multicols}', r'\begingroup\footnotesize',
             r'\begin{longtable}{@{}' + spec + '@{}}', r'\toprule',
             ' & '.join(r'\textbf{' + inline(h) + '}' for h in head) + r' \\', r'\midrule', r'\endhead']
    lines += [' & '.join(inline(c, linked) for c in r) + r' \\' for r in body]
    lines += [r'\bottomrule', r'\end{longtable}', r'\endgroup', r'\begin{multicols}{2}']
    return lines


def anchor(prefix, heading):
    if not prefix:
        return None
    if heading in PRINCIPLES:
        return 'gp-' + PRINCIPLES[heading]
    m = re.match(r'(\d+(?:\.\d+)?) ', heading)
    if m:
        return prefix + '-' + m.group(1)
    m = re.match(r'Appendix ([A-Z]):', heading)
    if m:
        return prefix + '-app' + m.group(1)
    return None


def convert(md, prefix=None):
    src = md.split('\n')
    out, i = [r'\begin{multicols}{2}'], 0
    while i < len(src):
        line = src[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r'^(#+) (.*)$', line)
        if m:
            level, text = len(m.group(1)), inline(m.group(2))
            name = anchor(prefix, m.group(2))
            if name:
                out.append(target(name))
            if level == 1:
                out.append(r'\noindent{\large\bfseries ' + text + r'}\par\medskip')
            elif level == 2:
                out.append(r'\subsubsection*{' + text + '}')
            else:
                out.append(r'\par\smallskip\noindent\textbf{' + text + r'}\par\nopagebreak')
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(src) and src[i].startswith('|'):
                rows.append(src[i])
                i += 1
            out += table(rows, bool(prefix))
            continue
        for pattern, env in ((r'^[-*] ', 'itemize'), (r'^\d+\. ', 'enumerate')):
            if re.match(pattern, line):
                out.append(r'\begin{' + env + r'}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}')
                while i < len(src) and re.match(pattern, src[i]):
                    out.append(r'\item ' + inline(re.sub(pattern, '', src[i]), bool(prefix)))
                    i += 1
                out.append(r'\end{' + env + '}')
                break
        else:
            para = []
            while i < len(src) and src[i].strip() and not re.match(r'^(#+ |\||[-*] |\d+\. )', src[i]):
                para.append(src[i].strip())
                i += 1
            out.append(inline(' '.join(para), bool(prefix)))
            continue
    out.append(r'\end{multicols}')
    return '\n\n'.join(out) + '\n'


if __name__ == '__main__':
    sys.stdout.write(convert(open(sys.argv[1], encoding='utf-8').read()))
