.PHONY: all clean ttf web pack check

NAME=Amiri
LATIN=AmiriLatin
VERSION=0.112

TOOLS=tools
SRC=sources
WEB=webfonts
DOC=documentation
TESTS=test-suite
FONTS=$(NAME)-Regular $(NAME)-Bold $(NAME)-Slanted $(NAME)-BoldSlanted $(NAME)Quran $(NAME)QuranColored
DIST=$(NAME)-$(VERSION)
WDIST=$(NAME)-$(VERSION)-WebFonts
CDIST=$(NAME)-$(VERSION)-CTAN

BUILD=$(TOOLS)/build.py
RUNTEST=$(TOOLS)/runtest.py
MAKECLR=$(TOOLS)/makeclr.py
MAKECSS=$(TOOLS)/makecss.py
MAKEWEB=$(TOOLS)/makeweb.py
PY ?= python3
PY2 ?= python2
FF=$(PY2) $(BUILD)
PP=gpp -I$(SRC)

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
WOF2=$(FONTS:%=$(WEB)/%.woff2)
CSSS=$(WEB)/$(NAME).css
PDFS=$(DOC)/FontTable-$(NAME).pdf $(DOC)/FontTable-$(NAME)Quran.pdf $(DOC)/Documentation-Arabic.pdf
FEAT=$(wildcard $(SRC)/*.fea)
TEST=$(wildcard $(TESTS)/*.test)
TEST+=$(wildcard $(TESTS)/*.ptest)

all: ttf web

ttf: $(DTTF)
web: $(WOFF) $(WOF2) $(CSSS)
doc: $(PDFS)

$(NAME)Quran.ttf: $(SRC)/$(NAME)-Regular.sfdir $(SRC)/latin/$(LATIN)-Regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DQURAN $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)Quran.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)Quran.fea.pp --version $(VERSION) --quran

$(NAME)QuranColored.ttf: $(NAME)Quran.ttf $(MAKECLR)
	@echo "   FF	$@"
	@$(PY) $(MAKECLR) $< $@

$(NAME)-Regular.ttf: $(SRC)/$(NAME)-Regular.sfdir $(SRC)/latin/$(LATIN)-Regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-Regular.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-Regular.fea.pp --version $(VERSION)

$(NAME)-Slanted.ttf: $(SRC)/$(NAME)-Regular.sfdir $(SRC)/latin/$(LATIN)-Italic.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DITALIC $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-Slanted.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-Slanted.fea.pp --version $(VERSION) --slant=10

$(NAME)-Bold.ttf: $(SRC)/$(NAME)-Bold.sfdir $(SRC)/latin/$(LATIN)-Bold.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-Bold.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-Bold.fea.pp --version $(VERSION)

$(NAME)-BoldSlanted.ttf: $(SRC)/$(NAME)-Bold.sfdir $(SRC)/latin/$(LATIN)-BoldItalic.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DITALIC $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-BoldSlanted.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-BoldSlanted.fea.pp --version $(VERSION) --slant=10

$(WEB)/%.woff $(WEB)/%.woff2: %.ttf $(MAKEWEB)
	@echo "   WEB	$*"
	@mkdir -p $(WEB)
	@$(PY) $(MAKEWEB) $< $(WEB)

$(WEB)/%.css: $(WOFF) $(MAKECSS)
	@echo "   GEN	$@"
	@mkdir -p $(WEB)
	@$(PY) $(MAKECSS) --css=$@ --fonts="$(WOFF)"

$(DOC)/FontTable-$(NAME)Quran.pdf: $(NAME)Quran.ttf
	@echo "   GEN	$@"
	@mkdir -p $(DOC)
	@fntsample --font-file $< --output-file $@ --write-outline --use-pango

$(DOC)/FontTable-$(NAME).pdf: $(NAME)-Regular.ttf
	@echo "   GEN	$@"
	@mkdir -p $(DOC)
	@fntsample --font-file $< --output-file $@ --write-outline --use-pango

$(DOC)/Documentation-Arabic.pdf: $(DOC)/Documentation-Arabic.tex $(DTTF)
	@echo "   GEN	$@"
	@latexmk --norc --xelatex --quiet --output-directory=${DOC} $<

check: $(TEST) $(DTTF)
	@echo "running tests"
	@$(foreach font,$(DTTF),echo "   OTS	$(font)" && ots-sanitize --quiet $(font) &&) true
	@$(PY) $(RUNTEST) $(TEST)

clean:
	rm -rfv $(DTTF) $(WOFF) $(WOF2) $(CSSS) $(PDFS) $(SRC)/$(NAME)*.fea.pp
	rm -rfv $(DOC)/documentation-arabic.{aux,log,toc}

distclean: clean
	rm -rf {$(DIST),$(CDIST),$(WDIST)}{,.zip}

dist: all check pack doc
	@rm -rf $(DIST) $(CDIST) $(WDIST)
	@mkdir -p $(DIST) $(CDIST) $(WDIST)
	@cp OFL.txt $(DIST)
	@cp OFL.txt $(CDIST)
	@cp OFL.txt $(WDIST)
	@cp $(DTTF) $(DIST)
	@cp $(DTTF) $(CDIST)
	@cp README.md $(DIST)/README
	@cp README.md $(CDIST)/README
	@cp README-Arabic.md $(DIST)/README-Arabic
	@cp README-Arabic.md $(CDIST)/README-Arabic
	@cp NEWS.md $(DIST)/NEWS
	@cp NEWS.md $(CDIST)/NEWS
	@cp NEWS-Arabic.md $(DIST)/NEWS-Arabic
	@cp NEWS-Arabic.md $(CDIST)/NEWS-Arabic
	@cp $(NAME).fontspec $(CDIST)
	@cp $(WOFF) $(WDIST)
	@cp $(WOF2) $(WDIST)
	@cp $(CSSS) $(WDIST)
	@cp $(WEB)/README $(WDIST)
	@cp $(PDFS) $(DIST)
	@cp $(PDFS) $(CDIST)
	@echo "   ZIP  $(DIST)"
	@zip -rq $(DIST).zip $(DIST)
	@echo "   ZIP  $(CDIST)"
	@zip -rq $(CDIST).zip $(CDIST)
	@echo "   ZIP  $(WDIST)"
	@zip -rq $(WDIST).zip $(WDIST)
