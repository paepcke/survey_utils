from setuptools import setup

from distutils.command.install import install, Command
from distutils.tests import test_cmd
import os,sys, unittest

sys.path.append(os.path.join(os.getcwd(), 'src'))

mods_to_install = []
mods_to_test    = []

class InstallCommand(install):

    description = "Installs the survey_utils package; allows specification of modules to include."

    # Add your new user options to the
    # ones that are baked into the install
    # command by default. Each new CLI option
    # is a triplet:
    #
    #   long_name, short_name, help_text
    #
    # Add a '=' after the long name if the
    # option requires an argument. Use None
    # if you don't want to allow a short option.
    #
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
        # Install math_utils only if explicitly
        # requested in the -m/--module option,
        # or if 'all' is requested
        if self.module == 'unfolding':
            mods_to_install = ['unfold']
        elif self.module in ['math_utils', 'all']:
            mods_to_install = ['unfold', 'math_utils']
        else:
            # No module arg given on the command line.
            # Require it for the install command, so that
            # user doesn't unexpectedly install all of
            # numpy/scipy:
         
            print("Must provide --module [unfolding | math_utils | all]. Install aborted.")
            sys.exit()
        
        install.run(self)


class TestCommand(Command):

    description = "The the survey_utils; allows specification of module to include"

    # Add these new user options to the
    # ones that are baked into the install
    # command by default:
    
    user_options = [
        ('module=', 'm', "Specify 'unfolding', 'math_utils', or 'all'."),
    ] + install.user_options

    def initialize_options(self):
        # *Must* initialize any options you introduced
        # in user_options. Else parent's finalize_options
        # won't read the option from the command line at
        # all!!!!
        self.module = None

    def finalize_options(self):
        assert self.module in (None, 'unfolding', 'math_utils', 'all'), 'Invalid module!'
        
    def run(self):
        if self.module == 'unfolding':
            from survey_utils.unfolding_test import TestUnfolding
            mods_to_test = [TestUnfolding]
        elif self.module == 'math_utils':
            from survey_utils.math_utils_test import TestMathUtils
            mods_to_test = [TestMathUtils]
        elif self.module == 'all':
            from survey_utils.unfolding_test import TestUnfolding
            from survey_utils.math_utils_test import TestMathUtils
            mods_to_test = [TestUnfolding, TestMathUtils]
        else:
            # No modules arg given on the command line.
            # Require it for the test command, so that
            # user doesn't unexpectedly install all of
            # numpy/scipy:
         
            print("Must provide --module [unfolding | math_utils | all]. Test aborted.")
            sys.exit()
        
        for test_class in mods_to_test:
            test_cmd.run_unittest(unittest.makeSuite(test_class))


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
      'install': InstallCommand,
      'test': TestCommand
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
