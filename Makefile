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
VERSION = 0.5.1


# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_SDIST = dist/$(PACKAGENAME)-$(VERSION).tar.gz
SOURCES_CODE = \
	simplicial/__init__.py \
	simplicial/simplicialcomplex.py \
	simplicial/triangularlattice.py \
	simplicial/embedding.py \
	simplicial/drawing/__init__.py \
	simplicial/drawing/drawing.py \
	simplicial/file/__init__.py \
	simplicial/file/json_simplicial.py

# Test suite
SOURCES_TESTS = \
	test/__init__.py \
	test/test_simplicialcomplex.py \
	test/test_homology.py \
	test/test_flag.py \
	test/test_join.py \
	test/test_vr.py \
	test/test_triangularlattice.py \
	test/test_randomplanes.py \
	test/test_json_simplicial.py
TESTSUITE = test

# Sources for Sphinx documentation
SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = $(PACKAGENAME)-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst \
	doc/reference.rst \
	doc/start.rst \
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
	tox \
	nose \
	coverage \
	sphinx \
	twine
PY_NON_REQUIREMENTS = \
	appnope \
	subprocess32 \
	functools32 \
	futures
VENV = venv3
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt


# ----- Tools -----

# Base commands
PYTHON = python3
JUPYTER = jupyter
PIP = pip
TOX = tox
COVERAGE = coverage
TWINE = twine
GPG = gpg
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
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
RUN_TESTS = $(TOX)
RUN_COVERAGE = $(COVERAGE) erase && $(COVERAGE) run -a setup.py test && $(COVERAGE) report -m --include '$(PACKAGENAME)*'
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = PYTHONPATH=$(ROOT) make html
RUN_TWINE = $(TWINE) upload dist/$(PACKAGENAME)-$(VERSION).tar.gz dist/$(PACKAGENAME)-$(VERSION).tar.gz.asc
NON_REQUIREMENTS = $(SED) $(patsubst %, -e '/^%*/d', $(PY_NON_REQUIREMENTS))


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run tests for all versions of Python we're interested in
test: env setup.py
	$(ACTIVATE) && $(RUN_TESTS)

# Run coverage checks over the test suite
coverage: env
	$(ACTIVATE) && $(RUN_COVERAGE)

# Build the API documentation using Sphinx
.PHONY: doc
doc: $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	$(ACTIVATE) && $(CHDIR) doc && $(RUN_SPHINX_HTML)

# Build a development venv from the known-good requirements in the repo
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(DEV_REQUIREMENTS) $(VENV)/requirements.txt
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Build a development venv from the latest versions of the required packages,
# creating a new requirements.txt ready for committing to the repo. Make sure
# things actually work in this venv before committing!
.PHONY: newenv
newenv:
	$(RM) $(VENV)
	$(VIRTUALENV) $(VENV)
	echo $(PY_REQUIREMENTS) | $(TR) ' ' '\n' >$(VENV)/$(REQUIREMENTS)
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt
	$(NON_REQUIREMENTS) $(VENV)/requirements.txt >$(REQUIREMENTS)
	echo $(PY_DEV_REQUIREMENTS) | $(TR) ' ' '\n' >$(VENV)/$(REQUIREMENTS)
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt
	$(NON_REQUIREMENTS) $(VENV)/requirements.txt >$(DEV_REQUIREMENTS)

# Build a source distribution
sdist: $(SOURCES_SDIST)

# Upload a source distribution to PyPi
upload: $(SOURCES_SDIST)
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	$(ACTIVATE) && $(RUN_TWINE)

# Clean up the distribution build
clean:
	$(RM) $(SOURCES_GENERATED) epyc.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP)

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQUIREMENTS/$(PY_REQUIREMENTS:%="%",)/g' >$@

# The source distribution tarball
$(SOURCES_SDIST): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) sdist


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite
   make env          create a known-good development virtual environment
   make newenv       update the development venv's requirements
   make sdist        create a source distribution
   make upload       upload distribution to PyPi
   make clean        clean-up the build
   make reallyclean  clean up build and development venv

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
