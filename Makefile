SRC=./sources
TOOLS=./tools
WEB=./web

BUILD=python $(TOOLS)/build.py
MKEOT=ttf2eot

all: ttf web
web: woff eot

regular-ttf: $(SRC)/amiri-regular.sfdir
	$(BUILD) $(SRC)/amiri-regular.sfdir amiri-regular.ttf

regular-woff: $(SRC)/amiri-regular.sfdir
	$(BUILD) $(SRC)/amiri-regular.sfdir $(WEB)/amiri-regular.woff

regular-eot: regular-ttf
	$(MKEOT) amiri-regular.ttf > $(WEB)/amiri-regular.eot

ttf: regular-ttf
woff: regular-woff
eot: regular-eot

clean:
	rm -rf *.ttf $(WEB)/*.woff $(WEB)/*.eot
