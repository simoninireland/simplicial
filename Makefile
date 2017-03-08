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

# The version we're building
VERSION = 0.1

# ----- Sources -----

# Source code
SOURCES_SETUP_IN = setup.py.in
SOURCES_CODE = \
	simplicial/__init__.py \
	simplicial/simplicialcomplex.py \
	simplicial/triangularlattice.py
SOURCES_TESTS = \
	test/__init__.py \
	test/__main__.py \
	test/simplicialcomplex.py \
	test/randomplaces.py
TESTSUITE = test

SOURCES_DOC_CONF = doc/conf.py
SOURCES_DOC_BUILD_DIR = doc/_build
SOURCES_DOC_BUILD_HTML_DIR = $(SOURCES_DOC_BUILD_DIR)/html
SOURCES_DOC_ZIP = simplicial-doc-$(VERSION).zip
SOURCES_DOCUMENTATION = \
	doc/index.rst

SOURCES_EXTRA = \
	README.md \
	LICENSE \
	HISTORY
SOURCES_GENERATED = \
	MANIFEST \
	setup.py \
	$(SOURCES_DOC_CONF)


# ----- Tools -----

# Base commands
PYTHON = python
IPYTHON = ipython
JUPYTER = jupyter
PIP = pip
VIRTUALENV = virtualenv
ACTIVATE = . bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r

# Constructed commands
RUN_TESTS = $(IPYTHON) -m $(TESTSUITE)
RUN_SETUP = $(PYTHON) setup.py
RUN_SPHINX_HTML = make html


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Build the API documentation using Sphinx
.PHONY: doc
doc: $(SOURCES_DOCUMENTATION) $(SOURCES_DOC_CONF)
	($(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(CHDIR) ../doc && PYTHONPATH=.. $(RUN_SPHINX_HTML))
	($(CHDIR) $(SOURCES_DOC_BUILD_HTML_DIR) && $(ZIP) $(SOURCES_DOC_ZIP) *)
	$(CP) $(SOURCES_DOC_BUILD_HTML_DIR)/$(SOURCES_DOC_ZIP) .

# Run a server for writing the documentation
.PHONY: docserver
docserver:
	($(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(CHDIR) ../doc && PYTHONPATH=.. $(RUN_NOTEBOOK))

# Build a source distribution
dist: $(SOURCES_GENERATED)
	$(RUN_SETUP) sdist

# Upload a source distribution to PyPi (has to be done in one command)
upload: $(SOURCES_GENERATED)
	$(RUN_SETUP) sdist upload -r pypi

# Clean up the distribution build 
clean:
	$(RM) $(SOURCES_GENERATED) epyc.egg-info dist $(SOURCES_DOC_BUILD_DIR) $(SOURCES_DOC_ZIP)

# Clean up everything, including the computational environment (which is expensive to rebuild)
reallyclean: clean
	$(RM) $(ENV_COMPUTATIONAL)


# ----- Helper targets -----

# Build a computational environment in which to run the test suite
env-computational: $(ENV_COMPUTATIONAL)

# Build a new, updated, requirements.txt file ready for commiting to the repo
# Only commit if we're sure we pass the test suite!
newenv-computational:
	echo $(PY_COMPUTATIONAL)  $(PY_INTERACTIVE) | $(TR) ' ' '\n' >$(REQ_COMPUTATIONAL)
	make env-computational
	$(NON_REQUIREMENTS) $(ENV_COMPUTATIONAL)/requirements.txt >$(REQ_COMPUTATIONAL)

# Only re-build computational environment if the directory is missing
$(ENV_COMPUTATIONAL):
	$(VIRTUALENV) $(ENV_COMPUTATIONAL)
	$(CP) $(REQ_COMPUTATIONAL) $(ENV_COMPUTATIONAL)/requirements.txt
	$(CHDIR) $(ENV_COMPUTATIONAL) && $(ACTIVATE) && $(PIP) install -r requirements.txt && $(PIP) freeze >requirements.txt


# ----- Generated files -----

# Manifest for the package
MANIFEST: Makefile
	echo  $(SOURCES_EXTRA) $(SOURCES_GENERATED) $(SOURCES_CODE) | $(TR) ' ' '\n' >$@

# The setup.py script
setup.py: $(SOURCES_SETUP_IN) Makefile
	$(CAT) $(SOURCES_SETUP_IN) | $(SED) -e 's/VERSION/$(VERSION)/g' -e 's/REQ_SETUP/$(REQ_SETUP)/g' >$@


# ----- Usage -----

define HELP_MESSAGE
Available targets:
   make test         run the test suite in a suitable virtualenv
   make doc          build the API documentation using Sphinx
   make cluster      run a small compute cluster for use by the tests
   make docserver    run a Jupyter notebook to edit the tutorial
   make dist         create a source distribution
   make upload       upload distribution to PyPi
   make clean        clean-up the build
   make reallyclean  clean up the virtualenv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
