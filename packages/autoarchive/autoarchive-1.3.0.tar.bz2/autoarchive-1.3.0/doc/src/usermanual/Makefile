# Makefile

# Project: AutoArchive
# License: GNU GPLv3

# Copyright (C) 2003 - 2012 Róbert Čerňanský



# .. Makefile for User documentation.



# You can set these variables from the command line.
SPHINXOPTS    = -E
SPHINXBUILD   = sphinx-build
BUILDDIR      = ../../user

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .
README_DIR    = ../../..

.PHONY: help all clean html text man

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  man        to make manual pages"
	@echo "  text       to make text files"
	@echo "  all        to make html, text and man at once"
	@echo "  clean      to clean the build directory"

all:	html man text

clean:
	-rm -rf $(BUILDDIR)/html $(BUILDDIR)/man $(BUILDDIR)/text $(BUILDDIR)/doctrees

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	-rm -rf $(BUILDDIR)/html/{man,text,.buildinfo,_sources} $(BUILDDIR)/doctrees
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	-rm -rf $(BUILDDIR)/doctrees
	-ln -s aa.1 $(BUILDDIR)/man/autoarchive.1
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	-rm -rf $(BUILDDIR)/doctrees
	-mv $(BUILDDIR)/text/text/readme.txt $(README_DIR)/README
	-rm -rf $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."
