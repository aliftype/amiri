.PHONY: all clean ttf web
#.SUFFIXES: $(SUFFIXES) .sfdir .ttf .otf

FF=python ../tools/build.py
MKEOT=ttf2eot

SFDS=amiri-regular.sfdir
TTFS=$(SFDS:.sfdir=.ttf)
WOFF=$(SFDS:.sfdir=.woff)
EOTS=$(SFDS:.sfdir=.eot)
PACK=$(SFDS:.sfdir=.sfd)
CSSS=amiri.css

all: ttf web

ttf: $(TTFS)
web: $(WOFF) $(EOTS) amiri.css
pack: $(PACK)

%.ttf : %.sfdir
	@echo "Generating $@"
	@$(FF) $< $@

%.woff : %.sfdir
	@echo "Generating $@"
	@$(FF) $< $@

%.eot : %.ttf
	@echo "Generating $@"
	@$(MKEOT) $< > $@

%.sfd : %.sfdir
	@echo "Packing $< into SFD file $@"
	@$(FF) $< $@

amiri.css: $(SFDS)
	@echo "Generating $@"
	@$(FF) $^ $@


clean:
	@rm -rf $(TTFS) $(WOFF) $(EOTS) $(CSSS) $(PACK)
