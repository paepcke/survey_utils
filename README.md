#### Installation

```
python setup install
python setup test
```

**Note:** The setup.py file contains a choice for installing
  particular modules, but not others. Currently there are just two
  choices that can be mixed and matched:

 * Only install `unfolding`. This facility will reshape
   tables. Installation is fast and sparse.
 * Only, or also install `math_utils`. This facility provides for
   replacing missing values by the mean or median of their row or
   column, some plotting utilities, and more. Including this module in
   the install will install scipy, a substantial package.

   When installing math_utils in **MacOS** you may get an error
   message: *error: library dfftpack has Fortran sources but no
   Fortran compiler found.* If this happens, you need first to:

   `brew install gcc`

   The gcc package contains a Fortran compiler.


#### Unfolding Tables

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
####Replacing Missing Values

Given either a numpy ndarray, or a Pandas DataFrame, you can replace
missing values. Options are to replace missing values with the:

 * mean of the value's row,
 * mean of the value's column,
 * median of the value's row,
 * median of the value's column,

In addition, you can specify what is considered a missing
value. Options are:

 * numpy.nan
 * numpy.inf
 * numpy.posinf
 * numpy.neginf
 * any other Python value.

Example: given `numpy.ndarray self.arr`:

  A | B | C | D
 ---|---|---|---
 1  |2  |3  |13
 4  |0  |6  |14
 4  |8  |9  |15
 10 |11 |12 |16


Can use:
```
res = replaceMissingValsNparray(self.arr, 
                                direction='column',
                                replacement='median',
                                missing_value=0)
```
to get:

  A | B | C | D
 ---|---|---|---
 1  |2  |3  |13
 4  |8  |6  |14
 4  |8  |9  |15
 10 |11 |12 |16

Notice that the zero in `arr[1,1]` was replaced
by the median of the column in which the zero
resided: MEDIAN(2,8,11). The zero itself is disregarded
for the median computation.

Instead of setting `replacement` to 'median', it can
be specified as 'mean,' resulting in:

  A | B | C | D
 ---|---|---|---
 1  |2  |3  |13
 4  |7  |6  |14
 4  |8  |9  |15
 10 |11 |12 |16

The `direction` parameter can be set to 'row', in
which case the mean/median are taken across, instead
of top to bottom.

In addtion to `replaceMissingValsNparray()`, which works
on numpy.ndarray structures, a corresponding
`replaceMissingValsDataFrame()` function works on Panda
`DataFrame`s.

####Dendrograms

Function `fancy_dendrogram()` displays hierarchical clusters
in visual form. The function is from ![a dendrogram tutorial](https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/)
with some additional documentation in the code header.

Here is how to use the facility.
```
def test_fancy_dendrogram(self):
    '''
    Generates a dendrogram in a new window.
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
```
	
![Example dendrogram](http://infolab.stanford.edu/~paepcke/shared-documents/dendrogram.png "Example dendrogram")
