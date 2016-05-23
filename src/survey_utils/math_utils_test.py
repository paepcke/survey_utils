'''
Created on May 22, 2016

@author: paepcke
'''
import unittest
from unittest import skipIf

import numpy as np
from math_utils import replaceZerosNparray
from IPython.external.decorators._decorators import skipif

DO_ALL = True

class Test(unittest.TestCase):


    def setUp(self):
        self.arr = np.array([[ 1,  2,  3, 13],
                        	 [ 4,  0,  6, 14],
                        	 [ 4,  8,  9, 15],
                        	 [10, 11, 12, 16]])
        
        self.arr_median_by_col = np.array([[ 1,  2,  3, 13],
                                           [ 4,  8,  6, 14],
                                           [ 4,  8,  9, 15],
                                           [10, 11, 12, 16]])
        
        self.arr_median_by_row = np.array([[ 1,  2,  3, 13],
                                           [ 4,  6,  6, 14],
                                           [ 4,  8,  9, 15],
                                           [10, 11, 12, 16]])
        
        self.arr_mean_by_col = np.array([[ 1,  2,  3, 13],
                        	             [ 4,  10.5,  6, 14],
                        	             [ 4,  8,  9, 15],
                        	             [10, 11, 12, 16]])
                
        self.arr_mean_by_row = np.array([[ 1,  2,  3, 13],
                        	    		 [ 4,  12,  6, 14],
                        	    		 [ 4,  8,  9, 15],
                        	    		 [10, 11, 12, 16]]) 
    def tearDown(self):
        pass


    @skipIf(DO_ALL != True, 'skip this one.')
    def test_median_replace_col(self):
        res = replaceZerosNparray(self.arr, 
                                  direction='column',
                                  replacement='median')
        self.assertEqual(self.arr_median_by_col.all(), res.all())
        
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_median_replace_row(self):
        res = replaceZerosNparray(self.arr, 
                                  direction='row',
                                  replacement='median')
        self.assertEqual(self.arr_median_by_row.all(), res.all())
        
        
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_mean_replace_col(self):
        res = replaceZerosNparray(self.arr, 
                                  direction='column',
                                  replacement='mean')
        self.assertEqual(self.arr_mean_by_col.all(), res.all())

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_mean_replace_row(self):
        res = replaceZerosNparray(self.arr, 
                                  direction='row',
                                  replacement='mean')
        self.assertEqual(self.arr_mean_by_row.all(), res.all())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()