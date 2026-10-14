import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from md2tex import convert

ROOT = Path(__file__).resolve().parents[2]
GP = ROOT / 'Governing Principles.md'
PSS = ROOT / 'Normative Structural Specification.md'


def paper_source(p):
    return p.read_text(encoding="utf-8").replace("Franz Bruckhoff, Stratington Systems", "Franz Bruckhoff")


def digest(p):
    return hashlib.sha256(paper_source(p).encode("utf-8")).hexdigest()


HEAD = r"""\section{The Framework and Its Core Documents}
\label{app:framework}

\begin{multicols}{2}
The Framework for Keeping Complex Work Coherent Across Time is a system of principles, normative requirements, domain bindings, guidance, and checks for complex engineering work. The current release has five parts.

\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
\item \textbf{Governing Principles}: the principles that define the governing model. Appendix~\ref{app:principles} reproduces them.
\item \textbf{Normative Structural Specification}: the mandatory project architecture that puts the Governing Principles into practice. Appendix~\ref{app:spec} reproduces it.
\item \textbf{Domain Profiles}: bindings of the abstract information model to concrete artifacts, locations, formats, and tools. The current reference bindings are the software profile and a hardware profile for physical systems. Appendix~\ref{app:entities} gives the software reference layout and the hardware differences.
\item \textbf{Guides}: explanatory and adoption material that helps people apply the framework. A guide adds no normative requirement and overrides none.
\item \textbf{Normative Checks}: deterministic checks that enforce the mechanically verifiable requirements of the Specification. The Specification states them in its \hyperlink{nss-16}{\S16}, and Appendix~\ref{app:checks} lists the minimum set.
\end{itemize}

The Governing Principles and the Specification are the domain-general core. The Domain Profiles, the Guides, and the Normative Checks support the use of that core. They do not override it.
\end{multicols}

The two core documents follow as issued, at version~1.0. The SHA-256 digest of each source file identifies the exact text reproduced here:

\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
\item Governing Principles: {\footnotesize\texttt{GPDIGEST}}
\item Normative Structural Specification: {\footnotesize\texttt{PSSDIGEST}}
\end{itemize}

\subsection{Governing Principles}
\label{app:principles}

"""

MID = r"""
\clearpage
\subsection{Normative Structural Specification}
\label{app:spec}

"""

out = sys.argv[1] if len(sys.argv) > 1 else ROOT / 'paper' / 'src' / 'appendix-f.tex'
text = (HEAD.replace('GPDIGEST', digest(GP)).replace('PSSDIGEST', digest(PSS))
        + convert(paper_source(GP), 'gp') + MID + convert(paper_source(PSS), 'nss'))

appendix_b = (ROOT / 'paper' / 'src' / 'appendix-b.tex').read_text(encoding='utf-8')
targets = set(re.findall(r'\\hypertarget\{([^}]+)\}', text + appendix_b))
dangling = sorted(set(re.findall(r'\\hyperlink\{([^}]+)\}', text)) - targets)
if dangling:
    sys.exit('build_appendix_f: links without a target: ' + ', '.join(dangling))
Path(out).write_text(text, encoding='utf-8')
