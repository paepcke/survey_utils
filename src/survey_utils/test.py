'''
Created on May 19, 2016

@author: paepcke
'''
import sys
import tempfile
from unittest import skipIf
import unittest

from survey_utils.unfold import OutMethod
from survey_utils.unfold import TableShaper


DO_ALL = False

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
        
    #@skipIf(DO_ALL == False, "Skipping for now") 
    def test_unfold_constant_cols(self):

        self.shaper.unfold(self.survey, 'question', 'answer', constant_cols=['questionType'])
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("Need to run unittest.main() in buffered mode (pass buffer=true).")
        output = sys.stdout.getvalue().strip()
        expected = "question,questionType,v0,v1\r\n" +\
                    "DOB,pullDown,1983,1980\r\n" +\
                    "gender,radio,F,M"
            
        self.assertEquals(expected, output)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    # Run unittest in buffered mode so
    # that some of the tests above can
    # check printed output of unfold():
    
    
    assert not hasattr(sys.stdout, "getvalue")
    unittest.main(module=__name__, buffer=True, exit=False)