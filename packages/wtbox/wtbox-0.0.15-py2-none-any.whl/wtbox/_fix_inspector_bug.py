# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 17:25:38 2016

@author: pkiefer
"""
from copy import deepcopy
from emzed.core.data_types import PeakMap
import emzed

def fix_ms2_inspect_integration_bug(table):
    Table=emzed.core.data_types.Table
    is_list=True
    if isinstance(table, Table):
        table=[table]
        is_list=False
    for t in table:
        postfixes=t.supportedPostfixes(['peakmap'])
        assert len(postfixes), 'column peakmap is missing or wrong column name!'
        for pstfx in postfixes:
            if not t.hasColumn('mslevel'+pstfx):
                t.addColumn('mslevel'+pstfx, t.apply(_addlevel,(t.getColumn('peakmap'+pstfx),)), 
                            type_=int)
                t.addColumn('temp'+pstfx, None, type_=type(None))
            t.replaceColumn('peakmap'+pstfx, 
                t.apply(modify_peakmap,(t.getColumn('peakmap'+pstfx), t.getColumn('mslevel'+pstfx))), 
                type_=PeakMap)
    emzed.gui.inspect(table)
    for t in table:
#        prefix=_get_pm_colname_prefix(t)
        for pstfx in t.supportedPostfixes(['peakmap']):
            t.replaceColumn('peakmap'+pstfx, 
                t.apply(modify_peakmap,(t.getColumn('peakmap'+pstfx), 
                t.getColumn('mslevel'+pstfx))), type_=PeakMap)
            if t.hasColumn('temp'+pstfx):
                t.dropColumns('temp'+pstfx, 'mslevel'+pstfx)
    if not is_list:
        table=table[0]


def _addlevel(pm):
    if isinstance(pm, PeakMap):
        if len(pm.getMsLevels())>1:
            print 'Warning: more than 1 mslevel in peakmap %s. mslevel is set to 1!' %pm.meta['source']
            return 1
        return pm.getMsLevels()[0]


def modify_peakmap(pm, level=None):
#    import pdb; pdb.set_trace()
    if pm is not None:
#        assert len(pm.getMsLevels())==1
        if level==2 and 2 in pm.getMsLevels():
            pm_ = deepcopy(pm)
            for spec in pm_.spectra:
                spec.msLevel=1
            return pm_
        elif level==2 and 1 in pm.getMsLevels():
            pm_ = deepcopy(pm)
            for spec in pm_.spectra:
                spec.msLevel=2
            return pm_
        return pm
    

#def _get_pm_colname_prefix(t):
#    PeakMap=emzed.core.data_types.PeakMap
#    colnames=[p[0] for  p in  zip(t.getColNames(), t.getColTypes()) if p[-1] == PeakMap]
#    assert len(colnames), 'peakmap is missing in table %s!' %t.title
#    return _get_prefix(colnames)
#    
#
#def _get_prefix(names):
#    length=[len(n) for n in names]
#    pos=length.index(min(length))
#    # shortest string must be prefix
#    prefix=names[pos]
#    assert all([re.match(prefix, n).string==n for n in names])
#    return prefix
#    
#    
#
#    