.PHONY: all clean ttf web pack check

NAME=amiri
VERSION=0.101

TOOLS=tools
SRC=sources
WEB=web
DOC=documentation
TESTS=test-suite
FONTS=$(NAME)-regular $(NAME)-bold $(NAME)-slanted $(NAME)-boldslanted
DOCS=README README-Arabic NEWS NEWS-Arabic
DIST=$(NAME)-$(VERSION)

BUILD=$(TOOLS)/build.py
RUNTEST=$(TOOLS)/runtest.py
FF=python $(BUILD)
MKEOT=ttf2eot
MKWOFF=sfnt2woff

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WTTF=$(FONTS:%=$(WEB)/%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
EOTS=$(FONTS:%=$(WEB)/%.eot)
PDFS=$(DOC)/$(NAME)-table.pdf
CSSS=$(WEB)/$(NAME).css
FEAT=$(wildcard $(SRC)/*.fea)
TEST=$(wildcard $(TESTS)/*.test)

DOCFILES=$(DOCS:%=$(DOC)/%.txt)
license=OFL.txt OFL-FAQ.txt

all: ttf web

ttf: $(DTTF)
web: $(WTTF) $(WOFF) $(EOTS) $(CSSS)
doc: $(PDFS)

$(WEB)/%.ttf: %.ttf $(BUILD)
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(FF) --input $< --output $@ --web

%.ttf: $(SRC)/%.sfdir $(SRC)/%.fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(FF) --input $< --output $@ --version $(VERSION)

$(NAME)-slanted.ttf: $(SRC)/$(NAME)-regular.sfdir $(SRC)/$(NAME)-regular.fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(FF) --input $< --output $@ --version $(VERSION) --slant=7

$(NAME)-boldslanted.ttf: $(SRC)/$(NAME)-bold.sfdir $(SRC)/$(NAME)-bold.fea $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(FF) --input $< --output $@ --version $(VERSION) --slant=7

$(WEB)/%.woff: $(WEB)/%.ttf
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(MKWOFF) $<

$(WEB)/%.eot: $(WEB)/%.ttf
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(MKEOT) $< > $@

$(WEB)/%.css: $(WTTF) $(BUILD)
	@echo "   GEN\t$@"
	@mkdir -p $(WEB)
	@$(FF) --css --input "$(WTTF)" --output $@ --version $(VERSION)

$(DOC)/$(NAME)-table.pdf: $(NAME)-regular.ttf
	@echo "   GEN\t$@"
	@mkdir -p $(DOC)
	@fntsample --exclude-range 0x25A0-0x25FF --font-file $< --output-file $@.tmp --print-outline > $@.txt
	@pdfoutline $@.tmp $@.txt $@
	@rm -f $@.tmp $@.txt

check: $(TEST) $(DTTF)
ifeq ($(shell which hb-shape),)
	@echo "hb-shape not found, skipping tests"
else
	@echo "running tests"
	@$(RUNTEST) $(TEST)
endif

clean:
	rm -rfv $(DTTF) $(WTTF) $(WOFF) $(EOTS) $(CSSS) $(PDFS)

#->8-
PACK=$(SRC)/$(NAME)-regular.sfd $(SRC)/$(NAME)-bold.sfd

pack: $(PACK)

%.sfd: %.sfdir
	@echo "   GEN\t$@"
	@fontforge -lang=ff -c 'Open("$<"); Save("$@");'

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
