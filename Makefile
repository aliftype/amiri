.PHONY: all clean ttf web pack check

VERSION=0.017

TOOLS=tools
SRC=sources
WEB=web
DOC=documentation
TESTS=test-suite
FONTS=amiri-regular
# the order of feature files is important
FEA=lang classes locl ccmp gsub quran tnum rtlm lellah calt kern
DOCS=README README-Arabic NEWS NEWS-Arabic

BUILD=$(TOOLS)/build.py
RUNTEST=$(TOOLS)/runtest.py
FF=python $(BUILD)
MKEOT=ttf2eot

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WTTF=$(FONTS:%=$(WEB)/%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
EOTS=$(FONTS:%=$(WEB)/%.eot)
PDFS=$(FONTS:%=$(DOC)/%-table.pdf)
CSSS=$(WEB)/amiri.css
FEAT=$(FEA:%=$(SRC)/%.fea)
TEST=$(wildcard $(TESTS)/*.test)

DOCFILES=$(DOCS:%=$(DOC)/%.txt)
license=OFL.txt OFL-FAQ.txt

all: ttf web

ttf: $(DTTF)
web: $(WTTF) $(WOFF) $(EOTS) $(CSSS)
table: $(PDFS)

%.ttf: $(SRC)/%.sfdir $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@$(FF) --input $< --output $@ --feature-files "$(FEAT)" --version $(VERSION) --no-localised-name

$(WEB)/%.ttf: $(SRC)/%.sfdir $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(FF) --web --input $< --output $@ --feature-files "$(FEAT)" --version $(VERSION)

$(WEB)/%.woff: $(SRC)/%.sfdir $(FEAT) $(BUILD)
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(FF) --web --input $< --output $@ --feature-files "$(FEAT)" --version $(VERSION)

$(WEB)/%.eot: $(WEB)/%.ttf
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(MKEOT) $< > $@

$(WEB)/%.css: $(SFDS) $(BUILD)
	@echo "   GEN\t$@"
	@mkdir -p $(WEB)
	@$(FF) --css --input $^ --output $@ --version $(VERSION)

$(DOC)/%-table.pdf: %.ttf
	@echo "   GEN\t$@"
	@mkdir -p $(DOC)
	@fntsample --font-file $< --output-file $@.tmp --print-outline > $@.txt
	@pdfoutline $@.tmp $@.txt $@

check: $(TEST)
	@echo "running tests"
	@$(RUNTEST) $^

clean:
	@rm -rf $(DTTF) $(WTTF) $(WOFF) $(EOTS) $(CSSS)

#->8-
PACK=$(SFDS:.sfdir=.sfd)

pack: $(PACK)

%.sfd: %.sfdir $(BUILD)
	@echo "   GEN\t$@"
	@$(FF) --sfd --input $< --output $@

distclean:
	@rm -rf amiri-$(VERSION) amiri-$(VERSION).tar.bz2
	@rm -rf $(PACK)

dist: all check pack table
	@echo "   Making dist tarball"
	@mkdir -p amiri-$(VERSION)/$(SRC)
	@mkdir -p amiri-$(VERSION)/$(WEB)
	@mkdir -p amiri-$(VERSION)/$(DOC)
	@mkdir -p amiri-$(VERSION)/$(TOOLS)
	@mkdir -p amiri-$(VERSION)/$(TESTS)
	@cp $(PACK) amiri-$(VERSION)/$(SRC)
	@cp $(FEAT) amiri-$(VERSION)/$(SRC)
	@sed -e "/#->8-/,$$ d" -e "s/sfdir/sfd/" Makefile > amiri-$(VERSION)/Makefile
	@cp $(license) amiri-$(VERSION)
	@cp $(DTTF) amiri-$(VERSION)
	@cp README.txt amiri-$(VERSION)
	@cp $(DOCFILES) amiri-$(VERSION)/$(DOC)
	@cp $(WTTF) amiri-$(VERSION)/$(WEB)
	@cp $(WOFF) amiri-$(VERSION)/$(WEB)
	@cp $(EOTS) amiri-$(VERSION)/$(WEB)
	@cp $(CSSS) amiri-$(VERSION)/$(WEB)
	@cp $(PDFS) amiri-$(VERSION)/$(DOC)
	@cp $(TEST) amiri-$(VERSION)/$(TESTS)
	@cp $(BUILD) amiri-$(VERSION)/$(TOOLS)
	@cp $(RUNTEST) amiri-$(VERSION)/$(TOOLS)
	@tar cfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)
