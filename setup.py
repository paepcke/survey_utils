from setuptools import setup

from distutils.command.install import install
import os,sys

sys.path.append(os.path.join(os.getcwd(), 'src'))

mods_to_install = []

class InstallCommand(install):

    description = "Installs the unfolding package."
    user_options = [
        ('module=', 'm', "Specify 'unfolding', 'math_utils', or 'all'."),
    ] + install.user_options

    def initialize_options(self):
        install.initialize_options(self)
        # *Must* initialize any options you introduced
        # in user_options. Else parent's finalize_options
        # won't read the option from the command line at
        # all!!!!
        self.module = None

    def finalize_options(self):
        install.finalize_options(self)
        assert self.module in (None, 'unfolding', 'math_utils', 'all'), 'Invalid module!'
        
    def run(self):
        if self.module == 'unfolding':
            mods_to_install = ['unfold']
        elif self.module in ['math_utils', 'all']:
            mods_to_install = ['unfold', 'math_utils']
        else:
            # No modules arg given on the command line.
            # Require it for the install command, so that
            # user doesn't unexpectedly install all of
            # numpy/scipy:
         
            print("Must provide --modules [unfolding | math_utils | all]. Install aborted.")
            sys.exit()
        
        install.run(self)

mods_to_require = []
if 'unfold' in mods_to_install:
    mods_to_require.append('ordered-set>=2.0.1')
if 'math_utils' in mods_to_install:
    mods_to_require.extend(['scipy>=0.17.0',
                            'matplotlib>=1.5.0',
                            'pandas>=0.17.1',
                            'freetype-py>=1.0.2',
                            ])

test_requirements = ['nose>=1.0']

setup(
    name = "survey_utils",
    version = "0.0.1",
    py_modules = mods_to_install,
    cmdclass = {
      'install': InstallCommand
      },

    # Dependencies on other packages:
    setup_requires   = ['nose>=1.3.7',
            'numpy>=1.11.0'
            ],
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
