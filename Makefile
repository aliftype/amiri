.PHONY: all clean ttf web pack

VERSION=0.003

SRC=sources
BUILD=./tools/build.py
FF=python $(BUILD)
MKEOT=ttf2eot

SFDS=$(SRC)/amiri-regular.sfdir
TTFS=$(SFDS:.sfdir=.ttf)
WOFF=$(SFDS:.sfdir=.woff)
EOTS=$(SFDS:.sfdir=.eot)
PACK=$(SFDS:.sfdir=.sfd)
CSSS=$(SRC)/amiri.css

DOC=README README.ar OFL.txt OFL-FAQ.txt NEWS NEWS.ar

all: ttf web

ttf: $(TTFS)
web: $(WOFF) $(EOTS) $(CSSS)
pack: $(PACK)

%.ttf : %.sfdir
	@echo "generating ‛$@’"
	@$(FF) $< $@

%.woff : %.sfdir
	@echo "generating ‛$@’"
	@$(FF) $< $@

%.eot : %.ttf
	@echo "generating ‛$@’"
	@$(MKEOT) $< > $@

%.css: $(SFDS)
	@echo "generating ‛$@’"
	@$(FF) $^ $@

%.sfd : %.sfdir
	@echo "packing ‛$<’ into ‛$@’"
	@$(FF) $< $@

clean:
	@rm -rfv $(TTFS) $(WOFF) $(EOTS) $(CSSS) $(PACK)
	@rm -rfv amiri-$(VERSION) amiri-$(VERSION).tar.bz2

dist: all pack
	@echo "Making dist tarball"
	@mkdir -p amiri-$(VERSION)/$(SRC)
	@mkdir -p amiri-$(VERSION)/web
	@mkdir -p amiri-$(VERSION)/tools
	@cp -r $(PACK) amiri-$(VERSION)/$(SRC)
	@cp Makefile amiri-$(VERSION)
	@cp $(DOC) amiri-$(VERSION)
	@cp $(BUILD) amiri-$(VERSION)/tools
	@cp $(TTFS) amiri-$(VERSION)
	@cp $(WOFF) amiri-$(VERSION)/web
	@cp $(EOTS) amiri-$(VERSION)/web
	@cp $(CSSS) amiri-$(VERSION)/web
	@tar cfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)
