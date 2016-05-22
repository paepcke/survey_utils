import multiprocessing
from setuptools import setup, find_packages


test_requirements = ['nose>=1.0']

setup(
    name = "survey_utils",
    version = "0.0.1",
    packages = find_packages(),

    # Dependencies on other packages:
    setup_requires   = ['nose>=1.1.2'],
    tests_require    = test_requirements,
    install_requires = ['ordered-set>=2.0.1'
			] + test_requirements,

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
