# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
PYTHONEXE     = python
SPHINXOPTS    =
SPHINXBUILD   = $(PYTHONEXE) -msphinx
SPHINXPROJ    = fluxdoc
SOURCEDIR     = .
BUILDDIR      = _build
NO_GET_CONST  = false

# Put it first so that "make" without argument is like "make help".
.PHONY: help
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


# just remove directories in BUILDDIR
clean:
	rm -rf $(BUILDDIR)/*/


# download and add constitutions:
.PHONY: get-constitutions
ifneq "$(NO_GET_CONST)" "true"
get-constitutions:
	python3 ./scripts/download_constitutions.py
else
get-constitutions: ;
endif


.PHONY: build-html
build-html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: dev
dev:
	$(MAKE) build-html


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
.DEFAULT:
	$(info Using exe: $(SPHINXBUILD))
	$(info Getting constitutions (use `NO_GET_CONST=true` to avoid))
	$(MAKE) get-constitutions
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
