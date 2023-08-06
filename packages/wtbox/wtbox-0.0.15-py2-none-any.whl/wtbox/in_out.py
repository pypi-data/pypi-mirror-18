# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:38:40 2015

@author: pkiefer
"""

import emzed
import json
import os
import re
import cPickle
import tempfile
import shutil
#from copy import deepcopy
from emzed.core.data_types import Table#, PeakMap
import pandas
import table_operations as _top

###############################################################################################
# (1) save and load dictionaries in json format

def save_dict(dic, path=None, overwrite=False, startAt=None):
    """ Saves dictionary `dic`  in path `path`. All keys are converted into strings.
        If no path is provided argument startAt allows assigning an initial 
        directory for the path dialog.
    """
    if not path:
        path=emzed.gui.askForSave(caption='save dictionary (.json)', extensions=['json'], 
                                  startAt=startAt)
    if os.path.isdir(path):
        path=emzed.gui.askForSave(caption='save dictionary (.json)', extensions=['json'], 
                                  startAt=path)
    path=check_and_modify_save_path(path, type_='json')
    print 'saving path: ', path
    if  os.path.exists(path) and not overwrite:
        assert False, '% s already exists. Please choose different name. '\
                    'To overwrite existing file choose overwrite=True'
    with open (path, 'w') as fp:
        json.dump(dic, fp, indent=4, encoding='latin-1')
    fp.close()


def load_dict(path=None, startAt=None):
    """loads dictionary saved in .json format if path exists, else default dialog is opened and
        argument startAt allows assigning an initial directory for the path dialog."""

    if path and _check_file_path(path, ['json']):
        pass
    else:
        path=emzed.gui.askForSingleFile(extensions=['json'], caption='load dictionary (.json)',
                                        startAt=startAt)
    if path:
        with open(path, "r") as fp:
            return  _convert(json.load(fp))



def _convert(input, encode='latin-1'):
    """ converts strings in unicode into encode format default=latin-1
    """
    if isinstance(input, dict):
        return {_convert(key): _convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [_convert(element) for element in input]
    elif isinstance(input, unicode):
        try: 
            return input.encode(encode)
        except:
            return input
    else:
        return input

##################################################################################################
# (2)  load multiple emzed Tables and PeakMaps
def load_tables(pathes=[], startAt=None, exclude_blanks=False):
    """ load_tables(pathes=[], startAt=None, filter_blanks=False) loads multiple emzed tables of
        of type table, CSV and json from a list of pathes(for details about tables in json see 
        table_operations.table_to_dict). If pathes is empty a dialog opens and argument startAt 
        allows assigning an initial directory for the path dialog.  If exclude_blanks is 
        True only files not labeled with 'blank' in file name are loaded. For details see 
        filter_blanks function.
    """
    assert all([os.path.isfile(p) for p in pathes]), 'check pathes'
    if not len(pathes):
        pathes=emzed.gui.askForMultipleFiles(caption='load tables', 
                                             startAt=startAt, extensions=['table', 'csv'])
    if exclude_blanks:
       pathes=filter_blanks(pathes) 
    return [load_table_item(p) for p in pathes]

def load_peakmaps(pathes=[], startAt=None, exclude_blanks=False):
    """ load_peakmaps(pathes=[], startAt=None, filter_blanks=False) loads multiple peakmaps of
        of type mzML and mzXML from a list of pathes(for details about tables in json see 
        table_operations.table_to_dict). If pathes is empty a dialog opens and argument startAt 
        allows assigning an initial directory for the path dialog.  If exclude_blanks is 
        True only files not labeled with 'blank' in file name are loaded. For details see 
        filter_blanks function.
    """
    assert all([os.path.isfile(p) for p in pathes]), 'check pathes'
    if not len(pathes):
        pathes=emzed.gui.askForMultipleFiles(caption='load peakmaps', 
                                             startAt=startAt, extensions=['mzML', 'mzXML'])
    if exclude_blanks:
       pathes=filter_blanks(pathes) 
    return [emzed.io.loadPeakMap(p) for p in pathes]


def load_table_item(path=None, startAt=None):
    """ determines data type from ending. Can load tables saved as json, table, and csv, 
    assertion if file type  does not fit. Output is a Table. If path is not specified a dialog 
    box opens and argument startAt allows assigning an initial directory for the path dialog.
    """
    print path
    if not path:
        path=emzed.gui.askForSingleFile(startAt=startAt, extensions=['table', 'csv', 'json'], 
                                        caption='load tables from table, csv or json')
        
    assert os.path.isfile(path), 'path %s is not a file' %path
    allowed=['json', 'table', 'csv']
    
    _, ending=os.path.basename(path).split('.')
    assert ending in allowed, '%s is not an accepted file format (%s)'%(ending, allowed)
    if ending == 'table':
        return emzed.io.loadTable(path)
    elif ending == 'csv':
        return emzed.io.loadCSV(path)
    else:
        dic= load_dict(path)
        return _top.dict_to_table(dic) 


def filter_blanks(pathes):
    """ filters a list of pathes if the file name contains the word blank seperated by space, -, _
        or if placed at the end of the file name the word blank is followed by `.`. Examples
        _blank_, -BlaNK.mzML
    """
    assert isinstance(pathes, list), 'FILENAMES ARE NOT IN A LIST'
    assert all([isinstance(n, str) for n in pathes]), 'List of filenames contains'\
                                                        ' at least 1 non-string object'
    def fun(v):
        pattern1='[-_\s][Bb][Ll][Aa][Nn][Kk][-_.\s]'                                                
        pattern2='[Bb][Ll][Aa][Nn][Kk][-_.\s]'                                                
        check1=len(re.findall(pattern1, v))
        check2=re.match(pattern2, v) # filename starts with blank
        if not check1 and not check2:
            return True
    return [n for n in pathes if fun(n)]  

#############################################################################################
# 

def enhanced_save_table(t, path=None, force_overwrite=True, startAt=None, type_='table'):
    """
    function enhanced_save_table automatically adds time label to 
    filename if force_overwrite is set to `False` and path exists. Allowed filename characters
    are restricted and unaccepted strings will open a dialog to allow the user filename correction. 
    filename type is automatically set to `table`. If no path is provided argument startAt allows 
    assigning an initial directory for the path dialog.
    """
    assert isinstance(t, Table), '%s is not of type Table' %path
    if not path:
        path=emzed.gui.askForSave(extensions=[type_], startAt=startAt)
    path=check_and_modify_save_path(path, type_)
    if not force_overwrite:
        path=add_time_label_if_path_exists(path)    
    else:
        if os.path.exists(path):
            print 'EXISTING  TABLE WILL BE OVERWRITEN!'
    emzed.io.storeTable(t, path=path, forceOverwrite=force_overwrite)
    return path

#def test_(a=5):
#    import inspect
#    frame=inspect.currentframe()
#    print inspect.getargvalues(frame)

    
def save_list_of_tables(tables, path=None, force_overwrite=True, startAt=None):
    """  save_list_of_tables(tables, path=None, force_overwrite=True, startAt=None) merges a list
    of tables applying emzed stackTables function, merged table will be saved as '.tables'. 
    """
    # add_table_id:
    assert all([isinstance(t,emzed.core.data_types.Table) for t in tables]), 'saving item must '\
            'be a list of emzed Table objects'
    ms=range(len(tables))
    tables_=[]
    for t, m in zip(tables, ms):
        if len(tables):
            t.addColumn('table_id', m, type_=int, format_='%d')
        else:
            t=t.copy()
            t.rows=[[None] * len(t.getColNames())]
            t.addColumn('table_id', -m, type_=int, format_='%d')
        tables_.append(t)    
    try:
        merged=emzed.utils.stackTables(tables_)       
    except:
        assert False, 'column names, types and formats must be the same for all tables!'
    merged.meta['is_list']=True
    [t.dropColumns('table_id') for t in tables]
    return enhanced_save_table(merged, path=path, force_overwrite=force_overwrite, startAt=startAt,
                               type_='tables')


def load_list_of_tables(path=None, startAt=None):
    """load_list_of_tables(path=None, startAt=None) ) loads merged list of tables of type '.tables' 
    which was saved with function -> save_list_of_tables and splits it into origin list of tables. 
    """
    if not path:
        path=emzed.gui.askForSingleFile(extensions=['tables'], startAt=startAt, 
                                   caption='load list of tables')
    t=emzed.io.loadTable(path)
    
    if t.meta.has_key('is_list'):
        tables=[]
        for t  in t.splitBy('table_id'):
            if t.table_id.uniqueValue()<0:
                t=t.emptyClone()
            t.dropColumns('table_id')
            tables.append(t)
        return tables
    else:
        print 'WARNING: Table was not saved with `merge_and_save_tables`. table will not '\
        'be splitted!'
        return t
        
##################################################################################################
def save_tables_as_excel(tables, path=None, force_overwrite=True, startAt=None):
    """ Function save_tables_as_excel(tables, path=None, force_overwrite=True, startAt=None)
        Saves a list of tables in excel file where each table is written to a separate sheet. 
        Excel sheet names are set to t.title  if t.title exists. Else sheet names are enumerated. 
        If path is None a dialog opens and argument startAt allows assigning an initial directory 
        for the path dialog. The function automatically adds time label to  filename 
        if force_overwrite is set to `False` and path exists. Only Columns of types 
        str, float, int, tuple, list, set, dict will be saved. COLUMNS WITH OTHER FORMATS WILL 
        BE LOST !!!!
    """
    if not path:
        path=emzed.gui.askForSave(extensions=['xlsx'], startAt=startAt, 
                                  caption='save list of tables as excel file')
    if not force_overwrite:
        path=add_time_label_if_path_exists(path)                                  
    writer=pandas.ExcelWriter(path, engine='xlsxwriter')
    titles=[t.title for t  in tables]
    for i, t in enumerate(tables):
        assert isinstance(t, Table), 'value is of Type %s. Iterable must only contain emzed'\
                                    ' Tables!' %type(t)
        t=_restrict_table_to_allowed_types(t)
        sheet_name=_build_sheet_name(t, i+1, titles)
        p=t.to_pandas()
        p.to_excel(writer, sheet_name)
    writer.save()
    return path


def _restrict_table_to_allowed_types(t):
    t=t.copy()
    allowed_types=(str, float, int, tuple, list, set, dict)
    colnames=[p[0] for p in zip(t.getColNames(), t.getColTypes()) if p[1]not in allowed_types]
    t.dropColumns(*colnames)
    return t

def _build_sheet_name(t, num, titles):
    unique=len(titles)==len(set(titles))
    title=t.title if t.title and unique else str(num)
    # remove invalid sheet name characters:
    for char in '[]:/\*?':
        title=title.replace(char, '_')
    return '_'.join(['table', title])
    
##################################################################################################

def save_table_as_json(t, path=None, force_overwrite=True, startAt=None):
    """ save_table_as_json(t, path=None, force_overwrite=True, startAt=None) saves table object as 
    json. Since columns 
    """
    d=_top.table_to_dict(t, True)
    save_dict(d, path=path, overwrite=force_overwrite, startAt=startAt)
    
    
###########################################################
#   save and load any pickled python object 

def save_item_as_pickle(value, path=None, overwrite=True, startAt=None):
    """ save_item_as_pickle(value, path=None, overwrite=True, startAt=None) saves any 
    python object as pickle. It automatically adds time label to filename if force_overwrite is 
    set to `False` and the file exists. Allowed file name characters are restricted and unaccepted 
    strings will open a dialog to allow the user file name correction. File name type is 
    automatically set to `pickled`. If no path is provided argument startAt allows assigning 
    an initial directory for the path GUI dialog.
    """
    if not path:
        path=emzed.gui.askForSave(extensions=['pickled'], startAt=startAt)
    path=check_and_modify_save_path(path, 'pickled')
    if not overwrite:
        path=add_time_label_if_path_exists(path)
    # create tempfile for faster saving:
    dirname, filename=os.path.split(path)
    temp=tempfile.mkdtemp()
    temp_path=os.path.join(temp, filename)
    # save pickled file locally
    with open(temp_path, 'wb') as fp:
        cPickle.dump(value, fp)
    # move pickled file to destination
    if os.path.exists(path):
       os.remove(path)         
    shutil.move(temp_path, dirname)
    os.removedirs(temp)


def load_pickled_item(path=None, startAt=None):
    """ loads pickled python objects. If no path is provided 
        argument startAt allows assigning an initial directory when starting the GUI dialog.
    """
    if path and _check_file_path(path, ['pickled']):
        pass
    else:
        path=emzed.gui.askForSingleFile(extensions=['pickled'], caption='load pickeld item (.json)',
                                        startAt=startAt)
    with  open(path, 'rb') as fp:
        return cPickle.load(fp)
        
################################################################################################
# HELPERS

def add_time_label_if_path_exists(path):
    """
    function save_as_if_path_exists(path) automatically adds time label to 
    filename if path exists
    """
    if os.path.exists(path):
       directory, name=os.path.split(path)
       name,ending=name.split('.')        
       name='_'.join([name,time_label()])
       name='.'.join([name, ending])
       return os.path.join(directory, name) 
    return path

####    
def check_and_modify_save_path(path, type_='table'):
    directory, name=os.path.split(path)
    name=_check_filename_and_type(name, type_)
    return os.path.join(directory, name)


def _check_filename_and_type(filename, type_='table'):
    fields=filename.split('.')
    # case 1: no type_ ending:
    assert len(fields)>0, 'filename is missing'
    if len(fields)==1:
        name, =fields
        ending=type_
    elif len(fields)==2:
        name, ending=fields
    else:
        name='.'.join(fields[:-1])
        ending=fields[-1]
    name=_check_filename(name)
    if ending!=type_:
             print 'WARNING! Ending is of filename %s is of type %s.'\
            '\n the filename will be modified to %s.' %(name, ending, type_)  
    return '.'.join([name, type_]) 


def _check_filename(name):
    # forbidden characters
    forbidden='[*;,:.\/^~@#$£!¨]'
    not_allowed=re.findall(forbidden, name)
    # name must not start with digit
    pattern='([A-Za-z_][A-Za-z0-9_-]+)'
    matchs=re.match(pattern, name) 
    while not matchs or not_allowed:
        emzed.gui.showWarning('Filenames must not start with digits and'\
             'should only contain characters A-Z, a-z, 0-9, _,-'\
        ' Please modify your filename!')
        name=emzed.gui.DialogBuilder('modify file name')\
        .addString('file name', default=name)\
        .show()
        matchs=re.match(pattern, name)
        not_allowed=re.findall(forbidden, name)
    return name


def _check_file_path(path, types):
    allowed=', '.join(types)
    if os.path.isfile(path):
        name, ending=path.split('.')
        if ending not in types:
             print 'WARNING! Ending is of filename %s is of type %s and not of any allowed type:'\
                     '%s.' %(name, ending, allowed)  
        else:
            return True
    
           
        
        
###########################################################################################

def time_label():
    """ gives string of current time back. Used to label filenames
    """
    import time
    x=time.localtime()
    year=str(x.tm_year)
    month=_add_zero(str(x.tm_mon))
    day=_add_zero(str(x.tm_mday))
    hour=_add_zero(str(x.tm_hour))
    mins=_add_zero(str(x.tm_min))
    secs=_add_zero(str(x.tm_sec))
    label=year+month+day+"_"+hour+"h"\
           + mins+"m"+secs+"s"
    return label
    
    
def _add_zero(item):
    if len(item)==1:
        return '0'+ item
    return item