.PHONY: all clean ttf web pack

VERSION=0.009

SRC=sources
BUILD=./tools/build.py
FF=python $(BUILD)
MKEOT=ttf2eot

SFDS=$(SRC)/amiri-regular.sfdir
TTFS=$(SFDS:.sfdir=.ttf)
WOFF=$(SFDS:.sfdir=.woff)
EOTS=$(SFDS:.sfdir=.eot)
PDFS=$(SFDS:.sfdir=-table.pdf)
CSSS=$(SRC)/amiri.css
FEAT=$(SRC)/gsub.fea

DOC=README README.ar OFL.txt OFL-FAQ.txt NEWS NEWS.ar

all: ttf web

ttf: $(TTFS)
web: $(WOFF) $(EOTS) $(CSSS)
table: $(PDFS)

%.ttf : %.sfdir $(SRC)/gsub.fea
	@echo "   FF\t$@"
	@$(FF) -i $< -o $@ -f $(SRC)/gsub.fea

%.woff : %.sfdir $(SRC)/gsub.fea
	@echo "   FF\t$@"
	@$(FF) --web -i $< -o $@ -f $(SRC)/gsub.fea

%.eot : %.ttf
	@echo "   FF\t$@"
	@$(MKEOT) $< > $@

%.css: $(SFDS)
	@echo "   GEN\t$@"
	@$(FF) --css -i $^ -o $@

%.pdf: $(TTFS)
	@echo "   GEN\t$@"
	@fntsample -f $< -o $@
clean:
	@rm -rfv $(TTFS) $(WOFF) $(EOTS) $(CSSS) $(PACK)
	@rm -rfv amiri-$(VERSION) amiri-$(VERSION).tar.bz2

#->8-
PACK=$(SFDS:.sfdir=.sfd)

pack: $(PACK)

%.sfd: %.sfdir
	@echo "   GEN\t$@"
	@$(FF) --sfd -i $< -o $@

dist: all pack table
	@echo "   Making dist tarball"
	@mkdir -p amiri-$(VERSION)/$(SRC)
	@mkdir -p amiri-$(VERSION)/web
	@mkdir -p amiri-$(VERSION)/tools
	@mkdir -p amiri-$(VERSION)/documentation
	@cp -r $(PACK) amiri-$(VERSION)/$(SRC)
	@cp $(FEAT) amiri-$(VERSION)/$(SRC)
	@sed -e "/#->8-/,$$ d" -e "s/sfdir/sfd/" Makefile > amiri-$(VERSION)/Makefile
	@cp $(DOC) amiri-$(VERSION)
	@cp $(BUILD) amiri-$(VERSION)/tools
	@cp $(TTFS) amiri-$(VERSION)
	@cp $(WOFF) amiri-$(VERSION)/web
	@cp $(EOTS) amiri-$(VERSION)/web
	@cp $(CSSS) amiri-$(VERSION)/web
	@cp $(PDFS) amiri-$(VERSION)/documentation
	@tar cfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)
