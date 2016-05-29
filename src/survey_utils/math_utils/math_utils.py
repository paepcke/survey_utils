
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

    