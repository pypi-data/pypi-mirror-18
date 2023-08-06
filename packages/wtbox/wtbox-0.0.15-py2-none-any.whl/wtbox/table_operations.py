# -*- coding: utf-8 -*-
"""
Created on Tue May 12 12:11:19 2015

@author: pkiefer
"""

import emzed
from emzed.core.data_types import PeakMap, Table, Blob
import difflib
import checks_and_settings as checks
import numpy as np

##################################################################################################

def split_table_by_columns(t, colnames, remove_split_id=True):
    """ allows splitting split id composed by seve_ral columns defined in iterable 
        colnames. this avoids nested appyling of splitBy
        example code:
            t=t=emzed.utils.toTable('id1', (0,0,0,1,1,1), type_=int)
            t.addColumn('id2', range(3) *2, type_=int)
            t.addColumn('a', range(6), type_=int)
        results:
            
            id1      id2      a       
            int      int      int     
            ------   ------   ------  
            0        0        0       
            0        1        1       
            0        2        2       
            1        0        3       
            1        1        4       
            1        2        5       

       split_table_by_columns(t, ['id1', 'id2']) results 6 tables :
           
           id1      id2      a       
           int      int      int     
           ------   ------   ------  
           0        0        0       
           
           id1      id2      a       
           int      int      int     
           ------   ------   ------  
           0        1        1       
           
           id1      id2      a       
           int      int      int     
           ------   ------   ------  
           0        2        2       

           id1      id2      a       
           int      int      int     
           ------   ------   ------  
           1        0        3       

           id1      id2      a       
           int      int      int     
           ------   ------   ------  
           1        1        4       
          
           id1      id2      a       
           int      int      int     
           ------   ------   ------  
           1        2        5       
       
       and equals:
           subsets=[]
           for subset1 in t.splitBy('id1'):
               subsets.extend(subset1.splitBy('id2'))
    """
    assert isinstance(t, Table), 't is not an emzed table!'
    missing=set(colnames)- set([n for n in t.getColNames()])
    assert t.hasColumns(*colnames), 'columns %s are missing' %', '.join(missing)
    id_cols=[t.getColumn(col).values for col in colnames]
    tuples=zip(*id_cols)
    t.addColumn('splitter', tuples, type_=tuple)
    tables=t.splitBy('splitter')
    if  remove_split_id:
        t.dropColumns('splitter')
        [sub.dropColumns('splitter') for sub in tables]
    return tables
    
############################################################################


def update_column_by_dict(t, col, key_col, dict_, type_=None):
    """ Function update_column_by_dict(t, col, ref_col, dict_, type_=None) updates column `col` 
        by ditionary where keys are in column key_col.
    """
    t=t.copy()
    if t.hasColumn(col):        
        _type=t.getColType(col)
        t.replaceColumn(col, (t.getColumn(key_col).apply(dict_.get)).ifNotNoneElse(t.getColumn(col)),
                        type_=_type)
    else:
        if not type_:
            type_=_get_type_from_dict(dict_)
        if type_:
            t.addColumn(col, t.getColumn(key_col).apply(dict_.get), type_=type_)
        else:
            t.addColumn(col, t.getColumn(key_col).apply(dict_.get), type_=object)
    return t

def _get_type_from_dict(dict_):
     types=list(set([type(v) for v in dict_.values()]))
     if len(types)==1:
         return types.pop()
    
################################################################################################         
     
def table_to_dict(t, as_json=False):
    """ converts table into dictionary ('colname', values). An additional key layout 
        contains information about column types and formats. If as_json is True, Peakmaps, 
        Blobs and Subtables are lost during conversion! 
    """
    assert isinstance(t, Table), 'item must be Table'
    excluded = [PeakMap, Blob, Table]
    if as_json:
        colnames=[name for name in  t.getColNames() if not t.getColType(name) in excluded]
        remove=[name for name in  t.getColNames() if t.getColType(name) in excluded]
        if len(remove):
            print 'columns %s will be lost while conversion to dictionary! If you want to keep those'\
                    'columns keep the original table!' %' ,'.join(remove)
    else:
        colnames=[name for name in  t.getColNames()]
    coltypes=[str(t.getColType(name)) for name in colnames]
    colformats=[t.getColFormat(name) for name in colnames]
    layout=zip(colnames, coltypes, colformats)
    table_dict=dict()
    print coltypes
    for i, name in enumerate(colnames):
            table_dict[name]=t.getColumn(name).values
    table_dict['layout']=layout
    return table_dict
    
    
def dict_to_table(dic):
    """ Inverse function of table_to_dict. converts dictionary into table with colnames dict.keys() 
        and column values must be lists, tuples of the same length or unique values. Additionaly, 
        a key layout is required containing a list of tuples 
        (column name, column type_, column format). 
    """
    assert isinstance(dic, dict), 'item must be dictionary'
    assert dic.has_key('layout'), 'dictionary is not a table dictionary'
    colnames=[v[0] for v in dic['layout']]
    assert set(dic.keys())-set(colnames)==set(['layout']), 'colnames are missing'
    types=[v[1] for v in dic['layout']]
    formats=[v[2] for v in dic['layout']]
    t=emzed.utils.toTable(str(colnames[0]), dic[colnames[0]], type_=_convert_str_to_type(types[0]),
                          format_=formats[0])
    for i,name in enumerate(colnames):
        if i: 
            type_ =   _convert_str_to_type(types[i])
            values=dic[name]
            t.addColumn(name, values, type_=type_, format_=formats[i])
    return t


def _convert_str_to_type(str_type):
    objects=[1, '1', 1.0, (1,), []]
    dic={str(type(o)): type(o) for o in objects }
    dic["<class 'emzed.core.data_types.ms_types.PeakMap'>"]=PeakMap
    return dic[str_type]
    

def transfer_column_between_tables(t_source, t_sink, data_col, ref_col, insert_before=None):
    """ Function (t_source, t_sink, data_col, ref_col)adds values from column data_col from Table 
        `t_source` to Table `t_sink` via common reference and returns a t_sink. 
    column `ref_col`. If column `data_col` exists already in t_sink an assertion occurs.
    
    """
    #    checks
    
    assert isinstance(t_source, Table), 't_source is not of Type table'
    assert isinstance(t_sink, Table), 't_sink is not of Type table'
    missing=set([data_col, ref_col])-set([n for n in t_source.getColNames()])
    assert len(missing)==0, 'column(s) %s are missing in Table %s' %(missing, t_source)
    assert t_sink.hasColumns(ref_col), 'column %s is missing in Table %s' %(ref_col, t_sink)
    assert t_sink.hasColumns(data_col)==False, 'column %s exists already in Table %s' \
                                                %(data_col, t_sink)
    t_sink=t_sink.copy()
    type_=t_source.getColType(data_col)
    format_=t_source.getColFormat(data_col)
    pairs=set(zip(t_source.getColumn(ref_col).values, t_source.getColumn(data_col).values))
    ref2data={v[0]:v[1] for v in pairs}
    def _add(v, dic=ref2data):
        return dic.get(v)
    t_sink.addColumn(data_col, t_sink.getColumn(ref_col).apply(_add), type_=type_, format_=format_, 
                     insertBefore=insert_before )
    
    return t_sink
#################################################################################################


def cleanup_table_join(t, remove_redundance=True):
    """ postfixes of unique columns of joint table t are removed. If remove redundance =
     True, all columns with postfixes having same values as corresponding column without postfix
     are removed
    """
    t=t.copy()
    postfixes=t.findPostfixes()
    postfixes.remove("")
    with_pstfx=[]
    colnames = [name for name in t.getColNames()]
    for fix in postfixes:
        names=[name.split(fix)[0] for name in t.getColNames() if name.endswith(fix)]
        with_pstfx.extend(names)
    if remove_redundance:
        unique=set(with_pstfx).difference(set(colnames))
        for colname in unique:
            for fix in postfixes:
                if t.hasColumn(colname+fix):
                    t.renameColumns(**{colname+fix:colname})
    return t


##############################################################################################
def peakmap_as_table(pm):
    """ converts peakmap pm into table format
    """
    assert isinstance(pm, PeakMap), 'item must be of type PeakMap!'
    t=emzed.utils.toTable('peakmap', [pm])
    t.addColumn('unique_id', pm.uniqueId())
    t.addColumn('full_source', pm.meta['full_source'])
    t.addColumn('source', pm.meta['source'])
    return t

#################################################################################################

def _extract_subpeakmap(id_, pm, rtmin, rtmax, mzmin, mzmax):
    pm.uniqueId()
    new=pm.extract(rtmin=rtmin, rtmax=rtmax, mzmin=mzmin, mzmax=mzmax)
    try:
        del new.meta['unique_id'] #bug fix
    except:
        pass # problem fixed in latest version
    new.uniqueId()
    return id_,  new
    
def _build_id_2pm(tuples):
    id_2pm=dict()
    for values in tuples:
        key,value=_extract_subpeakmap(*values)
        id_2pm[key]=value
    return id_2pm
        
def replace_peakmaps(t, ref_col, tuples, mslevel):
    postfix=_get_postfix(t, ['peakmap'])
    id_2pm=_build_id_2pm(tuples)
    def fun_(v, dic=id_2pm, mslevel=mslevel):
        pm=dic.get(v)
        pm.spectra=[spec for spec in pm.spectra if spec.msLevel==mslevel]
        return pm
    t.replaceColumn('peakmap'+postfix, t.getColumn(ref_col).apply(fun_), type_=PeakMap)
            

def reduce_peakmap_size_in_table(peaks_table, ref_col='id', 
                                 tol=(-60.0, +60.0, -10.0, +10.0), mslevel=1):
    """ function  reduces data size for e.g. targeted data analysis. Peakmaps are cut 
    to fit targeted extraction window defined by argument ref_col. Argument tol is a tuple with 
    values (lower rttol, upper rttol, lower mztol, upper mztol) and defines tolerance 
    for peakmap cutting.
    """
    t=peaks_table.copy()
    number=len(set(t.getColumn(ref_col).values))
    print 'reducing peakmap size to individual extraction window sizes for %d compounds' %number  
    required=['rtmin', 'rtmax', 'mzmin', 'mzmax']   
    checks.colname_type_checker(t, required)
    assert t.hasColumns(ref_col)
    tuples=_get_large_rt_mz_windows(t, ref_col, tol)
    replace_peakmaps(t, ref_col, tuples, mslevel)
    print 'Done.'
    return t

def _get_large_rt_mz_windows(t, ref_col, tol):
    window_cols=['rtmin', 'rtmax', 'mzmin', 'mzmax']
    pstfx=_get_postfix(t, window_cols)
#    window_cols=[''.join([n, pstfx]) for n in window_cols]
    pairs=zip(window_cols, tol)
    for name,add in pairs:
        if 'min' in name:
            t.addColumn('_'+name, t.getColumn(name+pstfx).min.group_by(t.getColumn(ref_col))+add, 
                        type_=float)
        else:
            t.addColumn('_'+name, t.getColumn(name+pstfx).max.group_by(t.getColumn(ref_col))+add, 
                        type_=float)
    values=set(zip(t.getColumn(ref_col).values, t.getColumn('peakmap'+pstfx).values, 
                   t._rtmin.values, t._rtmax.values, t._mzmin.values, t._mzmax.values))
    _drop_columns(t, window_cols)  
    return values

def _drop_columns(t, names):
    names=[''.join(['_', n]) for n in names]
    t.dropColumns(*names)


def _get_postfix(t, colnames):
    pstfxs=t.supportedPostfixes(colnames)
    assert len(pstfxs)==1, 'peakmap cutting is only possible if window per peak is defined'        
    return pstfxs[0]



#################################################################################################


def single_spec_to_table(prec, spec):
    """ Single_spec_to_table(prec, spec) converts ms2 spectrum into table. Suitable for to 
        visualize MS spectra from top_n or similar approaches.
    """
    from copy import deepcopy
    spec.msLevel=1
    spec1=deepcopy(spec)
    spec1.rt+=0.05
    pm=PeakMap([spec, spec1])
    t=emzed.utils.toTable('precursor', [prec])
    t.addColumn('mzmin', pm.mzRange()[0], type_=float, format_='%.5f')
    t.addColumn('mzmax', pm.mzRange()[1], type_=float, format_='%.5f')
    t.addColumn('rtmin', pm.rtRange()[0]-1.0, type_=float, format_='"%.2fm" %(o/60)')
    t.addColumn('rtmax', pm.rtRange()[1]+1.0, type_=float, format_='"%.2fm" %(o/60)')
    t.addColumn('peakmap', pm)
#    pm1=t.peakmap.uniqueValue()
#    t.replaceColumn('peakmap', pm1)
    return emzed.utils.integrate(t, 'max')

###################################################################################################
def add_plots_to_table(t, id2plots, id_cols, plot_colname='plot'):
    """
    developped to handle plots from funs ``plot_heatmaps_from_isotope_table`` and 
    ``plot_fitting_curves_from_table``. Both functions return a dictionary containing path 
    for each fitting id 
    dictionary id2plot keys: id_col values, values: plot_pathes
    """
    t=t.copy()
    assert type(id_cols) in [list, tuple], 'id_cols must be an iterable and not %s' %type(id_cols)
    assert isinstance(id2plots, dict)
    _id_cols=[t.getColumn(col).values for col in id_cols]
    tuples=zip(*_id_cols)
    try:
        t.addColumn('_id', tuples, type_=tuple)
        def get_plot(id_, dic=id2plots):
            path=dic.get(id_)
            return emzed.io.loadBlob(path) if path else None
                
        t.updateColumn(plot_colname, t._id.apply(get_plot), type_=Blob)
    except:
        print 'check input'
    t.dropColumns('_id')
    return t


##################################################################################################

def find_common_postfix(t, colnames=None):
    """ Function find_common_postfix(t, colnames=None) finds any common postfix for all colnames 
        of table t. Argument `colnames` is a list of strings, and if set common postfix of 
        selected colnames is returned if listed colnames are all columns of t else, 
        an empty string is returned.
    """
    if not colnames:
        colnames=[n  for n in t.getColNames()]
    if  t.hasColumns(*colnames):
        ref=colnames[0]
        matches=[]
        for name in colnames[1:]:
            s=difflib.SequenceMatcher(None, ref, name)
            match=s.find_longest_match(0, len(ref), 0, len(name))
            pstfx=ref[match.a:match.a+match.size]
            matches.append((pstfx, len(pstfx)))
        return min(matches, key=lambda v: v[1])[0]
    return ''
    
##################################################################################################


def update_rt_by_integration(t, mslevel=1):
    """update_rt_by_integration(t) returns new column with updated rt value. 
    Required columns rtmin, rtmax, mzmin, mzmax, peakmap
    """
    checks.is_integratable_table(t)
    t=t.copy()
    t.updateColumn('index', range(len(t)), type_=int)
    tt=emzed.utils.integrate(t, 'max', msLevel=mslevel)
    for pstfx in tt.supportedPostfixes(['rtmin', 'rtmax']):
        tt.updateColumn('rt'+pstfx, tt.apply(_det_rt,(tt.getColumn('params'+pstfx),)), type_=float)
    if t.hasColumn('rt' + pstfx):
        t.dropColumns('rt'+pstfx)
    t=transfer_column_between_tables(tt, t, 'rt', 'index', insert_before='rtmin')
    t.dropColumns('index')
    return t        
        
 
def _det_rt(params):
    rts, ints=params
    idx=np.where(max(ints)== ints)[0][0]
    return rts[idx]   