.PHONY: all clean ttf web
#.SUFFIXES: $(SUFFIXES) .sfdir .ttf .otf

FF=python ../tools/build.py
MKEOT=ttf2eot

SFDS=amiri-regular.sfdir
TTFS=$(SFDS:.sfdir=.ttf)
WOFF=$(SFDS:.sfdir=.woff)
EOTS=$(SFDS:.sfdir=.eot)
CSSS=amiri.css

all: ttf web

ttf: $(TTFS)
web: $(WOFF) $(EOTS) amiri.css

%.ttf : %.sfdir
	@echo "Generating $@"
	@$(FF) $< $@

%.woff : %.sfdir
	@echo "Generating $@"
	@$(FF) $< $@

%.eot : %.ttf
	@echo "Generating $@"
	@$(MKEOT) $< > $@

amiri.css: $(SFDS)
	@echo "Generating $@"
	@$(FF) $^ $@


clean:
	@rm -rf $(TTFS) $(WOFF) $(EOTS) $(CSSS)
