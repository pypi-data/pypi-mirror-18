# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:15:06 2015

@author: pkiefer
"""
import emzed
import wtbox.checks_and_settings as _checks
from emzed.core.data_types import PeakMap
from collections import defaultdict
from mf_utils import count_element as _count_element
import _iso_corr
import numpy as np

##################################################################################################
# PEAKS NORMALIZATION

def calculate_mid(t, id_col='feature_id', quantity_col='area', result_col='mi_fraction'):
    """ function calculate_mid(t, id_col='feature_id', quantity_col='area', result_col='mi_fraction')
        determines the mass isotopologue distribution of feature with id id_col and writes 
        the result in column result_col. By default the quantity col is area.  
    """
    return normalize_peaks(t, denominator_col=id_col, norm_peaks_id= id_col, 
                           quantity_col=quantity_col, result_col=result_col)



def normalize_peaks_by_idms(t, id_col='feature_id', mi_col='mi', quantity_col='area', 
                            result_col='idms_ratio'):
    """ normalize_peaks_by_idms(t, id_col='feature_id', mi_col='mi', quantity_col='area', 
        result_col='idms_ratio') calulates ratio of unlabeled (minimal labeled) and fully labeled 
        mass istopologues of each feature. Attributes:
        - id_col: groupes mass isotopoloques of a compound adduct ion
        - mi_col: nominal isotopoloque mass shift
        - quantity_col: peak area (intensity)
        - result_col: name of the result column
    """
    t=t.copy()
    expr=t.getColumn
    t.updateColumn('normalize_with', 
      (expr(mi_col).min.group_by(expr(id_col))==expr(mi_col)).thenElse(expr(id_col), None), type_=int)
    t.updateColumn('id_idms', 
      (expr(mi_col).max.group_by(expr(id_col))==expr(mi_col)).thenElse(expr(id_col), None), type_=int)
    print t 
    t=normalize_peaks(t, denominator_col='normalize_with', norm_peaks_id='id_idms',  
                    quantity_col=quantity_col, result_col=result_col)
    t.dropColumns( 'id_idms', 'normalize_with')
    expr=t.getColumn
    # remove None values from result_column
    t.replaceColumn(result_col, expr(result_col).max.group_by(expr(id_col)))
    return t
                           
def normalize_peaks_with_internal_standards(t, norm_id_col='norm_with',
                is_id_col='internal_standard', quantity_col='area', result_col='norm_area'):
    """
    Function normalize_peaks_with_internal_standards(t, norm_id_col='norm_with',
    is_id_col='internal_standard', quantity_col='area', result_col='norm_area') normalizes peak
    area (intensities) to user defined internal standard area. Attributes:
    - norm_id_col: contains id of internal standard used for normalization
    - is_id_col: defines peak as internal standard and assigns id to the peak. 
    - quantity_col: peak area (intensity)
    - result_col: name of the result column
    """
    t=normalize_peaks(t,   denominator_col=norm_id_col, norm_peaks_id=is_id_col, 
                           quantity_col=quantity_col, result_col=result_col) 
    return t

def normalize_peaks_with_TIC(t, quantity_col='area', result_col='norm_area'):
    """ 
       normalize_peaks_with_TIC(t, quantity_col='area', result_col='norm_area') normalizes peak 
       area of each peak to total table area. Attributes:
       - quantity_col: peak area (intensity)
       - result_col: name of the result column
    """
    t=t.copy()
    t.addColumn('tic_peak', 0, type_=int)
    t=normalize_peaks(t,   denominator_col='tic_peak', norm_peaks_id='tic_peak', 
                           quantity_col=quantity_col, result_col=result_col) 
    t.dropColumns('tic_peak')                          
    return t


#############################################
# MAIN FUNCTION
def normalize_peaks(t,  denominator_col='normalize_with', norm_peaks_id= 'norm_peaks_id',  
                    quantity_col='area', result_col='normalized_peak'):
    """ 
    adds column `normalized peak` to table t where each peak's quantity specified 
    in quantity_col is normalized by their normalizing  peak(s)  specified in column 'norm_col'. 
    Normalizing peaks are indexed in dominator_col. If more than 1 peak has the same id
    normalizing area is sum of peak areas with same index.  if denominator_col equals None 
    peaks are   not normalized.
    examples:
        (1) MID
        fid ¦ norm_peaks_id ¦ area ¦ normalize_with¦
        -------------------------------------------
        0   ¦       0       ¦   1e5¦ 0
        0   ¦       0       ¦   4e5¦ 0
        0   ¦       0       ¦   3e4¦ 0
        -> fid can be used as dominator_col and nomr_peaks_id_col at the same time
        
        
        (2) IDMS        
        fid ¦mi ¦ norm_peak_id  ¦ area ¦ normalize_with¦
        -------------------------------------------------
         1  ¦ 0 ¦ None          ¦  1e5 ¦ 1
         1  ¦ 6 ¦ 1             ¦  8e4 ¦ None
         
        -> 
        
        (3) Normalization to any internal standard
        
         ¦ norm_peak_id ¦ area ¦ normalize_with¦
         ----------------------------------
         ¦ None         ¦   1e5¦ 1
         ¦ None         ¦   8e4¦ 1
         ¦    1         ¦   8e4¦ None        


        (4) individual
        ¦ peak_id ¦ area ¦ normalize_with¦
        ----------------------------------
        ¦ 0       ¦   1e5¦ 2
        ¦ 1       ¦   4e5¦ 1 
        ¦ 2       ¦   3e4¦ None
        
    """
    t=t.copy()
    _check_postfixes_for_normalization(t, [denominator_col, norm_peaks_id, quantity_col])
    for required in [{denominator_col:int, norm_peaks_id:int}, {quantity_col:float}]: 
            _checks.colname_type_checker(t, required.keys(), required)
    expr=t.getColumn
    for pstfx in t.supportedPostfixes([quantity_col]):
        def has_pstfx(name, postfix=pstfx, t=t):
            return  name+postfix if t.hasColumn(name+postfix) else name
        check=all([isinstance(v, int) or v==None for v  in\
                    t.getColumn(has_pstfx(norm_peaks_id)).values])
        assert check, 'norm_col must be integer or None !'
        idcol2norm=_build_norm_id2norm_dict(t, has_pstfx(norm_peaks_id), quantity_col+pstfx)
        def fun(v, dict_=idcol2norm):
            return dict_.get(v )
        
        t.addColumn('norm_quan', expr(has_pstfx(denominator_col)).apply(fun), type_=float)        
        t.addColumn('temp', (t.norm_quan.isNotNone()).thenElse\
        (expr(quantity_col+pstfx)/t.norm_quan, None), type_=float, format_='%2.2e')
        t.dropColumns('norm_quan')
        if t.hasColumn(result_col+pstfx):
            t.replaceColumn(result_col+pstfx, t.temp, type_=float, format_='%2.2e')
            print 'WARNING: column `%s` already exists. Values will be replaced!' %result_col+pstfx
            t.dropColumns('temp')     
        else:
            t.renameColumn('temp', result_col+pstfx)
    return t    
    
def _build_norm_id2norm_dict(t, norm_id_col, quantity_col):
    expr=t.getColumn
    triples=zip( expr(norm_id_col).values, expr(quantity_col).values)  
    sum_dict=defaultdict(int)
    for norm, quan in triples:
        if isinstance(norm, int) and isinstance(quan,  float):
#            print quan, norm
            sum_dict[norm]+=quan
    return sum_dict


def _check_postfixes_for_normalization(t, colnames):
    """
    """
    denominator_col, norm_peaks_id, quantity_col=colnames
    expr=t.supportedPostfixes
    both =set(expr([denominator_col, norm_peaks_id]))
    assert len(set(expr(denominator_col))-both)==0 & len(set(expr(norm_peaks_id))-both)==0, '%s'\
    'and %s need the same postfixes!'
  

###################################################################################################
def correct_for_natural_C13(t, id_='feature_id',  isotope_id='mi', 
                            fraction_col='mi_fraction', mf_col='mf'):
    """ function correct_for_natural_C13(t, id_='feature_id',  isotope_id='mi', 
    fraction_col='isotope_fraction', mf_col='mf') subtracts carbon labeling originating from 
    natural 13C abundance from calculated mass isotopologue distribution and writes result in 
    column fraction_col with postfix ‘_corr’. The function is best suited for high mass 
    resolution data since it takes not into account heavy stable isotopes of other elements. 
    Attributes:
        o	         id_col: groupes mass isotopoloques of a compound adduct ion
        o	         isotope_id: nominal isotopoloque mass shift
        o	         fraction_col: column with mass calculated mass isotopologue distribution
        o	          mf_col: column with corresponding molecular formula
            
    """
    _checks.is_isotopologue_distribution_table(t, id_, isotope_id, fraction_col)
    _checks.colname_type_checker(t, [mf_col], {mf_col: str})
    postfixes=t.supportedPostfixes([isotope_id, fraction_col, mf_col])
    for pstfx in postfixes:
        _update_num_c(t, mf_col+pstfx)    
        features=t.splitBy(id_+pstfx)
        [correct_mi_frac(f, id_, isotope_id, fraction_col, pstfx, '_num_c') for f in features]
    result=emzed.utils.mergeTables(features)
    result.dropColumns('_num_c')
    return result
        

def _update_num_c(t, mf_col='mf'):
    def fun(v, el='C'):
        return _count_element(el, v)
    t.updateColumn('_num_c', t.getColumn(mf_col).apply(fun), type_=str)


def correct_mi_frac(t, fid, isotope_id, fraction_col, pstfx, num_c='num_c'):
    i_id=isotope_id+pstfx
    f_col=fraction_col+pstfx
    
    #NONE HANDLING:
    if all([v>=0 for v  in t.getColumn(f_col).values]):
        def fun(v):
            return 0 if v is None else v
        assert t.hasColumn(i_id), 'No of estimated C atoms in ion is missing'
        if t.hasColumn(num_c):
            n=t.getColumn(num_c).apply(fun, filter_nones=False).uniqueNotNone()
            if n and n<=170: #170 = limit für anzahl der C atome !!
                frac=np.zeros((n+1))
                for i in range(len(t)):
                    try:
                        j=t.getColumn(i_id).values[i]
                    except:
                        emzed.gui.inspect(t)
#                        print 'j, i', j, i
                    try:
                        frac[j]=t.getColumn(f_col).values[i]
                    except:
                        pass
                frac,_=_iso_corr.compute_distribution_of_labeling(frac, n)
                mi=t.getColumn(i_id).values
                value=[frac[i] for i in mi]
            else:
                value=None
            t.updateColumn(fraction_col+'_corr'+pstfx, value, format_='%2.2e', type_=float)
    else:
        print 'correction was not possible for feature %s' %t.getColumn(fid+pstfx).uniqueValue()
        t.updateColumn(fraction_col+'_corr'+pstfx, None, format_='%2.2e', type_=float)


  
##################################################################################################
def calculate_feature_labeled_fraction(t, id_col= 'feature_id', mi_col='mi' ,
                            mi_fraction_col='mi_fraction_corr', result_col='labeled_fraction'):
    """ calculate_feature_labeled_fraction(t, id_col, mi_col , mi_fraction_col) calculates labeled
       isotope fraction fromm mass isotopologue distribution
    """
    t=t.copy()
    required={mi_col:int, mi_fraction_col:float}
    _checks.colname_type_checker(t, required.keys(), required)
    expr=t.getColumn
    for pstfx in t.supportedPostfixes(required.keys()):
        n=result_col+pstfx
        t.updateColumn(n, 
                    expr(mi_col+pstfx)*expr(mi_fraction_col+pstfx), type_=float, format_='%.3f')
        t.replaceColumn(n, 
                expr(n).sum.group_by(expr(id_col))/expr(mi_col+pstfx).max.group_by(expr(id_col)),
                        type_=float)
    return t
    
    

###############################################################################################

def filter_top_n_by_fragment_ion(top_n_table, ions, mztol=0.005, min_int=1e3):
    """ filters a top_n table for specific fragment ions see ->feature_extraction.top_n_to_table.
        Attributes:
        - ions: list of fragment ion m/z values
        - mztol: m/z tolerance in units
        - min_int: minimsl peak intensity
        
    """
    t=top_n_table.copy()
    assert t.hasColumn('ms2_specs')
    specs=t.ms2_specs.values
    ions=[_check_for_ions(spec.peakmap.uniqueValue(), ions, mztol, min_int) for spec in specs]
    t.addColumn('fragment_ions', ions, type_=tuple)
    def fun(v):
        return len(v)>0
    t.addColumn('_select', t.fragment_ions.apply(fun))
    t=t.filter(t._select==True)
    t.dropColumns('_select')
    return t

def _check_for_ions(pm, ions, mztol=0.005, min_int=10000):
    assert isinstance(pm, PeakMap) and len(pm)==1
    spec=pm.spectra[0]
    return _spec_has_ions(spec, ions, mztol=mztol, min_int=min_int)
    
        
def _spec_has_ions(spec, ions, mztol=0.005, min_int=10000):
    spec=[(mz, int_) for mz, int_ in spec if int_> min_int]
    mzs=[mz for mz, __ in spec]
    found=[]
    for ion in ions:
        cand=[mz for mz  in mzs if abs(mz-ion)<=mztol]
        if len(cand):
            found.append(ion)
    return tuple(found)



