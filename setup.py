import multiprocessing
from setuptools import setup

# Modify mods_to_install to taste.
# If math_utils included, then scipy/numpy
# and matplotlib will be installed as well.
# Modules like 'unfold' are lighter weight:

mods_to_install = ['unfold']
#mods_to_install = ['unfold','math_utils']

mods_to_require = []
if 'unfold' in mods_to_install:
  mods_to_require.append('ordered-set>=2.0.1')
if 'math_utils' in mods_to_install:
  mods_to_require.extend(['scipy>=0.17.0', 'matplotlib>=1.5.0'])

test_requirements = ['nose>=1.0']

setup(
    name = "survey_utils",
    version = "0.0.1",
    py_modules = mods_to_install,

    # Dependencies on other packages:
    setup_requires   = ['nose>=1.1.2'],
    tests_require    = test_requirements,
    install_requires = mods_to_require + test_requirements,

    # Unit tests; they are initiated via 'python setup.py test'
    test_suite       = 'nose.collector', 

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
     #   '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
     #   'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Utilities for managing survey results.",
    license = "BSD",
    keywords = "surveys, table shaping",
    url = "https://github.com/paepcke/survey_utils",   # project home page, if any
)
