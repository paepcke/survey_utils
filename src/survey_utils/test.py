'''
Created on May 19, 2016

@author: paepcke
'''
import sys
import tempfile
from unittest import skipIf
import unittest

from survey_utils.unfolding import OutMethod
from survey_utils.unfolding import TableShaper
from cStringIO import StringIO


DO_ALL = True

class TestSurveyUtils(unittest.TestCase):
 
 
    def setUp(self):
        self.shaper = TableShaper()

        self.survey = [['userId','question','questionType','timeAdded','answer'],
                       [10,'DOB','pullDown','Jun2010','1983'],     
                       [10,'gender','radio','May2011','F'],
                       [20,'DOB','pullDown','Jun2010','1980'],
                       [20,'gender','radio','May2011','M']
                       ]
         
        self.surveyBadConst =\
                        [['userId','question','questionType','timeAdded','answer'],
                         [10,'DOB','radio','Jun2010','1983'],   # 'radio' should be 'pullDown'     
                         [10,'gender','radio','May2011','F'],
                         [20,'DOB','pullDown','Jun2010','1980'],
                         [20,'gender','radio','May2011','M']
                        ]
                        
        # Capture stdout in a buffer, so that print-outs
        # by unfold() can be unit-checked:
        self.stdout_saved = sys.stdout
        sys.stdout = StringIO()
        
    def tearDown(self):
        # Restore the real stdout:
        sys.stdout = self.stdout_saved

    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_no_error(self):
        
        self.shaper.unfold(self.survey, 'question', 'answer')
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Need to run unittest.main() in buffered mode (pass buffer=true).")
        output = sys.stdout.getvalue().strip()
        expected = "question,v0,v1\r\n" +\
                    "DOB,1983,1980\r\n" +\
                    "gender,F,M"
            
        self.assertEquals(expected, output)

    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_iterator(self):
        it = self.shaper.unfold(self.survey, 'question', 'answer', out_method=OutMethod.ITERATOR)
        self.assertEqual(['question','v0','v1'], it.next())
        self.assertEqual(['DOB','1983','1980'], it.next())
        self.assertEqual(['gender','F','M'], it.next())
        
    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_to_file(self):
        
        outfile_name = tempfile.NamedTemporaryFile().name
        self.shaper.unfold(self.survey, 'question', 'answer', out_method=OutMethod(outfile_name))
        with open(outfile_name, 'r') as fd:
            self.assertEqual('question,v0,v1', fd.readline().strip())
            self.assertEqual('DOB,1983,1980', fd.readline().strip())
            self.assertEqual('gender,F,M', fd.readline().strip())
                
    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_bad_unfold_col_spec(self):

        # Non-existent unfold col name:
        # Expect ValueError('The column to unfold (%s) does not appear in the table header (%s)' % (self.col_name_to_unfold, header))
        with self.assertRaises(ValueError):
            self.shaper.unfold(self.survey, 'blah-blah', 'answer')

        # Bad unfold col type:
        # Expect: raise ValueError('Must name column that is to be unfolded'):
        with self.assertRaises(ValueError):
            self.shaper.unfold(self.survey, 10, 'answer')
        
    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_one_constant_col(self):
        # Have one constant column:
        self.shaper.unfold(self.survey, 'question', 'answer', constant_cols=['questionType'])
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Need to run unittest.main() in buffered mode (pass buffer=true).")
        output = sys.stdout.getvalue().strip()
        expected = "question,questionType,v0,v1\r\n" +\
                    "DOB,pullDown,1983,1980\r\n" +\
                    "gender,radio,F,M"
            
        self.assertEquals(expected, output)
        
    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_two_constant_cols(self):
        # Have two constant columns:
        self.shaper.unfold(self.survey, 'question', 'answer', constant_cols=['questionType', 'timeAdded'])
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Need to run unittest.main() in buffered mode (pass buffer=true).")
        output = sys.stdout.getvalue().strip()
        expected = "question,questionType,timeAdded,v0,v1\r\n" +\
                    "DOB,pullDown,Jun2010,1983,1980\r\n" +\
                    "gender,radio,May2011,F,M"
            
        self.assertEquals(expected, output)

    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_unequal_constant_cols(self):
        # Make one supposedly constant column be
        # non-constant:
        self.survey[1][2] = 'radio'
        try:
            self.shaper.unfold(self.survey, 'question', 'answer', constant_cols=['questionType', 'timeAdded'])
            # No exception: bad:
            self.fail("Unequal constant-column value 'radio' should have been 'pullDown'")
        except ValueError:
            # Good! Got exception:
            pass

    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_no_error_new_cols_named(self):
        # Have the user-id column provide new columns' header:
        self.shaper.unfold(self.survey, 'question', 'answer', new_col_names_col='userId')
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Need to run unittest.main() in buffered mode (pass buffer=true).")
        output = sys.stdout.getvalue().strip()
        expected = "question,10,20\r\n" +\
                    "DOB,1983,1980\r\n" +\
                    "gender,F,M"
            
        self.assertEquals(expected, output)

    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_two_constant_cols_new_cols_names(self):
        # Have two constant columns:
        self.shaper.unfold(self.survey, 'question', 'answer', constant_cols=['questionType', 'timeAdded'], new_col_names_col='userId')
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Need to run unittest.main() in buffered mode (pass buffer=true).")
        output = sys.stdout.getvalue().strip()
        expected = "question,questionType,timeAdded,10,20\r\n" +\
                    "DOB,pullDown,Jun2010,1983,1980\r\n" +\
                    "gender,radio,May2011,F,M"
            
        self.assertEquals(expected, output)

    @skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_two_constant_cols_new_cols_names_bad_new_col_name_col(self):
        # Raise error: Foo column doesn't exist:
        try:
            self.shaper.unfold(self.survey, 'question', 'answer', constant_cols=['questionType', 'timeAdded'], new_col_names_col='Foo')
            # Shouldn't get here:
            self.fail("Column 'Foo' doesn't exist, so should cause an error.")
        except ValueError:
            # Good: exception:
            pass
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
