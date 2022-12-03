.PHONY: all clean ttf web pack check

NAME=Amiri
LATIN=AmiriLatin
TAG=$(shell git describe --tags --abbrev=0)
VERSION=$(TAG:v%=%)

SRC=sources
BUILDDIR=build
SCRIPTSDIR=scripts
FONTSDIR=fonts
DOC=documentation
FONTS=$(NAME)-Regular $(NAME)-Bold $(NAME)-Slanted $(NAME)-BoldSlanted $(NAME)Quran $(NAME)QuranColored
DIST=$(NAME)-$(VERSION)
LICENSE=OFL.txt

BUILD=${SCRIPTSDIR}/build.py
MAKEQURAN=${SCRIPTSDIR}/mkquran.py
PY ?= python

TTF=$(FONTS:%=${FONTSDIR}/%.ttf)
HTML=$(DOC)/Documentation-Arabic.html
FEA=$(wildcard $(SRC)/*.fea)

export SOURCE_DATE_EPOCH ?= 0

all: ttf

ttf: $(TTF)
doc: $(HTML)

$(BUILDDIR)/$(NAME).designspace: $(SRC)/$(NAME).glyphs
	@echo "   UFO	$@"
	@glyphs2ufo --minimal --generate-GDEF --output-dir=$(BUILDDIR) $<

$(BUILDDIR)/%.ufo: $(BUILDDIR)/$(NAME).designspace
	@echo "   UFO	$@"

${FONTSDIR}/$(NAME)QuranColored.ttf: $(BUILDDIR)/$(NAME)-Regular.ufo $(SRC)/$(LATIN)-Regular.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   GEN	$@"
	@$(PY) $(BUILD) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE) --quran

${FONTSDIR}/$(NAME)Quran.ttf: ${FONTSDIR}/$(NAME)QuranColored.ttf $(MAKEQURAN)
	@echo "   GEN	$@"
	@$(PY) $(MAKEQURAN) $< $@

${FONTSDIR}/$(NAME)-Regular.ttf: $(BUILDDIR)/$(NAME)-Regular.ufo $(SRC)/$(LATIN)-Regular.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   GEN	$@"
	@$(PY) $(BUILD) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE)

${FONTSDIR}/$(NAME)-Slanted.ttf: $(BUILDDIR)/$(NAME)-Regular.ufo $(SRC)/$(LATIN)-Slanted.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   GEN	$@"
	@$(PY) $(BUILD) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE) --slant=10

${FONTSDIR}/$(NAME)-Bold.ttf: $(BUILDDIR)/$(NAME)-Bold.ufo $(SRC)/$(LATIN)-Bold.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   GEN	$@"
	@$(PY) $(BUILD) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE)

${FONTSDIR}/$(NAME)-BoldSlanted.ttf: $(BUILDDIR)/$(NAME)-Bold.ufo $(SRC)/$(LATIN)-BoldSlanted.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   GEN	$@"
	@$(PY) $(BUILD) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE) --slant=10

$(DOC)/Documentation-Arabic.html: $(DOC)/Documentation-Arabic.md
	@echo "   GEN	$@"
	@pandoc $< -o $@ -f markdown-smart -t html -s -c Documentation-Arabic.css

check: $(TTF)
	@$(foreach font,$+,echo "   OTS	$(font)" && python -m ots --quiet $(font) &&) true

clean:
	rm -rfv $(TTF) $(HTML)

distclean: clean
	rm -rf $(DIST){,.zip}

dist: ttf check pack doc
	@echo "   DIST	$(DIST)"
	@rm -rf $(DIST){,.zip}
	@install -Dm644 -t $(DIST) $(LICENSE)
	@install -Dm644 -t $(DIST) $(TTF)
	@install -Dm644 -t $(DIST) README.md
	@install -Dm644 -t $(DIST) README-Arabic.md
	@install -Dm644 -t $(DIST) NEWS.md
	@install -Dm644 -t $(DIST) NEWS-Arabic.md
	@install -Dm644 -t $(DIST) $(HTML)
	@echo "   DROP GLYPH NAMES"
	@$(PY) ${SCRIPTSDIR}/no-glyphnames.py $(DIST)/*.ttf
	@echo "   ZIP  $(DIST)"
	@zip -rq $(DIST).zip $(DIST)
