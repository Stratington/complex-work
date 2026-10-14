# Long-Horizon AI-Augmented Engineering under Complexity

*An Inquiry into Principles and a Framework for Keeping Complex Work Coherent Across Time*

**[Franz Bruckhoff](https://fbx.io), [Stratington Systems](https://stratington.com) · [think-bigger.org](https://think-bigger.org)** · v1.0

[Read the paper](https://think-bigger.org/framework/paper) · [Apply the framework](https://think-bigger.org/framework/quick-start)

Without sufficient structure, complex work loses its coherence across time. A test can pass even after the requirement it once checked has changed. Across months or years, a project can lose the links between its goals, its contracts, and the evidence used to accept its work, and AI agents may then act on an incomplete record.

The Framework for Keeping Complex Work Coherent Across Time assigns these links to explicit project records. Five engineering principles organize component boundaries, stable requirements, verification, and human authority. The paper gives their basis in recorded engineering practice and examines the resulting requirements and relations.

## Introduction

Watch the introduction to the framework.

https://github.com/user-attachments/assets/aacc0dfb-fbd5-43da-a645-9fbb1e24e08c

## Read and explore

| Resource | Contents |
| --- | --- |
| [Paper](https://think-bigger.org/framework/paper) | The argument, derivation, analysis, and appendices. |
| [Governing Principles](https://think-bigger.org/framework/principles) | The five principles and the reasons for each. |
| [Normative Structural Specification](https://think-bigger.org/framework/specification) | Requirements for project records, verification, traceability, and human authority. |
| [LaTeX sources](paper/src/) | The paper source, bibliography, and style. Start with `main.tex`. |
| [Figures](paper/src/figures/README.md#figures) | The eleven figures as images, with standalone LaTeX sources, vector PDFs, and the data and generators used for the data figures. |

## Build

Install TeX Live with `latexmk`, `pgfplots`, and `standalone`. The paper also uses `xcolor`, `booktabs`, `microtype`, `preprint`, `background`, `scalerel`, `pgf`, `xkeyval`, `everypage`, `times`, and `courier`. Put the TeX Live binaries on your `PATH`.

Run these commands from the repository root. The first command marks the committed data as current, so the figure build uses those files without running their generators.

```sh
make -C paper/src/figures -t data
make -C paper/src/figures figures TEXBIN="$(dirname "$(command -v pdflatex)")"
(cd paper/src && latexmk main.tex)
```

The paper PDF is written to `paper/main.pdf`. The figure generators require external project data that is not included in this repository. See the [figure build instructions](paper/src/figures/README.md) for the data sources and tools. `make -C paper/src/figures images` renders the PNG images from the figure PDFs, with `pdftocairo` from Poppler.

### Appendix F

Python 3 regenerates Appendix F from the two Markdown documents at the repository root:

```sh
python3 paper/bin/build_appendix_f.py
```

The generator reproduces the document text and the author credits in the paper. Edit its source documents and generator rather than the generated appendix.

## License

The paper and the two framework documents are licensed under [CC BY-SA 4.0](LICENSE). The two-column style comes from [brenhinkeller/preprint-template.tex](https://github.com/brenhinkeller/preprint-template.tex) and retains its [CC BY 4.0 license](paper/src/LICENSE.preprint-template).
