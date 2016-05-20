from collections import OrderedDict
import csv
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import sys

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


#-------------------------
# unfold()
#----------------- 

def unfold(in_path_or_2d_array, col_name_to_unfold, col_name_unfold_values, out_path=None, constant_cols=None, new_col_names_col=None):
    '''
    Unfold (reshape) data frame like the following example:
    
       ======   ========   ============   =========   ======
       userId   question   questionType   timeAdded   answer 
       ======   ========   ============   =========   ======
        10      DOB          pullDown       Jun2010    1983     
        10      gender       radio          May2011      F
        20      DOB          pullDown       Jun2010    1980
        20      gender       radio          May2011      M
                         ...
                         
    Let the unfold column be 'question', and the 'constants'
    columns be 'questionType' and 'timeAdded'. You could call the
    function like this:
    
       unfold('/tmp/in.csv', 
              col_name_to_unfold='question'
              col_name_unfold_values='answer'
              out_path='/tmp/out.csv', 
              constant_cols=['questionType','timeAdded'])
              
    The reshaped table looks like this:
    
       ========   ============  =========    ==     ==
       question   questionType  timeAdded    v1     v2   
       ========   ============  =========    ==     ==       
         DOB        pullDown    June2010    1983   1980
       gender        radio       May2011     F       M      
    

    Each line is now one question. All answers to one question
    are columns in that question's row. It is an error to have
    inconsistencies in the constants-columns. For instance,
    if the original row "20  DOB   pullDown..." had been
    "20  DOB  radio" an error would have been raised. All constant-col
    field values for the same question (in different rows of the original)
    must match. 
    
    Another way to call the function controls the names of the new
    columns. One column  can be specified to provide the column headers:
    
       unfold('/tmp/in.csv',
              col_name_to_unfold='question'
              col_name_unfold_values='answer'
              out_path='/tmp/out.csv', 
              constant_cols=['questionType','timeAdded'],
              new_col_names_com='userId)
              
    The reshaped table would look like this:
    
       ========   ============  =========    ==     ==
       question   questionType  timeAdded    10     20
       ========   ============  =========    ==     ==       
         DOB        pullDown    June2010    1983   1980
       gender        radio       May2011     F       M      
              
     
     I.e. the user id values are used as the column headers
     of the new table.
                       
     
    :param in_path_or_2d_array: location of input CSV file, or
        an array of arrays. First row must be column names.
    :type in_path_or_2d_array: {string | [[]]}
    :param col_name_to_unfold: name of the column to unfold into columns
    :type col_name_to_unfold: string
    :param col_name_unfold_values: column name of the unfold values, i.e. the values 
         in rows under the new columns 
    :type col_name_unfold_values: string 
    :param out_path: where to put the output CSV. If None,
         new table is written to stdout.
    :type out_path: {None | string}
    :param constant_cols: names of columns that are to be retained 
    :type constant_cols: {None | [string]}
    :param new_col_names_col: name of column to use for column names of new columns
    :type new_col_names_col: {None | string}
    '''
    
    if type(col_name_to_unfold) != str:
        raise ValueError('Must name column that is to be unfolded')
    
    if new_col_names_col is not None and type(new_col_names_col) != str:
        raise ValueError('New-column prefix must be a string, was %s' % new_col_names_col)
    
    if constant_cols is not None and type(constant_cols) != list:
        raise ValueError('Parameter constant_cols must be None or a list of column names.')
    else:
        # constant_cols is None:
        constant_cols = []
    
    if new_col_names_col is None:
        # String for creating names for the new columns.
        # The string is prefixed to 1,2,3,...: 'v' for 'value':
        new_col_prefix = 'v'
    
    try:
        if type(in_path_or_2d_array) == str:
            reader = csv.reader(open(in_path_or_2d_array, 'r'), delimiter=',') 
        else:
            reader = iter(in_path_or_2d_array)
        
        # Header:
        header = reader.next()
        
        # If we are to use the value of a column to name
        # new columns created for the unfolded values, 
        # ensure the col exists:
        
        if new_col_names_col is not None:
            try:
                new_cols_col_indx = header.index(new_col_names_col)
            except IndexError:
                raise ValueError('Specified column %s as source of col names for unfolded columns, but no such column exists' % new_col_names_col)
        
        # Place to accumulated the unfolded values:
        unfolded_values_dict = OrderedDict()
        
        # Place to hold the columns that are constant:
        const_col_dict = OrderedDict()
        
        # Place to hold names for new columns:
        new_col_names = []
        
        try:
            col_indx_to_unfold = header.index(col_name_to_unfold)
        except IndexError:
            raise ValueError('The column to unfold (%s) does not appear in the table header (%s)' % (col_name_to_unfold, header)) 
        try:
            col_indx_of_values = header.index(col_name_unfold_values)
        except IndexError:
            raise ValueError('The column of unfold values (%s) does not appear in the table header (%s)' % (col_name_unfold_values, header)) 
        
        for row in reader:
            
            # Field value of the unfold-column that is key of rows in new tbl
            # e.g. 'DOB' or 'gender':
            unfold_key = row[col_indx_to_unfold]
            
            # Encountered this key (i.e. unfold-col value) before?
            # If not, init with empty array of that key's value for
            # the subject who is represented by this row.
            # We'll end up with this: {'DOB' : ['1983', '1980'], 'gender' : ['M','F']}:
            collected_values = unfolded_values_dict.get(unfold_key, [])
            
            # Value of this unfold-key in this row (e.g. '1983' or 'M'):
            unfold_value = row[col_indx_of_values]
            collected_values.append(unfold_value)
            unfolded_values_dict[unfold_key] = collected_values
            
            # Now take care of constant columns
            # and remembering column names that are
            # based on each row's field value of a
            # column specified by the caller:

            for col_num in range(len(row)):
                try:
                    col_name = header[col_num]
                except IndexError:
                    raise ValueError('Row %s has more columns than header (%s)' % (col_num, header))
                col_value = row[col_num]
                
                # Is this column constant for a given pivot column value?
                if col_name in constant_cols:
                    const_col_key = col_name+col_name_to_unfold
                    col_constant = const_col_dict.get(const_col_key, None)
                    # If it's constant for the fold-pivot, and we noted its 
                    # value earlier, compare to ensure that they are really
                    # equal:
                    if col_constant is None:
                        const_col_dict[const_col_key] = row[col_num]
                    else:
                        # Saw value for this column and pivot value earlier:
                        if col_value != col_constant:
                            raise ValueError("Column that is supposedly constant for a given pivot value is not: %s != %s" %\
                                             (col_value, col_constant))
                            
                # Are we to use an existing column as source for
                # names of new columns?
                
                if new_col_names_col is not None:
                    new_col_names.append(row[new_cols_col_indx])
                 
    finally:
        if type(in_path_or_2d_array) == str:
            reader.close()
                      
    # Create CSV: col_name_to_unfold, constant_cols[0], constant_cols[1], ..., unfolded-values-columns
    # Find the longest row of unfolded values, so that we can pad
    # them with zeroes:
    
    unfolded_max_len = 0
    for unfolded_value in unfolded_values_dict.keys():
        num_unfolded_values = len(unfolded_values_dict[unfolded_value])
        unfolded_max_len = max(num_unfolded_values, unfolded_max_len)
        
    # Do the writing-out:
    try:
        if out_path is not None:
            fd = open(out_path, 'w')
        else:
            fd = sys.stdout

        writer = csv.writer(fd)
        # Header: start with the column name that was unfolded:
        header = [col_name_to_unfold]
        
        # Continue with any columns that were constant for 
        # any given unfold-value:
        header.extend(const_col_dict.keys())
            
        # Finally: invent names for all the unfolded values
        # that are now columns; or the caller specified a  
        # new_col_names_col, and we accumulated values
        # from that column-name-providing column in new_col_names

        if new_col_names_col is not None:
            header.extend(new_col_names)
        else:
            # Invent names for the new columns: v<n>:
            for indx in range(unfolded_max_len):
                header.append('%s%s' % (new_col_prefix, indx))

        writer.writerow(header)
        # Each new row is about one of the unfolded values,
        # like 'question' in the example:
        for unfold_key in unfolded_values_dict.keys():
            new_row = [unfold_key]
            # Add constant-column values if any:
            for col_name in constant_cols:
                const_col_key = col_name+col_name_to_unfold
                col_constant = const_col_dict[const_col_key]
                new_row.append(col_constant)
            
            
            unfolded_values = unfolded_values_dict[unfold_key]
            # Fill short-row vectors with zeros:
            unfolded_values = unfolded_values + (unfolded_max_len - len(unfolded_values))*[0]
            new_row.extend(unfolded_values)
            writer.writerow(new_row)
    finally:
        if out_path is not None:
            fd.close()
        
    
