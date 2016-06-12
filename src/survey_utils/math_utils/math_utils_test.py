'''
Created on May 22, 2016

@author: paepcke
'''
import unittest
from unittest import skipIf

import numpy as np
import pandas as pn

from survey_utils.math_utils.math_utils import replaceMissingValsNparray, replaceMissingValsDataFrame
from survey_utils.math_utils.math_utils import replace_matches, non_matches
from survey_utils.math_utils import math_utils

DO_ALL = True

class TestMathUtils(unittest.TestCase):


    def setUp(self):
        self.arr = np.array([[ 1,  2,  3, 13],
                        	 [ 4,  0,  6, 14],
                        	 [ 4,  8,  9, 15],
                        	 [10, 11, 12, 16]])

        self.arr_nan = np.array([[ 1,  2,  3, 13],
                            	 [ 4,  np.nan,  6, 14],
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
                        	             [ 4,  7,  6, 14],
                        	             [ 4,  8,  9, 15],
                        	             [10, 11, 12, 16]])
                
        self.arr_mean_by_row = np.array([[ 1,  2,  3, 13],
                        	    		 [ 4,  8,  6, 14],
                        	    		 [ 4,  8,  9, 15],
                        	    		 [10, 11, 12, 16]])
        
        self.frm = pn.DataFrame([[ 1,  2,  3, 13],
                            	 [ 4,  0,  6, 14],
                            	 [ 4,  8,  9, 15],
                            	 [10, 11, 12, 16]])
            
        self.frm_nan = pn.DataFrame([[ 1,  2,  3, 13],
                                	 [ 4,  np.nan,  6, 14],
                                	 [ 4,  8,  9, 15],
                                	 [10, 11, 12, 16]])
            
    def tearDown(self):
        pass

    # ------------  TestMathUtils Numpy Array Missing Values Replacement --------------

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_nparray_median_replace_col(self):
        res = replaceMissingValsNparray(self.arr, 
                                        direction='column',
                                        replacement='median',
                                        missing_value=0)
        self.assertTrue(np.array_equal(self.arr_median_by_col,res))
    
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_nparray_nan_median_replace_col(self):
        # Default 'missing_value' is np.nan:
        res = replaceMissingValsNparray(self.arr_nan, 
                                        direction='column',
                                        replacement='median')
        self.assertTrue(np.array_equal(self.arr_median_by_col, res))
        
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_nparray_median_replace_row(self):
        res = replaceMissingValsNparray(self.arr, 
                                        direction='row',
                                        replacement='median',
                                        missing_value=0)
        self.assertTrue(np.array_equal(self.arr_median_by_row, res))
        
        
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_nparray_mean_replace_col(self):
        res = replaceMissingValsNparray(self.arr, 
                                        direction='column',
                                        replacement='mean',
                                        missing_value=0)
        self.assertTrue(np.array_equal(self.arr_mean_by_col, res))
        

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_nparray_nan_mean_replace_col(self):
        res = replaceMissingValsNparray(self.arr_nan, 
                                  direction='column',
                                  replacement='mean')
        self.assertTrue(np.array_equal(self.arr_mean_by_col, res))

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_nparray_mean_replace_row(self):
        res = replaceMissingValsNparray(self.arr, 
                                        direction='row',
                                        replacement='mean',
                                        missing_value=0)
        self.assertTrue(np.array_equal(self.arr_mean_by_row, res))
        
    # ------------  TestMathUtils DataFrame Missing Values Replacement --------------

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_frame_median_replace_col(self):
        res = replaceMissingValsDataFrame(self.frm, 
                                          direction='column',
                                          replacement='median',
                                          missing_value=0)
        self.assertTrue(np.array_equal(self.arr_median_by_col, res))

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_frame_median_replace_row(self):
        res = replaceMissingValsDataFrame(self.frm, 
                                          direction='row',
                                          replacement='median',
                                          missing_value=0)
        self.assertTrue(np.array_equal(self.arr_median_by_row, res))

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_frame_mean_replace_col(self):
        res = replaceMissingValsDataFrame(self.frm, 
                                          direction='column',
                                          replacement='mean',
                                          missing_value=0)
        self.assertTrue(np.array_equal(self.arr_mean_by_col, res))  

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_frame_mean_replace_row(self):
        res = replaceMissingValsDataFrame(self.frm, 
                                          direction='row',
                                          replacement='mean',
                                          missing_value=0)
        self.assertTrue(np.array_equal(self.arr_mean_by_row, res))

    @skipIf(DO_ALL != True, 'skip this one.')
    def test_frame_nan_mean_replace_row(self):
        res = replaceMissingValsDataFrame(self.frm_nan, 
                                          direction='row',
                                          replacement='mean')
        self.assertTrue(np.array_equal(self.arr_mean_by_row, res))

      
    #---------------------------- Array Element Extraction/Replacement Utils ----------------
    
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_replace_matches(self):
        # Replace missing values being zeros:
        new_arr = replace_matches(self.arr, 0, 8)
        self.assertTrue(np.array_equal(self.arr_median_by_col, new_arr))
        
        # Replace missing values being NaN:
        new_arr = replace_matches(self.arr_nan, np.nan, 8)
        self.assertTrue(np.array_equal(self.arr_median_by_col, new_arr))
        
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_non_matches(self):
        # TestMathUtils with getting zeros removed:
        new_arr = non_matches(self.arr[1,:], 0)
        self.assertTrue(np.array_equal(new_arr, np.array([4,6,14])))
        
        # TestMathUtils with getting NaN removed:
        new_arr = non_matches(self.arr_nan[1,:], np.nan)
        self.assertTrue(np.array_equal(new_arr, np.array([4,6,14])))
        
    @skipIf(DO_ALL != True, 'skip this one.')
    def test_get_nearest(self):
        rev = pn.Series([0,390.40,725.134,830.0])
        self.assertEqual((390.4,1),math_utils.get_nearest(rev, 11))
        self.assertEqual((0,0), math_utils.get_nearest(rev, 11, pick='smaller'))
        self.assertEqual((0,0), math_utils.get_nearest(rev, 0))
        self.assertEqual((830.0, 3), math_utils.get_nearest(rev, 840))
        self.assertEqual((390.4,1), math_utils.get_nearest(rev, 390.4))
        self.assertEqual((390.4,1), math_utils.get_nearest(rev, 390.4, pick='larger'))
        self.assertEqual((390.4,1), math_utils.get_nearest(rev, 390.4, pick='smaller'))                                
        
    #---------------------------- Main ----------------
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestMathUtils.testName']
    unittest.main()