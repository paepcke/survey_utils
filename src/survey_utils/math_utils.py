from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

#import pandas
import numpy as np

#-------------------------
# replacZerosNparray()
#----------------- 
def replaceMissingValsNparray(nxmNparray, 
                        direction='column',
                        replacement='median',
                        missing_value=np.nan):
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
               
    Analogously with the mean.
    
    :param nxmNparray: a two-dimensional numpy ndarray
    :type nxmNparray: numpby.ndarray 
    :param direction=: direction along which the median or mean
        is computed for replacing missing values. Options are
        'column' and 'row'
    :type directions=: string
    :param replacement=: whether to compute median or mean of
        the chosen direction (row/column) to replace missing
        values. Options are 'median' and 'mean'
    :type replacement=: string
    :param missing_value: the value that stands for 'value missing'. May be
        zero, numpy.nan, numpy.inf, or any other value.
    :type missing_value: ANY
    :returns new ndarray with zeros replaced.    
    :rtype: numpay.ndarray
    '''
    if direction == 'column':
        vecSize = nxmNparray.shape[1]
    else:
        vecSize = nxmNparray.shape[0]
    
    # For each column or row vector, replace
    # all missing values with the median/mean 
    # of that vector, calculated without those
    # missing values:
    
    for indx in range(vecSize):

        if direction == 'column':
            vec = nxmNparray[:,indx]
        else:
            vec = nxmNparray[indx,:]
        
        # Compute the median/mean for cells
        # of the vector that are missing values:
        if replacement == 'median':
            replacement_value = np.median(non_matches(vec, missing_value))
        else:
            replacement_value = np.mean(non_matches(vec, missing_value))
        
        # Replace the missing value(s) (in the original data):
        replace_matches(vec, missing_value, replacement_value)
        
    return(nxmNparray)

#-------------------------
# replacZerosDataFrame()
#----------------- 


def replaceMissingValsDataFrame(nxmDataFrame, 
                          direction='column',
                          replacement='median',
                          missing_value=np.nan):
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
               
    Analogously with the mean.

    :param nxmDataFrame: a two-dimensional pandas DataFrame 
    :type nxmNparray: pandas.DataFrame
    :param direction=: direction along which the median or mean
        is computed for replacing missing values. Options are
        'column' and 'row'
    :type directions=: string
    :param replacement=: whether to compute median or mean of
        the chosen direction (row/column) to replace missing
        values. Options are 'median' and 'mean'
    :type replacement=: string
    :param missing_value: the value that stands for 'value missing'. May be
        zero, numpy.nan, numpy.inf, or any other value.
    :type missing_value: ANY
    :returns nxmDataFrame with zeros replaced. I.e. returns a *view*, 
        not a copy.    
    :rtype: pandas.DataFrame
    
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

        # Compute the median, disregarding missing values:            
        if replacement == 'median':
            replacement_value = np.median(non_matches(vec, missing_value))
        else:
            replacement_value = np.mean(non_matches(vec, missing_value))

        # Replace the missing value(s) (in the original data):
        replace_matches(vec, missing_value, replacement_value)

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
    Calls scipy.cluster.hierarchy.dendrogram, adding a
    horizontal reference line at a chosen distance. That
    is the reference line is parallel to the x-axis, and
    intersects y-axis at a given distance.
    
    Keyword arguments are as per scipy.cluster.hierarchy.dendrogram,
    plus the ones below.
    
    :param max_d=: distance at which reference line is to be drawn
    :type max_d=: float
    :param annotate_above=: only show details of interior
        hierarchy nodes when distance is > annotate_above.
        I.e. only the higher nodes are detailed. Bottom layers
        are summarized.
    :type annotate_above=: float
    :param x_label=: label for x-axis. Default is 
        'Sample index or (cluster size)'
    :type x_label=: string    
    :param y_label=: label for y-axis. Default is 'Distance'.
    :type y_label=: string
    :param x_axis_font_size=: font size of x-axis label.
        Default: 9pt
    :type x_label=: integer
      - option to add the distance (i.e. y-axis) read-out 
    :param y_axis_font_size=: font size of y-axis label.
        Default: 9pt
    :type x_label=: integer
    :return: the dendrogram
    :rtype: ?
    
      - option to add the distance (i.e. y-axis) read-out 
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

# ----------------------------- Private Utility Functions -------------
        
#-------------------------
# non_matches
#----------------

def non_matches(arr, val):
    '''
    Given a ndarray and an arbitrary 
    value, including np.nan, np.inf, etc.,
    return an ndarray that contains 
    only elements that are *not* equal 
    to val.  
    
    :param arr: n-dimensional numpy array
    :type arr: numpy.ndarray
    :param val: value, including special values numpy.nan, numpy.inf, numpy.neginf, etc.
    :type val: ANY.
    '''
    
    # Special value?
    if np.isfinite(val):
        # No, just normal value:
        return arr[arr != val]
    # Is special value, such as numpy.nan.
    # Create ndarray with True/False entries
    # that reflect which entries are not equal
    # to val:
    elif np.isnan(val):
        cond = np.logical_not(np.isnan(arr))
    elif np.isinf(val):
        cond = np.logical_not(np.isinf(arr))
    elif np.isneginf(val):
        cond = np.logical_not(np.isneginf(arr))
    elif np.isposinf(val):
        cond = np.logical_not(np.isposinf(arr))
        
    # Use the True/False ndarray as a mask
    # over arr:
    return arr[cond]
        
#-------------------------
# replace_matches
#----------------
    
def replace_matches(arr, old_val, new_val):
    
    # Special value?
    if np.isfinite(old_val):
        # No, just normal value:
        arr[arr == old_val] = new_val
        return arr
    # Is special value, such as numpy.nan.
    # Create ndarray with True/False entries
    # that reflect which entries are not equal
    # to val:
    elif np.isnan(old_val):
        arr[np.isnan(arr)] = new_val
        return arr
    elif np.isinf(old_val):
        arr[np.isinf(arr)] = new_val
        return arr
    elif np.isneginf(old_val):
        arr[np.isneginf(arr)] = new_val
        return arr
    elif np.isposinf(old_val):
        arr[np.isposinf(arr)] = new_val
        return arr

    