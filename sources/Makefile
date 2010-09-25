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
	$(FF) $< $@

%.woff : %.sfdir
	$(FF) $< $@

%.eot : %.ttf
	$(MKEOT) $< > $@

amiri.css: amiri-regular.sfdir
	$(FF) $< $@


clean:
	rm -rf $(TTFS) $(WOFF) $(EOTS) $(CSSS)
