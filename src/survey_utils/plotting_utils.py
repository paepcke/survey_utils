'''
Created on May 26, 2016

@author: paepcke
'''

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

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
        