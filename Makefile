.PHONY: all clean ttf web pack

VERSION=0.010

TOOLS=tools
SRC=sources
WEB=web
DOC=documentation
FONTS=amiri-regular

BUILD=$(TOOLS)/build.py
FF=python $(BUILD)
MKEOT=ttf2eot

SFDS=$(FONTS:%=$(SRC)/%.sfdir)
DTTF=$(FONTS:%=%.ttf)
WTTF=$(FONTS:%=$(WEB)/%.ttf)
WOFF=$(FONTS:%=$(WEB)/%.woff)
EOTS=$(FONTS:%=$(WEB)/%.eot)
PDFS=$(FONTS:%=$(DOC)/%-table.pdf)
CSSS=$(WEB)/amiri.css
FEAT=$(SRC)/gsub.fea $(SRC)/calt.fea

docfiles=README README.ar OFL.txt OFL-FAQ.txt NEWS NEWS.ar

all: ttf web

ttf: $(DTTF)
web: $(WTTF) $(WOFF) $(EOTS) $(CSSS)
table: $(PDFS)

%.ttf: $(SRC)/%.sfdir $(FEAT)
	@echo "   FF\t$@"
	@$(FF) -i $< -o $@ -f "$(FEAT)" -v $(VERSION)

$(WEB)/%.ttf: $(SRC)/%.sfdir $(FEAT)
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(FF) --web -i $< -o $@ -f "$(FEAT)" -v $(VERSION)

$(WEB)/%.woff: $(SRC)/%.sfdir $(FEAT)
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(FF) --web -i $< -o $@ -f "$(FEAT)" -v $(VERSION)

$(WEB)/%.eot: $(WEB)/%.ttf
	@echo "   FF\t$@"
	@mkdir -p $(WEB)
	@$(MKEOT) $< > $@

$(WEB)/%.css: $(SFDS)
	@echo "   GEN\t$@"
	@mkdir -p $(WEB)
	@$(FF) --css -i $^ -o $@ -v $(VERSION)

$(DOC)/%-table.pdf: %.ttf
	@echo "   GEN\t$@"
	@mkdir -p $(DOC)
	@fntsample -f $< -o $@

clean:
	@rm -rf $(DTTF) $(WOFF) $(EOTS) $(CSSS) $(PACK)
	@rm -rf amiri-$(VERSION) amiri-$(VERSION).tar.bz2

#->8-
PACK=$(SFDS:.sfdir=.sfd)

pack: $(PACK)

%.sfd: %.sfdir
	@echo "   GEN\t$@"
	@$(FF) --sfd -i $< -o $@

dist: all pack table
	@echo "   Making dist tarball"
	@mkdir -p amiri-$(VERSION)/$(SRC)
	@mkdir -p amiri-$(VERSION)/$(WEB)
	@mkdir -p amiri-$(VERSION)/$(DOC)
	@mkdir -p amiri-$(VERSION)/$(TOOLS)
	@cp $(PACK) amiri-$(VERSION)/$(SRC)
	@cp $(FEAT) amiri-$(VERSION)/$(SRC)
	@sed -e "/#->8-/,$$ d" -e "s/sfdir/sfd/" Makefile > amiri-$(VERSION)/Makefile
	@cp $(docfiles) amiri-$(VERSION)
	@cp $(DTTF) amiri-$(VERSION)
	@cp $(WTTF) amiri-$(VERSION)/$(WEB)
	@cp $(WOFF) amiri-$(VERSION)/$(WEB)
	@cp $(EOTS) amiri-$(VERSION)/$(WEB)
	@cp $(CSSS) amiri-$(VERSION)/$(WEB)
	@cp $(PDFS) amiri-$(VERSION)/$(DOC)
	@cp $(BUILD) amiri-$(VERSION)/$(TOOLS)
	@tar cfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)
