.PHONY: all clean ttf web pack check

NAME=amiri
VERSION=0.108

TOOLS=tools
SRC=sources
WEB=webfonts
DOC=documentation
TESTS=test-suite
FONTS=$(NAME)-regular $(NAME)-quran $(NAME)-bold $(NAME)-slanted $(NAME)-boldslanted
DOCS=README README-Arabic NEWS NEWS-Arabic
DIST=$(NAME)-$(VERSION)

BUILD=$(TOOLS)/build.py
RUNTEST=$(TOOLS)/runtest.py
CHECKBLANKS=$(TOOLS)/checkblankglyphs.py
PY=python
FF=$(PY) $(BUILD)
SFNTTOOL=sfnttool
PP=gpp +c "/*" "*/" +c "//" "\n" +c "\\\n" "" -I$(SRC)

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WTTF=$(FONTS:%=$(WEB)/%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
EOTS=$(FONTS:%=$(WEB)/%.eot)
CSSS=$(WEB)/$(NAME).css
PDFS=$(DOC)/$(NAME)-table.pdf $(DOC)/documentation-arabic.pdf
FEAT=$(wildcard $(SRC)/*.fea)
TEST=$(wildcard $(TESTS)/*.test)
TEST+=$(wildcard $(TESTS)/*.ptest)

DOCFILES=$(DOCS:%=$(DOC)/%.txt)
license=OFL.txt OFL-FAQ.txt

all: ttf web

ttf: $(DTTF)
web: $(WTTF) $(WOFF) $(EOTS) $(CSSS)
doc: $(PDFS)

$(NAME)-quran.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/latin/amirilatin-regular.sfdir $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF	$@"
	@$(PP) -DQURAN $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-quran.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-quran.fea.pp --version $(VERSION) --quran

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

$(WEB)/%.ttf: %.ttf $(BUILD)
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(FF) --input $< --output $@ --web 1>/dev/null 2>&1

$(WEB)/%.woff: $(WEB)/%.ttf
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(SFNTTOOL) -w $< $@

$(WEB)/%.eot: $(WEB)/%.ttf
	@echo "   FF	$@"
	@mkdir -p $(WEB)
	@$(SFNTTOOL) -e -x $< $@

$(WEB)/%.css: $(WTTF) $(BUILD)
	@echo "   GEN	$@"
	@mkdir -p $(WEB)
	@$(FF) --css --input "$(WTTF)" --output $@ --version $(VERSION)

$(DOC)/$(NAME)-table.pdf: $(NAME)-regular.ttf
	@echo "   GEN	$@"
	@mkdir -p $(DOC)
	@fntsample --font-file $< --output-file $@.tmp --print-outline > $@.txt
	@pdfoutline $@.tmp $@.txt $@
	@rm -f $@.tmp $@.txt

$(DOC)/documentation-arabic.pdf: $(DOC)/$(DOC)-$(SRC)/documentation-arabic.tex
	@echo "   GEN	$@"
	@latexmk --norc --xelatex --quiet --output-directory=${DOC} $<

check: $(TEST) $(DTTF)
	@echo "running tests"
	@$(foreach font,$(DTTF),echo -e "BLANKS\t$(font)" && $(PY) $(CHECKBLANKS) $(font) 1>/dev/null 2>&1 &&) true
	@$(foreach font,$(DTTF),echo -e "OTS\t$(font)" && ot-sanitise $(font) &&) true
	@$(PY) $(RUNTEST) $(TEST)

clean:
	rm -rfv $(DTTF) $(WTTF) $(WOFF) $(EOTS) $(CSSS) $(PDFS) $(SRC)/$(NAME).fea.pp
	rm -rfv $(DOC)/documentation-arabic.{aux,log,toc}

#->8-
PACK=$(SRC)/$(NAME)-regular.sfd $(SRC)/$(NAME)-bold.sfd

pack: $(PACK)

%.sfd: %.sfdir
	@echo "   GEN	$@"
	@python -c 'import fontforge; f=fontforge.open("$<"); f.save("$@")'

distclean:
	@rm -rf $(DIST) $(DIST).zip
	@rm -rf $(PACK)

dist: all check pack doc
	@echo "   Making dist tarball"
	@mkdir -p $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(WEB)
	@mkdir -p $(DIST)/$(DOC)
	@mkdir -p $(DIST)/$(DOC)/$(DOC)-$(SRC)
	@mkdir -p $(DIST)/$(TOOLS)
	@mkdir -p $(DIST)/$(TESTS)
	@cp $(PACK) $(DIST)/$(SRC)
	@cp $(FEAT) $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(SRC)/latin
	@cp -r $(SRC)/latin/amirilatin-*.sfdir $(DIST)/$(SRC)/latin
	@cp -r $(SRC)/latin/README $(DIST)/$(SRC)/latin
	@sed -e "/#->8-/,$$ d" -e "s/sfdir/sfd/" Makefile > $(DIST)/Makefile
	@cp $(license) $(DIST)
	@cp $(DTTF) $(DIST)
	@cp README.txt $(DIST)
	@cp $(DOCFILES) $(DIST)/$(DOC)
	@cp $(WTTF) $(DIST)/$(WEB)
	@cp $(WOFF) $(DIST)/$(WEB)
	@cp $(EOTS) $(DIST)/$(WEB)
	@cp $(CSSS) $(DIST)/$(WEB)
	@cp $(WEB)/README $(DIST)/$(WEB)
	@cp $(PDFS) $(DIST)/$(DOC)
	@cp $(DOC)/$(DOC)-$(SRC)/documentation-arabic.tex $(DIST)/$(DOC)/$(DOC)-$(SRC)
	@cp $(TEST) $(DIST)/$(TESTS)
	@cp $(BUILD) $(DIST)/$(TOOLS)
	@cp $(RUNTEST) $(DIST)/$(TOOLS)
	@zip -r $(DIST).zip $(DIST)
	@tar cfj $(DIST)-ctan.tar.bz2 $(DIST) --exclude "$(WEB)*"
