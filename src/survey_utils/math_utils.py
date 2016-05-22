from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

#import pandas
import numpy as np

#-------------------------
# replacZerosNparray()
#----------------- 
def replaceZerosNparray(nxmNparray, 
                        direction='column',
                        replacement='median'):
    '''
    Given nxm nparray, replace every zero
    with the median/mean of either the cell's row 
    or column (direction), computed without considering 
    the 0-cell. Replaces in place, but also 
    returns the nparray.
    
    Ex (watch the zero cell):
       Given direction='column', and 
       replacement='median', the following input:
       
        array([[ 1,  2,  3, 13],
               [ 4,  0,  6, 14],
               [ 4,  8,  9, 15],
               [10, 11, 12, 16]])
               
        is turned into:
        array([[ 1,  2,  3, 13],
               [ 4,  8,  6, 14],
               [ 4,  8,  9, 15],
               [10, 11, 12, 16]])
    
        But passing 'row' as direction
        and the same input as above, the
        input is turned into:
    
        array([[ 1,  2,  3, 13],
               [ 4,  6,  6, 14],
               [ 4,  8,  9, 15],
               [10, 11, 12, 16]])
               
    Analogously with the mean:
    '''
    if direction == 'column':
        vecSize = nxmNparray.shape[1]
    else:
        vecSize = nxmNparray.shape[0]
    
    # For each column or row vector, replace
    # all 0s with the median of that vector,
    # calculated without those 0s:
    
    for indx in range(vecSize):

        if direction == 'column':
            vec = nxmNparray[:,indx]
        else:
            vec = nxmNparray[indx,:]
        
        # Compute the median/mean for cells
        # of the vector that are 0:
        if replacement == 'median':
            newVec = np.median(vec[vec > 0])
        else:
            newVec = np.mean(vec[vec > 0])
        
        # Replace the zero (in the original data):
        vec[vec == 0] = newVec
        
    return(nxmNparray)

#-------------------------
# replacZerosDataFrame()
#----------------- 


def replaceZerosDataFrame(nxmDataFrame, 
                          direction='column',
                          replacement='median'):
    '''
    Given nxm pandas DataFrame, replace every zero
    with the median/mean of either the cell's row 
    or column (direction), computed without considering 
    the 0-cell. Replaces in place, but also 
    returns the data frame:
    
    Ex (watch the zero cell):
       Given direction='column', and 
       replacement='median', the following input:
       
        array([[ 1,  2,  3, 13],
               [ 4,  0,  6, 14],
               [ 4,  8,  9, 15],
               [10, 11, 12, 16]])
               
        is turned into:
        array([[ 1,  2,  3, 13],
               [ 4,  8,  6, 14],
               [ 4,  8,  9, 15],
               [10, 11, 12, 16]])
    
        But passing 'row' as direction
        and the same input as above, the
        input is turned into:
    
        array([[ 1,  2,  3, 13],
               [ 4,  6,  6, 14],
               [ 4,  8,  9, 15],
               [10, 11, 12, 16]])
               
    Analogously with the mean:
    '''
    if direction == 'column':
        vecSize = nxmDataFrame.shape[1]
    else:
        vecSize = nxmDataFrame.shape[0]    

    # Get the column headers. They may be
    # user-set, or automatically set to ints.
    # We'll use them to grab columns:
    
    colNames = nxmDataFrame.columns
        
    # For each column vector, replace
    # all 0s with the median of that vector,
    # calculated without those 0s:
    
    for indx in range(vecSize):
        if direction == 'column':
            # For data frames, ints or vecs of ints
            # inside [] select columns:
            vec = nxmDataFrame[colNames[indx]].copy()
        else:
            # For data frames, slices
            # inside [] select rows. Must
            # make a copy, else pandas gives
            # warning when modified vector is
            # later assigned as a row:
            vec = nxmDataFrame.iloc[indx].copy()
            
        # Compute the median, disregarding 0s:
        if replacement == 'median':
            newVal = np.median(vec[vec > 0])
        else:
            newVal = np.mean(vec[vec > 0])
            
        # Replace the 0s:
        vec[vec == 0] = newVal
        
        # Replace the row/column in the original(!)        
        if direction == 'column':
            nxmDataFrame[colNames[indx]] = vec
        else:
            nxmDataFrame.iloc[indx] = vec
        
    return(nxmDataFrame)

#-------------------------
# fancy_dendrogram()
#----------------- 

def fancy_dendrogram(*args, **kwargs):
    '''
    Calls scipy.cluster.hierarchy.dendrogram, adding:
      - a horizontal reference line controlled by kwarg max_d=
      - option to add the distance (i.e. y-axis) read-out 
      - horizontal cluster links whose distance is larger
        then kwarg annotate_above=
      - labels Y-axis with content of kwarg y_label=,
        or with the default 'Distance'
      - labels X-axis either with content of kwarg x_label=
        or with the default 'Sample index or (cluster size)'
      - x-axis fontsize is kwarg x_axis_font_size= or 9pt
      - y-axis fontsize is kwarg y_axis_font_size= or 9pt
    '''
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d

    annotate_above = kwargs.pop('annotate_above', 0)

    y_label = kwargs.pop('y_label', 'Distance')
    x_label = kwargs.pop('x_label', 'Sample index or (cluster size)')
    x_axis_font_size = kwargs.pop('x_axis_font_size', 9)
    y_axis_font_size = kwargs.pop('y_axis_font_size', 9)    

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel(x_label, fontsize=x_axis_font_size)
        plt.ylabel(y_label, fontsize=y_axis_font_size)
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata   


        
    
