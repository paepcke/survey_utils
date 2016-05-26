'''
Created on May 26, 2016

@author: paepcke
'''

from unittest import skipIf
import unittest

import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import linkage
from plotting_utils import fancy_dendrogram

DO_DENDROGRAM = True

class TestPlotting(unittest.TestCase):


    def testName(self):
        pass

    #---------------------------- Dendrogram ----------------
    
    @skipIf(DO_DENDROGRAM != True, 'skip this one.')    
    def test_fancy_dendrogram(self):
        '''
        Generates a dendrogram in a new window. No
        way to assert anythying.
        '''
        # generate two clusters: a with 100 points, b with 50:
        np.random.seed(4711)  # for repeatability of this tutorial
        a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
        b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
        X = np.concatenate((a, b),)        

        # generate the linkage matrix
        Z = linkage(X, 'ward')

        fancy_dendrogram(
            Z,
            truncate_mode='lastp',
            p=12,
            leaf_rotation=90.,
            leaf_font_size=12.,
            show_contracted=True,
            annotate_above=10  # useful in small plots so annotations don't overlap
            )

        plt.show()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()