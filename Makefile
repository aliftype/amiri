.PHONY: all clean ttf web pack check

NAME=Amiri
LATIN=AmiriLatin
VERSION=0.114

SRC=sources
BUILDDIR=build
DOC=documentation
FONTS=$(NAME)-Regular $(NAME)-Bold $(NAME)-Slanted $(NAME)-BoldSlanted $(NAME)Quran $(NAME)QuranColored
DIST=$(NAME)-$(VERSION)
LICENSE=OFL.txt

BUILD=build.py
MAKEQURAN=mkquran.py
PY ?= python
FF=$(PY) $(BUILD)

TTF=$(FONTS:%=%.ttf)
OTF=$(FONTS:%=%.otf)
HTML=$(DOC)/Documentation-Arabic.html
FEA=$(wildcard $(SRC)/*.fea)

export SOURCE_DATE_EPOCH ?= 0

all: ttf

ttf: $(TTF)
otf: $(OTF)
doc: $(HTML)

$(BUILDDIR)/%.ufo: $(SRC)/%.sfd
	@echo "   UFO	$@"
	@mkdir -p $(BUILDDIR)
	@sfd2ufo --minimal $< $@

$(NAME)QuranColored.ttf $(NAME)QuranColored.otf: $(BUILDDIR)/$(NAME)-Regular.ufo $(BUILDDIR)/$(LATIN)-Regular.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE) --quran

$(NAME)Quran.ttf: $(NAME)QuranColored.ttf $(MAKEQURAN)
	@echo "   FF	$@"
	@$(PY) $(MAKEQURAN) $< $@

$(NAME)Quran.otf: $(NAME)QuranColored.otf $(MAKEQURAN)
	@echo "   FF	$@"
	@$(PY) $(MAKEQURAN) $< $@

$(NAME)-Regular.ttf $(NAME)-Regular.otf: $(BUILDDIR)/$(NAME)-Regular.ufo $(BUILDDIR)/$(LATIN)-Regular.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE)

$(NAME)-Slanted.ttf $(NAME)-Slanted.otf: $(BUILDDIR)/$(NAME)-Regular.ufo $(BUILDDIR)/$(LATIN)-Slanted.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE) --slant=10

$(NAME)-Bold.ttf $(NAME)-Bold.otf: $(BUILDDIR)/$(NAME)-Bold.ufo $(BUILDDIR)/$(LATIN)-Bold.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE)

$(NAME)-BoldSlanted.ttf $(NAME)-BoldSlanted.otf: $(BUILDDIR)/$(NAME)-Bold.ufo $(BUILDDIR)/$(LATIN)-BoldSlanted.ufo $(SRC)/$(NAME).fea $(FEA) $(LICENSE) $(BUILD)
	@echo "   FF	$@"
	@$(FF) --input $< --output $@ --features=$(SRC)/$(NAME).fea --version $(VERSION) --license $(LICENSE) --slant=10

$(DOC)/Documentation-Arabic.html: $(DOC)/Documentation-Arabic.md
	@echo "   GEN	$@"
	@pandoc $< -o $@ -f markdown-smart -t html -s -c Documentation-Arabic.css

check: $(TTF) $(OTF)
	@echo "running tests"
	@$(foreach font,$+,echo "   OTS	$(font)" && python -m ots --quiet $(font) &&) true

clean:
	rm -rfv $(TTF) $(OTF) $(HTML)

distclean: clean
	rm -rf $(DIST){,.zip}

dist: otf check pack doc
	@rm -rf $(DIST)
	@mkdir -p $(DIST)/otf
	@cp $(LICENSE) $(DIST)
	@cp $(TTF) $(DIST)
	@cp $(OTF) $(DIST)/otf
	@cp README.md $(DIST)/README
	@cp README-Arabic.md $(DIST)/README-Arabic
	@cp NEWS.md $(DIST)/NEWS
	@cp NEWS-Arabic.md $(DIST)/NEWS-Arabic
	@cp $(HTML) $(DIST)
	@echo "   ZIP  $(DIST)"
	@zip -rq $(DIST).zip $(DIST)
