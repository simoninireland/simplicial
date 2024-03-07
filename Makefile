# Makefile for simplicial
#
# Copyright (C) 2017--2024 Simon Dobson
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
VERSION = 1.1.1


# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_SDIST = dist/$(PACKAGENAME)-$(VERSION).tar.gz
SOURCES_WHEEL = dist/$(PACKAGENAME)-$(VERSION)-py2-py3-none-any.whl
SOURCES_CODE_INIT = \
	simplicial/__init__.py \
	simplicial/drawing/__init__.py \
	simplicial/file/__init__.py
SOURCES_CODE = \
	simplicial/utils.py \
	simplicial/rep.py \
	simplicial/referencerep.py \
	simplicial/graphrep.py \
	simplicial/simplicialcomplex.py \
	simplicial/function.py \
	simplicial/sheaf.py \
	simplicial/dvf.py \
	simplicial/subcomplex.py \
	simplicial/generators.py \
	simplicial/filtration.py \
	simplicial/eulerintegrator.py \
	simplicial/triangularlattice.py \
	simplicial/embedding.py \
	simplicial/drawing/drawing.py \
	simplicial/drawing/draw_euler.py \
	simplicial/file/json_simplicial.py

# Test suite
SOURCES_TESTS_INIT = test/__init__.py
SOURCES_TESTS = \
	test/test_simplicialcomplex.py \
	test/test_filtration.py \
	test/test_eulerintegrator.py \
	test/test_homology.py \
	test/test_cohomology.py \
	test/test_morse.py \
	test/test_flag.py \
	test/test_compose.py \
	test/test_function.py \
	test/test_sheaf.py \
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
	doc/rep.rst \
	doc/referencerep.rst \
	doc/graphrep.rst \
	doc/simplicialcomplex.rst \
	doc/filtration.rst \
	doc/eulerintegrator.rst \
	doc/generators.rst \
	doc/embedding.rst \
	doc/triangularlattice.rst \
	doc/function.rst \
	doc/sfrep.rst \
	doc/sheaf.rst \
	doc/drawing.rst \
	doc/file.rst \
	doc/installation.rst \
	doc/glossary.rst \
	doc/contributing.rst \
	doc/acknowledgements.rst \
	doc/zbibliography.rst \
	doc/tutorial.rst \
	doc/tutorial/build-complex.rst \
	doc/tutorial/navigating-complex.rst \
	doc/tutorial/simplex-attributes.rst \
	doc/tutorial/constructing.rst \
	doc/tutorial/analysis.rst \
	doc/tutorial/filtrations.rst \
	doc/implementation.rst \
	doc/implementation/simplicialcomplex.rst \
	doc/implementation/homology.rst
SOURCES_PAPER = \
	paper.md \
	paper.bib \

# Extras for the build and packaging system
SOURCES_EXTRA = \
	README.rst \
	branches.org \
	CITATION.cff \
	LICENSE \
	HISTORY
SOURCES_GENERATED = \
	MANIFEST \
	setup.py


# ----- Tools -----

# Base commands
PYTHON = python3
JUPYTER = jupyter
PIP = pip
TOX = tox
COVERAGE = coverage
TWINE = twine
GPG = gpg
GIT = git
FLAKE8 = flake8
MYPY = mypy
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
TR = tr
CAT = cat
SED = sed
ETAGS = etags
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r
PASTE = paste

# Files that are locally changed vs the remote repo
# (See https://unix.stackexchange.com/questions/155046/determine-if-git-working-directory-is-clean-from-a-script)
GIT_DIRTY = $(shell $(GIT) status --untracked-files=no --porcelain)

# The git branch we're currently working on
GIT_BRANCH = $(shell $(GIT) rev-parse --abbrev-ref HEAD 2>/dev/null)

# Root directory
ROOT = $(shell pwd)

# Requirements for running the library and for the development venv needed to build it
VENV = venv3
REQUIREMENTS = requirements.txt
DEV_REQUIREMENTS = dev-requirements.txt

# Requirements for setup.py
# Note we elide dependencies to do with backporting the type-checking
PY_REQUIREMENTS = $(shell $(SED) -e '/^typing_extensions/d' -e 's/^\(.*\)/"\1",/g' $(REQUIREMENTS) | $(TR) '\n' ' ')

# Constructed commands
RUN_TESTS = $(TOX)
RUN_COVERAGE = $(COVERAGE) erase && $(COVERAGE) run -a setup.py test && $(COVERAGE) report -m --include '$(PACKAGENAME)*'
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = PYTHONPATH=$(ROOT) make html
RUN_TWINE = $(TWINE) upload dist/$(PACKAGENAME)-$(VERSION).tar.gz dist/$(PACKAGENAME)-$(VERSION).tar.gz.asc


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Build the tags file
tags:
	$(ETAGS) -o TAGS $(SOURCES_CODE) $(SOURCES_TESTS)

# Run tests for all versions of Python we're interested in
test: env Makefile setup.py
	$(ACTIVATE) && $(RUN_TESTS)

# Run coverage checks over the test suite
coverage: env
	$(ACTIVATE) && $(RUN_COVERAGE)

# Run lint checks
lint: env
	$(ACTIVATE) && $(FLAKE8) $(SOURCES_CODE) --count --statistics --ignore=E501,E303,E301,E302,E261,E741,E265,E402,E731,E129,W504

# Build the API documentation using Sphinx
.PHONY: doc
doc: env $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	$(ACTIVATE) && $(CHDIR) doc && $(RUN_SPHINX_HTML)

# Build a development venv from the requirements in the repo
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CAT) $(REQUIREMENTS) $(DEV_REQUIREMENTS) >$(VENV)/requirements.txt
	$(ACTIVATE) && $(PIP) install -U pip wheel && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt
	$(ACTIVATE) && $(MYPY) --install-types --non-interactive

# Make a new release
release: $(SOURCES_GENERATED) master-only lint commit sdist wheel upload

# Build a source distribution
sdist: $(SOURCES_SDIST)

# Build a wheel distribution
wheel: $(SOURCES_WHEEL)

# Upload a source distribution to PyPi
upload: commit sdist wheel
	$(GPG) --detach-sign -a dist/$(PACKAGENAME)-$(VERSION).tar.gz
	$(ACTIVATE) && $(RUN_TWINE)

# Check we're on the master branch before uploading
master-only:
	if [ "$(GIT_BRANCH)" != "master" ]; then echo "Can only release from master branch"; exit 1; fi

# Update the remote repos on release
commit: check-local-repo-clean
	$(GIT) push origin master
	$(GIT) tag -a v$(VERSION) -m "Version $(VERSION)"
	$(GIT) push origin v$(VERSION)

.SILENT: check-local-repo-clean
check-local-repo-clean:
	if [ "$(GIT_DIRTY)" ]; then echo "Uncommitted files: $(GIT_DIRTY)"; exit 1; fi

# Clean up the distribution build
clean:
	$(RM) $(SOURCES_GENERATED) simplicial.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP) dist build

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQUIREMENTS/$(PY_REQUIREMENTS)/g' >$@

# The source distribution tarball
$(SOURCES_SDIST): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) sdist

# The binary (wheel) distribution
$(SOURCES_WHEEL): $(SOURCES_GENERATED) $(SOURCES_CODE) Makefile
	$(ACTIVATE) && $(RUN_SETUP) bdist_wheel

# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite
   make env          create a known-good development virtual environment
   make tags         build the TAGS file
   make coverage     run coverage checks of the test suite
   make lint         run lint style checks
   make doc          build the API documentation using Sphinx
   make release      make a release and upload to PyPi
   make clean        clean-up the build
   make reallyclean  clean up build and development venv

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
