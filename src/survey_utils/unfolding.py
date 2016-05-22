'''
Created on May 20, 2016

@author: paepcke
'''
import argparse
from collections import OrderedDict
import csv
import os
import sys

from ordered_set import OrderedSet


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
    # unfold
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
         
         To have the function behave like an iterator
         (each item will be an array with one row of the
          reshaped table):
         
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
        else:
            self.col_name_to_unfold = col_name_to_unfold
        
        if new_col_names_col is not None and type(new_col_names_col) != str:
            raise ValueError('New-column prefix must be a string, was %s' % new_col_names_col)
        self.new_col_names_col = new_col_names_col
        if new_col_names_col is None:
            # No col specified to provide column headers
            # for new columns:
            # String for creating names for the new columns.
            # The string is prefixed to 1,2,3,...: 'v' for 'value':
            self.new_col_prefix = 'v'
        
        if constant_cols is not None:
            if type(constant_cols) != list:
                raise ValueError('Parameter constant_cols must be None or a list of column names.')
            self.constant_cols = constant_cols
        else:
            # constant_cols is None:
            self.constant_cols = []
        
        self.out_method = out_method
        self.col_name_unfold_values = col_name_unfold_values
        
        # Place to accumulated the unfolded values:
        self.unfolded_values_dict = OrderedDict()
        
        # Place to hold the columns that are constant:
        self.const_col_dict = OrderedDict()
        
        # Place to hold names for new columns:
        self.new_col_names = OrderedSet()
        
        try:
            if type(in_path_or_2d_array) == str:
                # Get in-table from a file:
                in_fd = open(in_path_or_2d_array, 'r')
                reader = csv.reader(in_fd, delimiter=',') 
            else:
                # Get in-table from a 2d array:
                reader = iter(in_path_or_2d_array)
                in_fd = None
    
            # Look at in-table's header line and get various
            # constants initialized:
                    
            self.header = self.process_in_header_line(reader) 
            
            # Read the rows and create in-memory representation
            # of transformed structure:
            for row in reader:
                
                # Field value of the unfold-column that is key of rows in new tbl
                # e.g. 'DOB' or 'gender':
                unfold_col_value = row[self.col_indx_to_unfold]
                
                # Encountered thiS key (i.e. unfold-col value) before?
                # If not, init with empty array of that key's value for
                # the subject who is represented by this row.
                # We'll end up with this: {'DOB' : ['1983', '1980'], 'gender' : ['M','F']}:
                collected_values = self.unfolded_values_dict.get(unfold_col_value, [])
                
                # Value of this unfold-key in this row (e.g. '1983' or 'M'):
                unfold_value = row[self.col_indx_of_values]
                collected_values.append(unfold_value)
                self.unfolded_values_dict[unfold_col_value] = collected_values
                
                # Now take care of constant columns.
                # For each unique value of the column that
                # is being unfolded, constant columns must
                # be unique. Example to end up with:
                #
                #    question   questionType   answer1    answer2
                #    --------------------------------------------
                #      DOB       pullDown       1980       1983
                #     gender      radio          F          M
                #
                # Cannot have original table contain 'pullDown' for 
                # some DOB row, and 'radio' for another. This won't
                # work as an original:
                #     subject   question answer  questionType
                #    -----------------------------------------
                #    subject1    DOB      1980   pullDown
                #    subject1   gender     F      radio
                #    subject2    DOB      1983    radio
                #    subject2   gender     M      radio
                # 
    
                for col_num in range(len(row)):
                    try:
                        col_name = self.header[col_num]
                    except IndexError:
                        raise ValueError('Row %s has more columns than header (%s)' % (col_num, self.header))
                    col_value = row[col_num]
                    
                    # Is this column constant for a given pivot column value?
                    if col_name in self.constant_cols:
                        
                        # Dict: 
                        #    {(<unfold-col-value, constant_col_name) : constant_col_value}
                        # I.e. for each of the values in the column to be unfolded,
                        # each constant column has the same value, else something is wrong.
                        # Check whether we already encountered the value in the current
                        # row's unfold-value; if not init, if yes, ensure that this 
                        # constant-col's value in the current row is the same as in 
                        # other rows in which the unfold-value is the same as in this row:
                        
                        const_values_dict_key = (unfold_col_value,col_name)
                        col_constant = self.const_col_dict.get(const_values_dict_key, None)
                        
                        if col_constant is None:
                            self.const_col_dict[const_values_dict_key] = col_value
                        else:
                            # Saw value for this column and pivot value earlier:
                            if col_value != col_constant:
                                raise ValueError("Column that is supposedly constant for a given pivot value is not: %s != %s" %\
                                                 (col_value, col_constant))
                                
                    # Are we to use an existing column as source for
                    # names of new columns?
                    
                    if self.new_col_names_col is not None:
                        self.new_col_names.add(row[self.new_cols_col_indx])
                     
        finally:
            if type(in_path_or_2d_array) == str:
                in_fd.close()
                                    
        return(self.output_result())

    # ---------------------------------- Private Methods ---------------------

    
    #-------------------------
    # create_out_header_row
    #----------------- 
    
    def create_out_header_row(self, header):
        
        # Create CSV: col_name_to_unfold, constant_cols[0], constant_cols[1], ..., unfolded-values-columns
        # Find the longest row of unfolded values, so that we can pad
        # them with zeroes:
        unfolded_max_len = 0
        for unfolded_value in self.unfolded_values_dict.keys():
            num_unfolded_values = len(self.unfolded_values_dict[unfolded_value])
            unfolded_max_len = max(num_unfolded_values, unfolded_max_len) # Header: start with the column name that was unfolded:
        
        header = [self.col_name_to_unfold] 
        # Continue with any columns that were constant for
        # any given unfold-value:
        header.extend(self.constant_cols)
        # Finally: invent names for all the unfolded values
        # that are now columns; or the caller specified a
        # self.new_col_names_col, and we accumulated values
        # from that column-name-providing column in self.new_col_names
        if self.new_col_names_col is not None:
            for new_col_header in self.new_col_names:
                header.append(new_col_header)
        else:
            # Invent names for the new columns: v<n>:
            for indx in range(unfolded_max_len):
                header.append('%s%s' % (self.new_col_prefix, indx))
        
        return (header, unfolded_max_len)

    
    #-------------------------
    # process_in_header_line
    #----------------- 
    
    def process_in_header_line(self, reader):
        '''
        Given a csv- or excel reader that is pointed to
        table file, read the first row, which is expected
        to be the table header. Error-check, and return
        that header. 
        
        :param reader: object providing the file-like API
        :type reader: csv.Reader
        '''
    
        header = reader.next()
        
        # If we are to use the value of a column to name
        # new columns created for the unfolded values,
        # ensure the col exists:
        
        if self.new_col_names_col is not None:
            try:
                self.new_cols_col_indx = header.index(self.new_col_names_col)
            except IndexError:
                raise ValueError('Specified column %s as source of col names for unfolded columns, but no such column exists' % self.new_col_names_col)
        else:
            self.new_cols_col_indx = None
        try:
            # Does the column to be unfolded exist?
            # in the running example: 'question':
            self.col_indx_to_unfold = header.index(self.col_name_to_unfold)
        except IndexError:
            raise ValueError('The column to unfold (%s) does not appear in the table header (%s)' % (self.col_name_to_unfold, header))
        try:
            # Does the column with the unfold-values
            # exist? In the running example: 'answer':
            self.col_indx_of_values = header.index(self.col_name_unfold_values)
        except IndexError:
            raise ValueError('The column of unfold values (%s) does not appear in the table header (%s)' % (self.col_name_unfold_values, header))
        return header
        
    #-------------------------
    # output_result
    #----------------- 
        
    def output_result(self):
        # Do the writing-out, to STDOUT, a file, or
        # by building an internal 2d array of the result
        # and returning an iterator to it:
        try:
            # Will be None if iterator requested:
            (out_fd, writer) = self.make_writer(self.out_method)
            
            (header, unfolded_max_len) = self.create_out_header_row(self.header)
    
            if self.out_method == OutMethod.ITERATOR:
                result = [header]
            else:
                writer.writerow(header)
            # Each new row is about one of the unfolded values,
            # like 'DOB' or 'gender' in the example:
            for unfold_key in self.unfolded_values_dict.keys():
                new_row = [unfold_key]
                # Add constant-column values if any:
                for col_name in self.constant_cols:
                    # The constant-column value for the current
                    # rows value in the column being unfolded is
                    # kept in self.const_col_dict. Keys are tuples:
                    # (unfold_col_value, constant_col_name):
                    const_col_key = (unfold_key, col_name)
                    col_constant = self.const_col_dict[const_col_key]
                    new_row.append(col_constant)
                
                unfolded_values = self.unfolded_values_dict[unfold_key]
                # Fill short-row vectors with zeros:
                unfolded_values = unfolded_values + (unfolded_max_len - len(unfolded_values))*[0]
                new_row.extend(unfolded_values)
                if self.out_method == OutMethod.ITERATOR:
                    result.append(new_row)
                else:
                    writer.writerow(new_row)
        finally:
            if self.out_method == OutMethod.ITERATOR:
                return(iter(result))
            elif self.out_method != OutMethod.STDOUT:
                out_fd.close()

    # ---------------------------------- Support Methods ---------------------
                    
    #-------------------------
    # make_writer
    #----------------- 
            
    def make_writer(self, out_method):
    # Obtain a csv writer object if function is
    # not called as a generator:
        if out_method != OutMethod.ITERATOR and out_method != OutMethod.STDOUT:
            fd = open(out_method.FILE, 'w')
        elif out_method == OutMethod.STDOUT:
            fd = sys.stdout
        else:
            fd = writer = None
        if fd is not None:
            writer = csv.writer(fd)
        return (fd,writer)
    
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--constantCol',
                        action='append',
                        default=None,
                        help='Column(s) to keep; all others except the unfold\n'+\
                             'column will be discarded. Use as often as needed.')
    parser.add_argument('-n', '--newColNameCol',
                        action='store',
                        default=None,
                        help="Column that will supply names for new columns \n"+\
                             "(e.g. 'userId'); if not provided, the new cols \n"+\
                             "will be 'v1','v2',...")
    parser.add_argument('table_path',
                        help='Path to .csv file'
                        )
    parser.add_argument('col_to_unfold',
                        help="Name of column whose values are to be new columns")
    parser.add_argument('col_of_values',
                        help="Name of column whose values will be the values in the new columns.")
    
    args = parser.parse_args();
    
    shaper = TableShaper()
    shaper.unfold(args.table_path, 
                  args.col_to_unfold, 
                  args.col_of_values, 
                  out_method=OutMethod.STDOUT, 
                  constant_cols=args.constantCol, 
                  new_col_names_col=args.newColNameCol)

        