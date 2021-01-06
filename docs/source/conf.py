# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
import sphinx

# Adds system path two folders back (where project lives.)
sys.path.insert(0, os.path.abspath("../.."))

# PyLint might complain, but the interpreter should be able to find this on run.
import toolbox

# -- Project information -----------------------------------------------------

project = "Toolbox"
copyright = "2020, Felipe Faria"
author = "Felipe Faria"

# -- General configuration ---------------------------------------------------

# Project Name
html_title = "{}".format(project)

# Order of docs.
autodoc_member_order = "bysource"

# Turn off typehints.
autodoc_typehints = "signature"

# Remove module names from class docs.
add_module_names = False

# Show only class docs.
autoclass_content = "both"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "m2r2",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# PDF Latex Config
latex_elements = {"extraclassoptions": "openany,oneside"}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
