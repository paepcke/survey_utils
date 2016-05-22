# Unfolding Tables

Survey results often arrive with a row holding data from
one respondent. What is needed for many stats analyses is
one row for each question, where the responses to one row's
question occupy one column for each respondent.

The `unfold()` method of `TableShaper` provides this folding.
Input can either be a .csv file, or a 2D Python array. Outputs
may be:

* directed to a new .csv file
* written to stdout (the default)
* retrievable as from an iterator: `next()`

The unfold service may be invoked from Python code, or
from the command line.

In reshaping, some columns may be retained, others discarded.
Consider the following example:
 
    userId |  question |  questionType |  timeAdded |  answer 
    -------|-----------|---------------|------------|---------
     10    |  DOB      |    pullDown   |    Jun2010 |   1983     
     10    |  gender   |    radio      |    May2011 |     F
     20    |  DOB      |    pullDown   |    Jun2010 |   1980
     20    |  gender   |    radio      |    May2011 |     M
                      ...

Minimally we want this table to be:

    question | v1  |  v2   
    ---------|-----|-----       
      DOB    | 1983| 1980
    gender   |  F  |  M      

In this most minimal (but often sufficient) result, **questionType** and
**timeAdded** are dropped. Values of the **question**
column are distributed across new columns. Each **v_n**
column holds answers by one respondent to all questions.
Rows now hold information about one question, no longer about
a respondent.

Terminology:

* The *unfold column* is the column whose values
  will turn into columns.
* *Unfold values* are the values that are initially in
  the unfold column, and which will make up the new columns.
* *Constant columns* are columns that will remain columns in
  the final outcome.
* *Column-name provider* is a column whose values will be used
  as the names of the new columns. Often a respondent ID will
  be appropriate for this role. If no such column is provided,
  `unfold()` creates names.

Let the *unfold column* be **question**, and the *constants
columns* be **questionType** and **timeAdded**. You could call the
function like this:

'''
shaper = TableShaper()
shaper.unfold('/tmp/in.csv', 
       	      col_name_to_unfold='question'
       	      col_name_unfold_values='answer'
       	      constant_cols=['questionType','timeAdded'])

The reshaped table looks like this:
 
    question | questionType | timeAdded  | v1  |  v2   
    ---------|--------------|------------|-----|-----       
      DOB    |   pullDown   | June2010   | 1983| 1980
    gender   |    radio     |  May2011   |  F  |  M      
 

Note that in this example the *constant columns* are **questionType**
and **timeAdded**, and they are retained. It is an error to have
inconsistencies in the *constant columns*. For instance,
if the original row

 >"20  DOB   pullDown..."

had been
 >"20  DOB     radio"

an error would have been raised. All *constant columns*
field values for the same question (in different rows of the original)
must match. 

Another way to call the function controls the names of the new
columns. One column  can be specified to provide the column headers:
 
```

shaper.unfold('/tmp/in.csv',
       	      col_name_to_unfold='question'
       	      col_name_unfold_values='answer'
       	      constant_cols=['questionType','timeAdded'],
       	      new_col_names_col='userId)
```       
           
The reshaped table would look like this:
 
    question | questionType | timeAdded  |  10  |  20
    ---------| -------------|------------|------|-----
      DOB    |   pullDown   | June2010   | 1983 | 1980
    gender   |    radio     |  May2011   |   F  |   M 

I.e. the user id values are used as the column headers
of the new table.

To have the function behave like an iterator
(each item will be an array with one row of the
 reshaped table):
  
```
it = unfold('/tmp/in.csv',
           col_name_to_unfold='question'
           col_name_unfold_values='answer'
           constant_cols=['questionType','timeAdded'],
           out_method=OutMethod.ITERATOR)
for row in it:
    print(row)
```
        
To write the output to a file:

```
unfold('/tmp/in.csv',
       col_name_to_unfold='question'
       col_name_unfold_values='answer'
       constant_cols=['questionType','timeAdded'],
       new_col_names_col='userId,
       out_method=OutMethod('/tmp/trash.csv')
```
Finally, to use the unfold facility from the **command line**:

```
prompt> python src/survey_utils/unfolding.py --h
usage: unfolding.py [-h] [-c CONSTANTCOL] [-n NEWCOLNAMECOL]
                    table_path col_to_unfold col_of_values

positional arguments:
  table_path            Path to .csv file
  col_to_unfold         Name of column whose values are to be new columns
  col_of_values         Name of column whose values will be the values in the new columns.

optional arguments:
  -h, --help            show this help message and exit
  -c CONSTANTCOL, --constantCol CONSTANTCOL
                        Column(s) to keep; all others except the unfold
                        column will be discarded. Use as often as needed.
  -n NEWCOLNAMECOL, --newColNameCol NEWCOLNAMECOL
                        Column that will supply names for new columns 
                        (e.g. 'userId'); if not provided, the new cols 
                        will be 'v1','v2',...
```
