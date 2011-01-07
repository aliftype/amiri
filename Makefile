.PHONY: clean

VERSION=0.003

src=sources
build=./tools/build.py

dist_doc=README README.ar OFL.txt OFL-FAQ.txt NEWS NEWS.ar

all:
	@$(MAKE) -C $(src)

dist: all
	@echo "Making dist tarball"
	@$(MAKE) pack -C $(src)
	@mkdir -p amiri-$(VERSION)/$(src)
	@mkdir -p amiri-$(VERSION)/web
	@mkdir -p amiri-$(VERSION)/tools
	@cp -r $(src)/*.sfd amiri-$(VERSION)/$(src)
	@cp Makefile amiri-$(VERSION)
	@cp $(src)/Makefile amiri-$(VERSION)/$(src)
	@cp $(dist_doc) amiri-$(VERSION)
	@cp $(build) amiri-$(VERSION)/tools
	@cp $(src)/*.ttf amiri-$(VERSION)
	@cp $(src)/*.woff amiri-$(VERSION)/web
	@cp $(src)/*.eot amiri-$(VERSION)/web
	@cp $(src)/*.css amiri-$(VERSION)/web
	@tar cfj amiri-$(VERSION).tar.bz2 amiri-$(VERSION)

clean:
	@$(MAKE) -C $(src) clean
	@rm -rf *.tar.bz2 amiri-$(VERSION)
