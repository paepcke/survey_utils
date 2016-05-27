import multiprocessing
from setuptools import setup

import os,sys
sys.path.append(os.path.join(os.getcwd(), 'src'))

test_requirements = ['nose>=1.0']

setup(
    name = "survey_utils",
    version = "0.0.2",

    # Dependencies on other packages:
    setup_requires   = ['nose>=1.3.7',
			'numpy>=1.11.0'
			],
    tests_require    = test_requirements,
    #install_requires = test_requirements,

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
