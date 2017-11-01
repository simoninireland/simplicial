# Makefile for simplicial
#
# Copyright (C) 2017 Simon Dobson
# 
# This file is part of simplicial, simplicial topology in Python.
#
# Simplicial is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simplicial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Simplicial. If not, see <http://www.gnu.org/licenses/gpl.html>.

# The name of our package on PyPi
PACKAGENAME = simplicial

# The version we're building
VERSION = 0.4.1


# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_CODE = \
	simplicial/__init__.py \
	simplicial/simplicialcomplex.py \
	simplicial/triangularlattice.py \
	simplicial/drawing/__init__.py \
	simplicial/drawing/drawing.py \
	simplicial/drawing/layout.py \
	simplicial/file/__init__.py \
	simplicial/file/json_simplicial.py

# Test suite
SOURCES_TESTS = \
	test/__init__.py \
	test/__main__.py \
	test/simplicialcomplex.py \
	test/triangularlattice.py \
	test/randomplanes.py \
	test/json_simplicial.py
TESTSUITE = test

# Sources for Sphinx documentation
SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = $(PACKAGENAME)-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst \
	doc/simplicialcomplex.rst \
	doc/embedding.rst \
	doc/triangularlattice.rst \
	doc/drawing.rst \
	doc/file.rst \
	doc/installation.rst \
	doc/glossary.rst \
	doc/acknowledgements.rst \
	doc/bibliography.rst

# Extras for the build and packaging system
SOURCES_EXTRA = \
	README.rst \
	LICENSE \
	HISTORY
SOURCES_GENERATED = \
	MANIFEST \
	setup.py

# Requirements for running the library, for the development venv needed to
# build it, and and OS-specific non-requirements that need to be removed
# for portability
PY_REQUIREMENTS = \
	numpy \
	matplotlib
PY_DEV_REQUIREMENTS = \
	$(PY_REQUIREMENTS) \
	sphinx \
	twine
PY_NON_REQUIREMENTS = \
	appnope \
	subprocess32 \
	functools32
VENV = venv
REQUIREMENTS = requirements.txt


# ----- Tools -----

# Base commands
PYTHON = python
JUPYTER = jupyter
PIP = pip
TWINE = twine
GPG = gpg
VIRTUALENV = virtualenv
ACTIVATE = . bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r

# Root directory
ROOT = $(shell pwd)

# Constructed commands
RUN_TESTS = $(PYTHON) -m $(TESTSUITE)
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = make html
RUN_TWINE = $(TWINE) upload dist/$(PACKAGENAME)-$(VERSION).tar.gz dist/$(PACKAGENAME)-$(VERSION).tar.gz.asc
NON_REQUIREMENTS = $(SED) $(patsubst %, -e '/^%*/d', $(PY_NON_REQUIREMENTS))


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# RUn the test suite
.PHONY: test
test: env
	$(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) $(ROOT) && $(RUN_TESTS)

# Build the API documentation using Sphinx
.PHONY: doc
doc: env $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	$(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) $(ROOT)/doc && PYTHONPATH=$(ROOT) $(RUN_SPHINX_HTML)
	$(CHDIR) $(SOURCES_DOC_BUILD_HTML_DIR) && $(ZIP) $(SOURCES_DOC_ZIP) *
	$(CP) $(SOURCES_DOC_BUILD_HTML_DIR)/$(SOURCES_DOC_ZIP) .

# Build a development venv from the known-good requirements in the repo
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(REQUIREMENTS) $(VENV)/requirements.txt
	$(CHDIR) $(VENV) && $(ACTIVATE) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt

# Build a development venv from the latest versions of the required packages,
# creating a new requirements.txt ready for committing to the repo. Make sure
# things actually work in this venv before committing!
.PHONY: newenv
newenv:
	echo $(PY_DEV_REQUIREMENTS) | $(TR) ' ' '\n' >$(REQUIREMENTS)
	make env
	$(NON_REQUIREMENTS) $(VENV)/requirements.txt >$(REQUIREMENTS)

# Build a source distribution
dist: $(SOURCES_GENERATED)
	$(RUN_SETUP) sdist

# Upload a source distribution to PyPi
upload: $(SOURCES_GENERATED)
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	($(CHDIR) $(VENV) && $(ACTIVATE) && $(CHDIR) $(ROOT) && $(RUN_TWINE))

# Clean up the distribution build 
clean:
	$(RM) $(SOURCES_GENERATED) simplicial.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP)

# Clean up the development venv as well
reallyclean: clean
	$(RM) $(VENV)


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQUIREMENTS/$(PY_REQUIREMENTS:%="%",)/g' >$@


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite
   make env          create a known-good development virtual environment
   make newenv       update the development venv's requirements
   make dist         create a source distribution
   make upload       upload distribution to PyPi
   make clean        clean-up the build
   make reallyclean  clean up build and development venv

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
