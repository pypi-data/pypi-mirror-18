# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:12:22 2015

@author: pkiefer
"""


import pylab
import matplotlib
import os
import numpy as np
from tempfile import gettempdir
from wtbox.table_operations import split_table_by_columns, add_plots_to_table

##################################################################################################
# BUILDING PLOTS FROM TABLE COLUMNS AND ADDING THEM TO TABLE

def plot_from_table_columns(t, id_cols, plot_fun, plot_fun_args2colnames, save_dir, 
                                    plot_colname='plot', kwargs=None):
    """ description of function arguments:
        - t: table
        - id_cols: tuple with columns to define sub_tables with plot values. Example: to
        plot isotopique pattern of different compounds and samples in the same table you can
        assign the plots correctly via the column name tuple (sample_name, compound_name).
        - plot_fun: function to create the plot. 
        - plot_fun_args2values: dictionary with plot function arguments as keys and tuple
        (colname, uniqueValue) as value {plotarg : (columnname, False)}, if uniqueValue
        is True and all only 1 value in column single value is extracted
        - save_dir: direction where to save figure files 
        - kwargs: plot function dependendent plotting parameter arguments e.g. dpi, plot type_, 
        colors, styles, ....
    """
    id2plots=dict()
    for item in split_table_by_columns(t, id_cols, False):
        id_=item.splitter.uniqueValue()
        args2values=extract_plot_values(item, plot_fun_args2colnames)
        
        args2values['plot_title']=_make_plot_title(item, id_cols)
        if not args2values.has_key('sample_name'):
            args2values['sample_name']=item.source.uniqueValue()[-10:] # not more than 10 characters 
        save_path=build_save_path(item, plot_colname, id_cols, save_dir, kwargs['plot_format'])
        plot_fun(args2values, plot_colname, save_path, kwargs)
        id2plots[id_]=save_path
        save_and_close_figure(save_path, kwargs)
    t.dropColumns('splitter')
    add_plots_to_table(t, id2plots, id_cols=id_cols, plot_colname=plot_colname)


def _make_plot_title(item, id_cols):
    id_=item.splitter.uniqueValue()
    title=None
    for name, value in zip(id_cols, id_):
        if not title:
            title= '_'.join([name, str(value)])
        else:
            title='_'.join([title, name, str(value)])
    return title[:20] #max 20 characters
        
    

def extract_plot_values(t, plotargs2colnames):
    p2v=dict()
    expr=t.getColumn
    for key in plotargs2colnames.keys():
        colname, unique_value=plotargs2colnames[key]
        v= expr(colname).uniqueValue() if unique_value else expr(colname).values
        p2v[key]=v
    return p2v

def build_save_path(t, plot_colname, id_cols, save_dir, fig_type):
    prefix='_'.join(id_cols)
    postfix='_'.join([str(v) for v in t.splitter.uniqueValue()])
    title='_'.join([plot_colname, prefix, postfix])
    assert os.path.isdir(save_dir), 'selected path %s is not a directory' %save_dir
    return os.path.join(save_dir , '.'.join([title, fig_type]))


def save_and_close_figure(path, kwargs):
    pylab.savefig(path, dpi=kwargs['dpi'], facecolor=kwargs['figure_facecolor'])
    pylab.close()



###################################################################################################
def plot_heatmap(data, xlabels, ylabels, label_right=False, colorbar= True, pad_colorbar=0.1, 
                 binsize=None, title=None, save_dir=None, cmap="Greens", none_color="#777777",
                 fig_type='png', dpi=None):
    """
    plots heatmap including axis labels, colorbar and title

    paramters:
      data        :  2d numpy array
      xlabels     :  list of strings, len is number of colums in data
      ylabels     :  list of strings, len is number of rows in data
      label_right :  boolean, indicates if labels at right of heatmap should be plotted
      colorbar    :  show colorbar, default = True
      pad_colorbar:  float in range 0 .. 1, distance of colorbar to heatmap
      binsize     :  None or float in range 0..1, if this value is not None the heat map and
                     the colorbar are discretised according to this value.
      title       :  None or string
      cmap        :  string with name of colormap, see help(pylab.colormaps) for alternatives
      none_color  :  rgb string for plotting missing values.
    """
    target=None
    n_rows, n_cols = data.shape
    print 'heatmap_ dimension:', n_rows, n_cols
    assert len(xlabels) == n_cols
    assert len(ylabels) == n_rows
    data = np.ma.masked_where(np.isnan(data), data)
    cmap = pylab.cm.get_cmap(cmap)
    cmap.set_bad(none_color)
    if binsize is not None:
        bounds = np.arange(-0.1, 1.001, binsize)
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    else:
        norm = None
    labelright="on" if label_right else "off"
    print labelright
    im = pylab.imshow(data, interpolation='none', cmap=cmap, norm=norm, aspect="auto")
    pylab.tick_params(axis="both", 
                      left="off", bottom="off", top="off", right="off",
                      labelbottom="on", labeltop="off", labelleft="on",
                      labelright=labelright)
    if colorbar:                      
        pylab.colorbar(im, pad=pad_colorbar, shrink=0.9)
    axes = im.get_axes()
    axes.set_xticks(range(n_cols))
    axes.set_xticklabels(xlabels, fontsize='small', rotation=90)
    axes.set_yticks(range(n_rows))
    axes.set_yticklabels(ylabels, fontsize='small')
    im.set_axes(axes)
    if save_dir is None:
        save_dir=gettempdir()
    assert os.path.isdir(save_dir), 'selected path %s is not a directory' %save_dir
    target=os.path.join(save_dir , '.'.join([title, fig_type]))
    pylab.savefig(target, dpi=dpi)
    pylab.close()
    
    return target


def _plot_heatmap_from_feature_table(feature, value_col='mi_frac', columns_col='time', 
                                rows_col='mi', add_missing_values=0.0, cmap='binary',
                                title='test', save_dir=None):
    t=feature
    complete=set(t.getColumn(rows_col).values)
    if all([isinstance(v, float) for v in t.getColumn(value_col)]):
            
        rows=[]
    #    id_cols.append(value_col)
        t.sortBy(columns_col)
        name=average_multiple_values(t, rows_col, columns_col, value_col)
        for column in split_table_by_columns(t, [columns_col]):
    #        rows.append(_get_row(row, complete, order_col, value_col, add_missing_values))
            missing =complete-set(column.getColumn(rows_col))    
            missing=[(mi, add_missing_values) for mi in missing]
            tuples=list(set(zip(column.getColumn(rows_col), column.getColumn(name))))
            tuples.extend(missing)
            tuples.sort(key=lambda v: v[0])
            rows.append(np.array([v[1] for v in tuples]))
            
        data=np.array(rows)
#        return data
        data=np.transpose(data)
        x_labels=list(set(feature.getColumn(columns_col).values))
        x_labels.sort()
        if 'time' in columns_col and all([isinstance(v, float) for v in x_labels]):
            x_labels=[_convert_time_label(v) for v in x_labels]
        else:
            print "Warning: x_labels were not regognized as time values!"
        y_labels=[''.join(['M', str(i)]) for i in sorted(list(complete))]
        t.dropColumns(name)
        return plot_heatmap(data, x_labels, y_labels, save_dir=save_dir, title=title, cmap=cmap)


def average_multiple_values(t, rows_col, columns_col, value_col):
    expr=t.getColumn
    name='_'.join([value_col,  'mean'])
    t.addColumn('id_', zip(expr(rows_col),  expr(columns_col)), type_=tuple)
    t.updateColumn(name, expr(value_col).mean.group_by(t.id_), type_=float)
    t.dropColumns('id_')
    return name

    
def _convert_time_label(time_point):
    units=['s', 'm', 'h']
    conversion=[1.0, 60.0, 3600.0] # sec , min, h
    end=time_point
    if not end:
        which=0
    else:
        which=len([end/v for v in conversion if end/v>=1])-1 # units where step >1
    norm=conversion[which]
    def norm2str(v, norm=norm):
        return str(round(v/norm,1))
    return ' '.join([norm2str(time_point), units[which]])
    
    
def plot_heatmaps_from_isotope_table(t, id_col='feature_id', columns_col='time', 
                                rows_col='mi', value_col='mi_frac_corr', add_missing_values=0.0, 
                                 cmap='binary', save_dir=None):    
    """
    Plots heatmap plot from table columns using function plot_heatmap and returns a dictionary
    containing id_col as key and correspondong plot_path as value. To add plots to table see
    -> wtbox.table_operations.add_plots_to_table
    o	id_col: defines the subtable for each heatmap
    o	columns_col: x-axis of heatmat plot
    o	rows_col: y-axis of heatmap plot
    o	value_col: value assigned to (x,y) 
    o	add_missing_values: replaces None values by user defined value
    o	cmap : string with name of colormap, see help(pylab.colormaps) for alternatives
    o	save_dir: saving direction of heatmap plots

    """
    params={'columns_col':columns_col, 'rows_col':rows_col, 'value_col':value_col,
            'add_missing_values':add_missing_values, 'cmap':cmap, 'save_dir': save_dir}
    
    id2plot_path=dict()
    for item in split_table_by_columns(t, (id_col,)):
        id_=item.getColumn(id_col).uniqueValue()
        title='_'.join(['heatmap', id_col, str(id_)])
        params['title']=title
        plot_path=_plot_heatmap_from_feature_table(item, **params)
        if plot_path:
            id2plot_path[(id_,)] =  plot_path# tuple needed
            # since add plots also works plot_fitting_curve_from_table where more than 1 id col is 
            # needed sometimes, e.g. to fit isotopologues
    return  id2plot_path         
   
    
##################################################################################################
# Main User Functions

def plot_fitting_curve(x, y, x_fit, y_fit, x_tick_labels='', y_tick_labels='', x_ticks=None, 
                       unit='', y_ticks=None, ylabel=None, title=None, outlier_values=[(None,None)]):
    """ Default scatter plot of measured values x, y combined with line line plot of fitted values 
        of fitted values x_fit, y_fit. Optional attributes:
        o	x_tick_labels: list of string (in general numbers), labeling x-ticks
        o	y_tick_labels: list of string (in general numbers), labeling y-ticks
        o	x_ticks: list of float values, positioning x ticks
        o	y_ticks: list of float values, positioning y ticks
        o	y_label : name of x axis
        o	title: plot title
        o	outlier_value: list of (x, y) tuples that allows depicting outlier values in different 
           color separately.

    """
    pylab.plot(x_fit, y_fit, 'r', linewidth=3)
    pylab.xlabel("time " +unit, fontsize=18)
    if not ylabel:
        pylab.ylabel("labeled C", fontsize=18)
    else:
        pylab.ylabel(ylabel, fontsize=18)
    if title:
        pylab.title(title)
    pylab.plot(x, y, "bo", markersize=9)
    _add_outliers(outlier_values)     
    axes=pylab.gca()
    # to suppress label
    #axes.set_xticks([])
    if x_ticks:
        axes.set_xticks(x_ticks)
    else:
        axes.set_xticks(range(len(x_tick_labels)))
    axes.set_xticklabels(x_tick_labels, fontsize='large')
    if  y_ticks:
        axes.set_yticks(y_ticks)
    else:
        axes.set_yticks(range(len(y_tick_labels)))
    axes.set_yticklabels(y_tick_labels, fontsize='large')
    axes.set_axes([axes])


def _get_fitting_curve_axes_layout(xs,ys):
    tmax=max(xs)
    values=list(smart_time_axis(tmax))
    ymin, ymax = (min(ys), max(ys) ) 
    values.extend(list(smart_y_axis(ymin, ymax)))
    keys=['x_tick_labels', 'x_ticks', 'unit', 'y_tick_labels', 'y_ticks']
    return {keys[i]: values[i] for i in range(len(keys))}
  
  
def plot_fitting_curves_from_table(t, id_cols=('feature_id',), time_col='time', 
                            value_col='no_C13', fun_col='no_C13_fitting_fun',
                            params_col='no_C13_fit_params', add_missing_tp_as_zero=True,
                            outlier_col=None, num_points=50, 
                             save_dir=r'P:\tmp', fig_type='png', dpi=None):
        """ Plots fitting curve of (isotope) table t. Arguments names are chosen to simplify 
            plotting of DLI isotopologue curves, but any  x,y fitting can be plotted. Function 
            returns a dictionary containing id_col as key and correspondong plot_path as value. 
            To add plots to table see -> wtbox.table_operations.add_plots_to_table. Function
            attributes:
        o	id_cols: Tuple defining subtable for fitting plot. It allows combining different columns 
            to define subgroup. Example: To plot all isotpologues of a feature you can combine 
            the two columns as identifier by id_cols=(‘feature_id’, ‘mi’)
        o	time_col: Defines column with x- values (time)
        o	value_col: defines y values for plot
        o	fun_col: Fitting function that was applied
        o	params_col: parameters determined with fitting function to calculate y_fit
        o	add,_missing_tp_ as_zero: None values will be shown as zero
        o	outlier_col: a column can be provided that contains (x,y) pairs which have been 
           excluded from fitting process. 
        o	num_points: Number of points calculated with fitting_function to draw line plot
        """
        id2plot_path=dict()
        for item in split_table_by_columns(t, id_cols, False): # column splitter needed for dic
            # determine ploting axis labels
            x=item.getColumn(time_col).values
            y=item.getColumn(value_col).values
            x,y=_get_unique_x_y(x,y)
            x_fit, y_fit=_get_x_fit_y_fit(item, time_col, params_col, fun_col, num_points)
            if not x_fit==None and not y_fit==None:
                plot_params=_get_fitting_curve_axes_layout(x,y)
                plot_params['ylabel']=value_col
                plot_params['title']=_build_title(item, id_cols)
                if outlier_col:
                    plot_params['outlier_values']=_get_outliers(item, time_col, outlier_col)
                plot_fitting_curve(x, y, x_fit, y_fit, **plot_params)
                if save_dir is None:
                    save_dir=gettempdir()
                prefix='_'.join(id_cols)
                postfix='_'.join([str(v) for v in item.splitter.uniqueValue()])
                title='_'.join(['fit_curve', prefix, postfix])
                assert os.path.isdir(save_dir), 'selected path %s is not a directory' %save_dir
                target=os.path.join(save_dir , '.'.join([title, fig_type]))
                pylab.savefig(target, dpi=dpi)
                pylab.close()
                id_=item.splitter.uniqueValue()
                id2plot_path[id_]=target
        t.dropColumns('splitter')
        return id2plot_path
        

def _get_outliers(t, time_col, colname):
    # fixes t.colname.uniqueValue() problem when column colname contains tuples
    if t.getColType(colname)==tuple:
        values=set(t.getColumn(colname).values)
        return list(values)


def _add_outliers(pairs):
    pairs=[p for p in pairs if all([v!=None for v in p])]
    xs=[p[0] for p in pairs]
    ys=[p[1] for p in pairs]
    pylab.plot(xs, ys,'ro', markerfacecolor='r')



def _build_title(item, id_cols):
    fields=[]
    for col in id_cols:
        fields.append('='.join([col, str(item.getColumn(col).uniqueValue())]))
    return '_'.join(fields)
    
def _get_unique_x_y(x,y):
    pair =zip(x,y)
    pair=list(set(pair))
    pair.sort(key=lambda v: v[0])
    return [v[0] for v  in pair], [v[1] for v  in pair] 
    
    
def _get_x_fit_y_fit(t, time_col, params_col, fun_col, num_points):
    try:
        fun=t.getColumn(fun_col).uniqueValue()[0]
        x=t.getColumn(time_col).values
        x_fit=np.linspace(min(x), max(x), num_points)
        params=get_fun_params(t, params_col)
        return x_fit, np.array([fun(v, *params) for v in x_fit] )
    except:
        return None, None
#####################################################################################

def smart_time_axis(tmax, stepsize=5.0):
    step=np.ceil(float(tmax)/stepsize) 
    units=['[s]', '[min]', '[h]']
    conversion=[1, 60, 3600] # sec , min, h
    which=len([step/v for v in conversion if step/v>=1])-1 # units where step >1
    norm=conversion[which]
    x_tick_labels=[str(round(v/norm,1)) for v in np.arange(0,tmax+1, step)]
    x_ticks=[float(v) for v in np.arange(0,tmax+1, step)]
    return x_tick_labels, x_ticks, units[which]                          



def smart_y_axis(ymin, ymax, stepsize=5.0, max_digits=3):
    int_char=max(len(str(int(ymin))), len(str(int(ymax))))
    digits=max_digits-int_char
    if digits>0:
        y_ticks=[np.round(v, digits) for v in np.linspace(np.floor(ymin), np.ceil(ymax), stepsize)]    
        y_tick_labels=[str(v) for v in y_ticks]
    else:
        y_ticks=[np.round(v, 0) for v in np.linspace(np.floor(ymin), np.ceil(ymax), stepsize)]            
        y_tick_labels=['{:.1e}'.format(v) for v in y_ticks]
    return y_tick_labels, y_ticks
    
    
def get_fun_params(t, params_col):
    params=t.getColumn(params_col).values
    len_params=len(params[0])
    for i  in range(len_params):
        assert len(set([p[i] for p in params]))==1, 'more than one fit function for time series. '\
                         'Please check please parameter id_cols!'
    return params[0]
    
    
    
    