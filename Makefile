.PHONY: all clean ttf web pack check

NAME=amiri
VERSION=0.104

TOOLS=tools
SRC=sources
WEB=web
DOC=documentation
TESTS=test-suite
FONTS=$(NAME)-regular $(NAME)-quran $(NAME)-bold $(NAME)-slanted $(NAME)-boldslanted
DOCS=README README-Arabic NEWS NEWS-Arabic
DIST=$(NAME)-$(VERSION)

BUILD=$(TOOLS)/build.py
RUNTEST=$(TOOLS)/runtest.py
FF=python $(BUILD)
SFNTTOOL=sfnttool
PP=gpp +c "/*" "*/" +c "//" "\n" +c "\\\n" "" -I$(SRC)

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WTTF=$(FONTS:%=$(WEB)/%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
EOTS=$(FONTS:%=$(WEB)/%.eot)
PDFS=$(DOC)/$(NAME)-table.pdf
HTML=$(DOC)/documentation-arabic.html
CSSS=$(WEB)/$(NAME).css
FEAT=$(wildcard $(SRC)/*.fea)
TEST=$(wildcard $(TESTS)/*.test)
TEST+=$(wildcard $(TESTS)/*.ptest)

DOCFILES=$(DOCS:%=$(DOC)/%.txt)
license=OFL.txt OFL-FAQ.txt

all: ttf web

ttf: $(DTTF)
web: $(WTTF) $(WOFF) $(EOTS) $(CSSS)
doc: $(PDFS) $(HTML)

$(NAME)-quran.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/crimson/Crimson-Roman.sfd $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(PP) -DQURAN $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-quran.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-quran.fea.pp --version $(VERSION) --quran

$(NAME)-regular.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/crimson/Crimson-Roman.sfd $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(PP) $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-regular.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-regular.fea.pp --version $(VERSION)

$(NAME)-slanted.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/crimson/Crimson-Italic.sfd $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(PP) -DITALIC $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-slanted.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-slanted.fea.pp --version $(VERSION) --slant=7

$(NAME)-bold.ttf: $(SRC)/$(NAME)-bold.sfdir $(SRC)/crimson/Crimson-Bold.sfd $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(PP) $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-bold.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-bold.fea.pp --version $(VERSION)

$(NAME)-boldslanted.ttf: $(SRC)/$(NAME)-bold.sfdir $(SRC)/crimson/Crimson-BoldItalic.sfd $(SRC)/$(NAME).fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(PP) -DITALIC $(SRC)/$(NAME).fea -o $(SRC)/$(NAME)-boldslanted.fea.pp
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME)-boldslanted.fea.pp --version $(VERSION) --slant=7

$(WEB)/%.ttf: %.ttf $(BUILD)
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(FF) --input $< --output $@ --web 1>/dev/null 2>&1

$(WEB)/%.woff: $(WEB)/%.ttf
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(SFNTTOOL) -w $< $@

$(WEB)/%.eot: $(WEB)/%.ttf
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(SFNTTOOL) -e -x $< $@

$(WEB)/%.css: $(WTTF) $(BUILD)
	@echo "   GEN\t$@"
	@mkdir -p $(WEB)
	@$(FF) --css --input "$(WTTF)" --output $@ --version $(VERSION)

$(DOC)/$(NAME)-table.pdf: $(NAME)-regular.ttf
	@echo "   GEN\t$@"
	@mkdir -p $(DOC)
	@fntsample --font-file $< --output-file $@.tmp --print-outline > $@.txt
	@pdfoutline $@.tmp $@.txt $@
	@rm -f $@.tmp $@.txt

$(DOC)/documentation-arabic.html: $(DOC)/documentation-sources/documentation-arabic.md
	@echo "   GEN\t$@"
	@pandoc $< -o $@ -f markdown -t html -s -c documentation-arabic.css --toc

check: $(TEST) $(DTTF)
ifeq ($(shell which hb-shape),)
	@echo "hb-shape not found, skipping tests"
else
	@echo "running tests"
	@$(RUNTEST) $(TEST)
endif

clean:
	rm -rfv $(DTTF) $(WTTF) $(WOFF) $(EOTS) $(CSSS) $(PDFS) $(SRC)/$(NAME).fea.pp

#->8-
PACK=$(SRC)/$(NAME)-regular.sfd $(SRC)/$(NAME)-bold.sfd

pack: $(PACK)

%.sfd: %.sfdir
	@echo "   GEN\t$@"
	@python -c 'import fontforge; f=fontforge.open("$<"); f.save("$@")'

distclean:
	@rm -rf $(DIST) $(DIST).tar.bz2
	@rm -rf $(PACK)

dist: all check pack doc
	@echo "   Making dist tarball"
	@mkdir -p $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(WEB)
	@mkdir -p $(DIST)/$(DOC)
	@mkdir -p $(DIST)/$(TOOLS)
	@mkdir -p $(DIST)/$(TESTS)
	@cp $(PACK) $(DIST)/$(SRC)
	@cp $(FEAT) $(DIST)/$(SRC)
	@mkdir -p $(DIST)/$(SRC)/crimson
	@cp -r $(SRC)/crimson/Crimson-*.sfd $(DIST)/$(SRC)/crimson
	@cp -r $(SRC)/crimson/README $(DIST)/$(SRC)/crimson
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
	@cp $(TEST) $(DIST)/$(TESTS)
	@cp $(BUILD) $(DIST)/$(TOOLS)
	@cp $(RUNTEST) $(DIST)/$(TOOLS)
	@tar cfj $(DIST).tar.bz2 $(DIST)
	@tar cfj $(DIST)-ctan.tar.bz2 $(DIST) --exclude "$(WEB)*"
