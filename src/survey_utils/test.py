'''
Created on May 19, 2016

@author: paepcke
'''
import unittest
from utils import unfold

class TestSurveyUtils(unittest.TestCase):


    def setUp(self):
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

    def tearDown(self):
        pass


    def test_unfold_no_error(self):
        unfold(self.survey, 'question', 'answer')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()