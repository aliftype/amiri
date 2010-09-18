VERSION=0.001

SRC=./sources
TOOLS=./tools
WEB=./web

BUILD=python $(TOOLS)/build.py
MKEOT=ttf2eot

all: ttf web
web: woff eot css

regular-ttf: $(SRC)/amiri-regular.sfdir
	$(BUILD) $(SRC)/amiri-regular.sfdir amiri-regular.ttf

regular-woff: $(SRC)/amiri-regular.sfdir
	$(BUILD) $(SRC)/amiri-regular.sfdir $(WEB)/amiri-regular.woff

regular-eot: regular-ttf
	$(MKEOT) amiri-regular.ttf > $(WEB)/amiri-regular.eot

regular-css: $(SRC)/amiri-regular.sfdir
	$(BUILD) $(SRC)/amiri-regular.sfdir $(WEB)/amiri.css

ttf: regular-ttf
woff: regular-woff
eot: regular-eot
css: regular-css

dist: all
	mkdir -p amiri-$(VERSION)/sources
	mkdir -p amiri-$(VERSION)/web
	mkdir -p amiri-$(VERSION)/tools
	cp amiri-regular.ttf amiri-$(VERSION)
	cp README README.ar OFL.txt OFL-FAQ.txt Makefile amiri-$(VERSION)
	cp -r sources/amiri-regular.sfdir amiri-$(VERSION)/sources
	cp web/amiri-regular.woff amiri-$(VERSION)/web
	cp web/amiri-regular.eot amiri-$(VERSION)/web
	cp web/amiri.css amiri-$(VERSION)/web
	cp tools/build.py amiri-$(VERSION)/tools
	tar cvfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)


clean:
	rm -rf *.ttf $(WEB)/*.woff $(WEB)/*.eot *.tar.bz2 amiri-$(VERSION)
