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
PY ?= python
FF=$(PY) $(BUILD)

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
DOTF=$(FONTS:%=%.otf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
WOF2=$(FONTS:%=$(WEB)/%.woff2)
CSSS=$(WEB)/$(NAME).css
PDFS=$(DOC)/Documentation-Arabic.pdf
FEAT=$(wildcard $(SRC)/*.fea)
TEST=$(wildcard $(TESTS)/*.test)
TEST+=$(wildcard $(TESTS)/*.ptest)

export SOURCE_DATE_EPOCH ?= 0

all: ttf web

ttf: $(DTTF)
otf: $(DOTF)
web: $(WOFF) $(WOF2) $(CSSS)
doc: $(PDFS)

$(NAME)Quran.ttf $(NAME)Quran.otf: $(SRC)/$(NAME)-Regular.sfdir $(SRC)/latin/$(LATIN)-Regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --quran

$(NAME)QuranColored.ttf: $(NAME)Quran.ttf $(MAKECLR)
	@echo "   FF	$@"
	@$(PY) $(MAKECLR) $< $@

$(NAME)QuranColored.otf: $(NAME)Quran.otf $(MAKECLR)
	@echo "   FF	$@"
	@$(PY) $(MAKECLR) $< $@

$(NAME)-Regular.ttf $(NAME)-Regular.otf: $(SRC)/$(NAME)-Regular.sfdir $(SRC)/latin/$(LATIN)-Regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION)

$(NAME)-Slanted.ttf $(NAME)-Slanted.otf: $(SRC)/$(NAME)-Regular.sfdir $(SRC)/latin/$(LATIN)-Italic.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --slant=10

$(NAME)-Bold.ttf $(NAME)-Bold.otf: $(SRC)/$(NAME)-Bold.sfdir $(SRC)/latin/$(LATIN)-Bold.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION)

$(NAME)-BoldSlanted.ttf $(NAME)-BoldSlanted.otf: $(SRC)/$(NAME)-Bold.sfdir $(SRC)/latin/$(LATIN)-BoldItalic.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --slant=10

$(WEB)/%.woff $(WEB)/%.woff2: %.ttf $(MAKEWEB)
	@echo "   WEB	$*"
	@mkdir -p $(WEB)
	@$(PY) $(MAKEWEB) $< $(WEB)

$(WEB)/%.css: $(WOFF) $(MAKECSS)
	@echo "   GEN	$@"
	@mkdir -p $(WEB)
	@$(PY) $(MAKECSS) --css=$@ --fonts="$(WOFF)"

$(DOC)/Documentation-Arabic.pdf: $(DOC)/Documentation-Arabic.tex $(DTTF)
	@echo "   GEN	$@"
	@latexmk --norc --xelatex --quiet --output-directory=${DOC} $<

check: $(TEST) $(DTTF)
	@echo "running tests"
	@$(foreach font,$(DTTF),echo "   OTS	$(font)" && python -m ots --quiet $(font) &&) true
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
