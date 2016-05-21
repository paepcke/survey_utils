'''
Created on May 20, 2016

@author: paepcke
'''
from collections import OrderedDict
import csv
import sys

class OutMethod():
    '''
    Enumeration-like entity used as parameter
    to TableShaper.unfold() to control where output
    is written:
    
       OutMethod.ITERATOR --> 0
       OutMethod.STDOUT   --> 1
       OutMethod.FILE     --> AttributeError
       
    But: OutMethod('/tmp/trash.txt').FILE --> '/tmp/trash.txt'
    To get output unfold() output to go to file /tmp/trash.txt, 
    use the above expression for the out_method parameter. 
    Then, within the unfold() method OutMethod.FILE will 
    return the file name. 
    '''
    ITERATOR = 0
    STDOUT   = 1
    
    def __init__(self, file_path=None):
        self.FILE = file_path

class TableShaper(object):

#-------------------------
# unfold()
#----------------- 

    def unfold(self,
               in_path_or_2d_array, 
               col_name_to_unfold, 
               col_name_unfold_values, 
               out_method=OutMethod.STDOUT, 
               constant_cols=None, 
               new_col_names_col=None):
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
                  constant_cols=['questionType','timeAdded'],
                  new_col_names_col='userId)
                  
        The reshaped table would look like this:
        
           ========   ============  =========    ==     ==
           question   questionType  timeAdded    10     20
           ========   ============  =========    ==     ==       
             DOB        pullDown    June2010    1983   1980
           gender        radio       May2011     F       M      
                  
         
         I.e. the user id values are used as the column headers
         of the new table.
         
         To have the function behave like an iterator:
         
           it = unfold('/tmp/in.csv',
                      col_name_to_unfold='question'
                      col_name_unfold_values='answer'
                      constant_cols=['questionType','timeAdded'],
                      out_method=OutMethod.ITERATOR)
           for row in it:
               print(row)
               
        To write the output to a file:
        
           unfold('/tmp/in.csv',
                  col_name_to_unfold='question'
                  col_name_unfold_values='answer'
                  constant_cols=['questionType','timeAdded'],
                  new_col_names_col='userId,
                  out_method=OutMethod('/tmp/trash.csv')
        
         
        :param in_path_or_2d_array: location of input CSV file, or
            an array of arrays. First row must be column names.
        :type in_path_or_2d_array: {string | [[]]}
        :param col_name_to_unfold: name of the column to unfold into columns
        :type col_name_to_unfold: string
        :param col_name_unfold_values: column name of the unfold values, i.e. the values 
             in rows under the new columns 
        :type col_name_unfold_values: string 
        :param out_method: where to put the output CSV. If omitted,
             new table is written to stdout.
        :type out_method: OutMethod
        :param constant_cols: names of columns that are to be retained 
        :type constant_cols: {None | [string]}
        :param new_col_names_col: name of column to use for column names of new columns
        :type new_col_names_col: {None | string}
        '''
        
        # Error checking and initializations:
        
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
        
        # Place to accumulated the unfolded values:
        unfolded_values_dict = OrderedDict()
        
        # Place to hold the columns that are constant:
        const_col_dict = OrderedDict()
        
        # Place to hold names for new columns:
        new_col_names = []
        
        
        try:
            if type(in_path_or_2d_array) == str:
                reader = csv.reader(open(in_path_or_2d_array, 'r'), delimiter=',') 
            else:
                reader = iter(in_path_or_2d_array)
    
            # Look at in-table's header line and get various
            # constants initialized:
                    
            (col_indx_to_unfold, col_indx_of_values, header, new_cols_col_indx) =\
                self.process_in_header_line(col_name_to_unfold, col_name_unfold_values, new_col_names_col, reader) 
            
            # Read the rows and create in-memory representation
            # of transformed structure:
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
            (writer, fd) = self.make_writer(out_method)
                
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
    
            if out_method == OutMethod.ITERATOR:
                self.yield_row(header)
            else:
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
                if out_method == OutMethod.ITERATOR:
                    self.yield_row(new_row)
                else:
                    writer.writerow(new_row)
        finally:
            if out_method == OutMethod.ITERATOR:
                raise StopIteration
            elif out_method != OutMethod.STDOUT:
                fd.close()
                
    def yield_row(self, row):
        yield row
    
    def make_writer(self, out_method):
    # Obtain a csv writer object if function is
    # not called as a generator:
        if out_method != OutMethod.ITERATOR and out_method != OutMethod.STDOUT:
            fd = open(out_method, 'w')
        elif out_method == OutMethod.STDOUT:
            fd = sys.stdout
        else:
            fd = None
        if fd is not None:
            writer = csv.writer(fd)
        return (writer, fd)
    
    def process_in_header_line(self, col_name_to_unfold, col_name_unfold_values, new_col_names_col, reader):
    
        header = reader.next()
        
        # If we are to use the value of a column to name
        # new columns created for the unfolded values,
        # ensure the col exists:
        
        if new_col_names_col is not None:
            try:
                new_cols_col_indx = header.index(new_col_names_col)
            except IndexError:
                raise ValueError('Specified column %s as source of col names for unfolded columns, but no such column exists' % new_col_names_col)
        else:
            new_cols_col_indx = None
        try:
            col_indx_to_unfold = header.index(col_name_to_unfold)
        except IndexError:
            raise ValueError('The column to unfold (%s) does not appear in the table header (%s)' % (col_name_to_unfold, header))
        try:
            col_indx_of_values = header.index(col_name_unfold_values)
        except IndexError:
            raise ValueError('The column of unfold values (%s) does not appear in the table header (%s)' % (col_name_unfold_values, header))
        return (col_indx_to_unfold, col_indx_of_values, header, new_cols_col_indx)

            
survey = [['Userid','Question','Questiontype','Timeadded','Answer'],
               [10,'Dob','Pulldown','Jun2010','1983'],     
               [10,'Gender','Radio','May2011','f'],
               [20,'Dob','Pulldown','Jun2010','1980'],
               [20,'Gender','Radio','May2011','m']
               ]

shaper = TableShaper()

shaper.unfold(survey, 'Question', 'Answer', out_method=OutMethod.STDOUT)
    
            
        