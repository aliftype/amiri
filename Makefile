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
PACK=$(SFDS:.sfdir=.sfd)
PDFS=$(SFDS:.sfdir=-table.pdf)
CSSS=$(SRC)/amiri.css

DOC=README README.ar OFL.txt OFL-FAQ.txt NEWS NEWS.ar

all: ttf web

ttf: $(TTFS)
web: $(WOFF) $(EOTS) $(CSSS)
pack: $(PACK)
table: $(PDFS)

%.ttf : %.sfdir
	@echo "   FF\t$@"
	@$(FF) $< $@

%.woff : %.sfdir
	@echo "   FF\t$@"
	@$(FF) $< $@

%.eot : %.ttf
	@echo "   FF\t$@"
	@$(MKEOT) $< > $@

%.css: $(SFDS)
	@echo "   GEN\t$@"
	@$(FF) $^ $@

%.sfd: %.sfdir
	@echo "   GEN\t$@"
	@$(FF) $< $@

%.pdf: $(TTFS)
	@echo "   GEN\t$@"
	@fntsample -f $< -o $@
clean:
	@rm -rfv $(TTFS) $(WOFF) $(EOTS) $(CSSS) $(PACK)
	@rm -rfv amiri-$(VERSION) amiri-$(VERSION).tar.bz2

dist: all pack table
	@echo "   Making dist tarball"
	@mkdir -p amiri-$(VERSION)/$(SRC)
	@mkdir -p amiri-$(VERSION)/web
	@mkdir -p amiri-$(VERSION)/tools
	@mkdir -p amiri-$(VERSION)/documentation
	@cp -r $(PACK) amiri-$(VERSION)/$(SRC)
	@cp Makefile amiri-$(VERSION)
	@cp $(DOC) amiri-$(VERSION)
	@cp $(BUILD) amiri-$(VERSION)/tools
	@cp $(TTFS) amiri-$(VERSION)
	@cp $(WOFF) amiri-$(VERSION)/web
	@cp $(EOTS) amiri-$(VERSION)/web
	@cp $(CSSS) amiri-$(VERSION)/web
	@cp $(PDFS) amiri-$(VERSION)/documentation
	@tar cfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)
