
TEXBIN := $(HOME)/texlive/bin/universal-darwin
export PATH := $(TEXBIN):$(PATH)

PYTHON := python3
LATEX  := $(TEXBIN)/pdflatex -interaction=nonstopmode -halt-on-error

FIGURES := f01/f01-funnel.pdf f02/f02-verification-loop.pdf \
           f04/f04-entity-model.pdf f03/f03-family-section-matrix.pdf \
           f06/f06-ingestion-pipeline.pdf f05/f05-graph-structure.pdf \
           f08/f08-coverage.pdf f09/f09-relation-graph.pdf \
           f10/f10-dependency-structure.pdf f07/f07-semantic-graph.pdf \
           f11/f11-literature-domains.pdf

DATA := f01/f01-funnel.csv f08/f08-coverage.csv \
       f03/f03-matrix.csv f03/f03-families.csv \
       f05/f05-nodes.csv f05/f05-edges.csv f05/f05-legend.csv f05/f05-levels.csv \
       f09/f09-nodes.csv f09/f09-bands.csv \
       f10/f10-matrix.csv f10/f10-sections.csv \
       f07/f07-semantic-graph-data.tex f07/f07-semantic-graph-anchors.tex \
       f11/f11-cells.csv f11/f11-families.csv f11/f11-domains.csv

IMAGES := $(FIGURES:.pdf=.png)

all: data figures

data: $(DATA)

figures: $(FIGURES)

images: $(IMAGES)

%.png: %.pdf
	pdftocairo -png -r 300 -singlefile $< $(basename $@)

f01/f01-funnel.csv: f01/f01-funnel.py
	$(PYTHON) $<

f08/f08-coverage.csv: f08/f08-coverage.py
	$(PYTHON) $<

f03/f03-matrix.csv f03/f03-families.csv: f03/f03-family-section-matrix.py
	$(PYTHON) $<

f05/f05-nodes.csv f05/f05-edges.csv f05/f05-legend.csv f05/f05-levels.csv: f05/f05-graph-structure.py
	$(PYTHON) $<

f09/f09-nodes.csv f09/f09-bands.csv: f09/f09-relation-graph.py
	$(PYTHON) $<

f10/f10-matrix.csv f10/f10-sections.csv: f10/f10-dependency-structure.py
	$(PYTHON) $<

f11/f11-cells.csv f11/f11-families.csv f11/f11-domains.csv: f11/f11-literature-domains.py
	$(PYTHON) $<

f07/f07-semantic-graph-data.tex f07/f07-semantic-graph-anchors.tex: f07/f07-semantic-graph.py
	$(PYTHON) $<

%.pdf: %.tex
	cd $(dir $<) && $(LATEX) $(notdir $<)

f01/f01-funnel.pdf: f01/f01-funnel.tex f01/f01-funnel.csv
f03/f03-family-section-matrix.pdf: f03/f03-family-section-matrix.tex f03/f03-matrix.csv f03/f03-families.csv
f05/f05-graph-structure.pdf: f05/f05-graph-structure.tex f05/f05-nodes.csv f05/f05-edges.csv f05/f05-legend.csv f05/f05-levels.csv
f08/f08-coverage.pdf: f08/f08-coverage.tex f08/f08-coverage.csv
f09/f09-relation-graph.pdf: f09/f09-relation-graph.tex f09/f09-nodes.csv f09/f09-bands.csv
f10/f10-dependency-structure.pdf: f10/f10-dependency-structure.tex f10/f10-matrix.csv f10/f10-sections.csv
f07/f07-semantic-graph.pdf: f07/f07-semantic-graph.tex f07/f07-semantic-graph-data.tex f07/f07-semantic-graph-anchors.tex
f11/f11-literature-domains.pdf: f11/f11-literature-domains.tex f11/f11-cells.csv f11/f11-families.csv f11/f11-domains.csv

clean:
	rm -f f*/*.aux f*/*.log

.PHONY: all data figures images clean
