.PHONY: all clean ttf web pack check

NAME=amiri
VERSION=0.108

TOOLS=tools
SRC=sources
WEB=webfonts
DOC=documentation
TESTS=test-suite
FONTS=$(NAME)-regular $(NAME)-quran $(NAME)-quran-colored $(NAME)-bold $(NAME)-slanted $(NAME)-boldslanted
DIST=$(NAME)-$(VERSION)
WDIST=$(NAME)-$(VERSION)-webfonts

BUILD=$(TOOLS)/build.py
RUNTEST=$(TOOLS)/runtest.py
MAKECLR=$(TOOLS)/makeclr.py
MAKECSS=$(TOOLS)/makecss.py
MAKEWEB=$(TOOLS)/makeweb.py
PY=python2.7
FF=$(PY) $(BUILD)
SFNTTOOL=sfnttool
WOFF2_COMPRESS=woff2_compress
PP=gpp -I$(SRC)

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WTTF=$(FONTS:%=$(WEB)/%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
WOF2=$(FONTS:%=$(WEB)/%.woff2)
EOTS=$(FONTS:%=$(WEB)/%.eot)
CSSS=$(WEB)/$(NAME).css
PDFS=$(DOC)/$(NAME)-table.pdf $(DOC)/documentation-arabic.pdf
FEAT=$(wildcard $(SRC)/*.fea)
TEST=$(wildcard $(TESTS)/*.test)
TEST+=$(wildcard $(TESTS)/*.ptest)

all: ttf web

ttf: $(DTTF)
web: $(WTTF) $(WOFF) $(WOF2) $(EOTS) $(CSSS)
doc: $(PDFS)

$(NAME)-quran.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/latin/amirilatin-regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DQURAN $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-quran.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-quran.fea.pp --version $(VERSION) --quran

$(NAME)-quran-colored.ttf: $(NAME)-quran.ttf $(MAKECLR)
	@echo "   FF	$@"
	@$(PY) $(MAKECLR) $< $@

$(NAME)-regular.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/latin/amirilatin-regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-regular.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-regular.fea.pp --version $(VERSION)

$(NAME)-slanted.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/latin/amirilatin-italic.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DITALIC $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-slanted.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-slanted.fea.pp --version $(VERSION) --slant=10

$(NAME)-bold.ttf: $(SRC)/$(NAME)-bold.sfdir $(SRC)/latin/amirilatin-bold.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-bold.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-bold.fea.pp --version $(VERSION)

$(NAME)-boldslanted.ttf: $(SRC)/$(NAME)-bold.sfdir $(SRC)/latin/amirilatin-bolditalic.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DITALIC $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-boldslanted.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-boldslanted.fea.pp --version $(VERSION) --slant=10

$(WEB)/%.ttf: %.ttf $(MAKEWEB)
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(PY) $(MAKEWEB) $< $@ 1>/dev/null 2>&1

$(WEB)/%.woff: $(WEB)/%.ttf
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(SFNTTOOL) -w $< $@

$(WEB)/%.woff2: $(WEB)/%.ttf
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(WOFF2_COMPRESS) $< 1>/dev/null

$(WEB)/%.eot: $(WEB)/%.ttf
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(SFNTTOOL) -e -x $< $@

$(WEB)/%.css: $(WTTF) $(MAKECSS)
	@echo "   GEN	$@"
	@mkdir -p $(WEB)
	@$(PY) $(MAKECSS) --css=$@ --fonts="$(WTTF)"

$(DOC)/$(NAME)-table.pdf: $(NAME)-regular.ttf
	@echo "   GEN	$@"
	@mkdir -p $(DOC)
	@fntsample --font-file $< --output-file $@.tmp --print-outline > $@.txt
	@pdfoutline $@.tmp $@.txt $@
	@rm -f $@.tmp $@.txt

$(DOC)/documentation-arabic.pdf: $(DOC)/documentation-arabic.tex $(DTTF)
	@echo "   GEN	$@"
	@latexmk --norc --xelatex --quiet --output-directory=${DOC} $<

check: $(TEST) $(DTTF)
	@echo "running tests"
	@$(foreach font,$(DTTF),echo "   OTS	$(font)" && ot-sanitise $(font) &&) true
	@$(PY) $(RUNTEST) $(TEST)

clean:
	rm -rfv $(DTTF) $(WTTF) $(WOFF) $(WOF2) $(EOTS) $(CSSS) $(PDFS) $(SRC)/$(NAME).fea.pp
	rm -rfv $(DOC)/documentation-arabic.{aux,log,toc}

distclean:
	@rm -rf $(DIST) $(DIST).zip $(WDIST) $(WDIST).zip

dist: all check pack doc
	@echo "   Making dist tarball"
	@mkdir -p $(DIST)
	@mkdir -p $(WDIST)
	@cp OFL.txt $(DIST)
	@cp OFL.txt $(WDIST)
	@cp $(DTTF) $(DIST)
	@cp README.md $(DIST)/README
	@cp README-Arabic.md $(DIST)/README-Arabic
	@cp NEWS.md $(DIST)/NEWS
	@cp NEWS-Arabic.md $(DIST)/NEWS-Arabic
	@cp $(WTTF) $(WDIST)
	@cp $(WOFF) $(WDIST)
	@cp $(WOF2) $(WDIST)
	@cp $(EOTS) $(WDIST)
	@cp $(CSSS) $(WDIST)
	@cp $(WEB)/README $(WDIST)
	@cp $(PDFS) $(DIST)
	@zip -r $(DIST).zip $(DIST)
	@zip -r $(WDIST).zip $(WDIST)
