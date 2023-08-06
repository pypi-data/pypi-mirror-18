# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:21:06 2015

@author: pkiefer
"""

from emzed.core.data_types import PeakMap, Table
from emzed.utils import formula

##########################################################
# Cheking table types

def is_ff_metabo_table(t):
    
    """verifies whether table column names and column types correspond
    to featureFinderMetabo output table
    
    """
    assert isinstance(t, Table), "item must  be Table"
    
    required=['id', 'feature_id', 'mz', 'mzmin', 'mzmax', 'rt', 'rtmin',
                  'rtmax', 'intensity', 'quality', 'fwhm', 'z', 'peakmap',
                  'source']
    t.hasColumns(*required)
    if len(set(t.getColNames())-set(required)):
        print 'WARNING: TABLE %s HAS ADDITIONAL COLUMNS!' %t.source.uniqueValue()
    colname_type_checker(t, required)
    check_ranges(t, t.supportedPostfixes(required))


def is_integratable_table(t):
    assert isinstance(t, Table), "t must be Table expression"
    required=['rtmin', 'rtmax', 'mzmin', 'mzmax', 'peakmap']
    colname_type_checker(t, required)
    check_ranges(t, t.supportedPostfixes(required))



def is_integrated_table(t):
    required=['rtmin', 'rtmax', 'mzmin', 'mzmax', 'peakmap', 'area', 'method', 'rmse']
    colname_type_checker(t, required)
    check_ranges(t, t.supportedPostfixes(required))


def is_ms_peaks_table(t):
    assert isinstance(t, Table), 'object is not of type emzed table!'
    required=['mzmin', 'mzmax', 'rtmin', 'rtmax']
    colname_type_checker(t, required)
    print t.supportedPostfixes(required)
    check_ranges(t, t.supportedPostfixes(required))


def is_isotopologue_distribution_table(t, fid='feature_id', isotope_id='mi', 
                                       fraction_col='isotope_fraction'):
    try:
         name2types={fid:int, isotope_id:int, fraction_col:float}
         colname_type_checker(t, name2types.keys(), name2types=name2types)
    except:
        for name2types in [{fid:int}, {isotope_id:int, fraction_col:float}]:
            colname_type_checker(t, name2types.keys(), name2types=name2types)
     


def is_prm_peaks_table(t, id_col='fragment_id'):
    assert isinstance(t, Table), 'object is not of type emzed table!'
    is_ms_peaks_table(t)
    for postfix in t.supportedPostfixes([id_col]):
        name2types={'precursor_ion'+postfix: float, id_col+postfix: int}
        colname_type_checker(t, name2types.keys(), name2types=name2types)




def colname_type_checker(t, colnames, name2types=None):
    """
    checks whether column names [colnames] of  table [t] are of type required.  
    Optional [name2types -> dictionary {name : type}]. If None,
    colnames of standard dictionary colname_type_settings (e.g. mz, rt) are checked.  
    """
    if not name2types:
        name2types=colname_type_settings()
#    print 'colnames:', colnames
    postfixes=t.supportedPostfixes(colnames)
    assert len(postfixes)>0, 'column postfixes are not consistent: %s or colunms are missing!' \
                'required: %s \n existing %s '\
                % (', '.join(postfixes), ', '.join(colnames), ', '.join(t.getColNames()))
    for postfix in postfixes:
        for colname in colnames:
            assert t.hasColumn(colname+postfix)==True,'Column %s is missing' %colname+postfix
            # fix peakmap can be of type object in older tables 
            if colname=='peakmap':
                if t.getColType(colname+postfix)==object:
                    
                    pms=list(set(t.getColumn(colname+postfix).values))
                    for pm in pms:
                        assert isinstance(pm, PeakMap), 'Object(s) in column %s is not '\
                        'of type Peakmap' %colname+postfix
                    t.setColType(colname+postfix, PeakMap)
            if colname.startswith('mf'): # all molecular_formulas 
                assert all([_is_mf(v) for v in t.getColumn(colname+postfix).values]), ''\
                        'the mf columns does not only contain molecular formulas.'\
                        'Please check values:\n%s' %',\n'.join(t.getColumn('mf'+postfix).values)
            is_col_type=t.getColType(colname+postfix).__name__
            exp_col_type=name2types.get(colname).__name__
            assert is_col_type == exp_col_type or exp_col_type==None, 'Column %s is of '\
            'type %s and not of type %s' %(colname, is_col_type, exp_col_type )


def colname_type_settings():
    """
    """
    name_type={'mz': float, 'mzmin': float, 'mzmax': float, 
               'rt': float, 'rtmin': float, 'rtmax': float,
               'fwhm': float, 'quality': float, 'intensity': float, 
               'area': float, 'rmse': float, 'feature_id': int,
               'id': int, 'm0': int, 'params': object, 'z': int,
               'source': str, 'method': str, 'peakmap': PeakMap, 'mf':str}
    return name_type


def check_ranges(t, postfixes):
    for postfix in postfixes:
        mz_pairs=zip(t.getColumn('mzmin'+postfix).values, t.getColumn('mzmax'+postfix).values)
        rt_pairs=zip(t.getColumn('rtmin'+postfix).values, t.getColumn('rtmax'+postfix).values)
        assert _compare(mz_pairs), '0 <= mzmin < mzmax is not fullfilled for all peaks: %s'%mz_pairs 
        assert _compare(rt_pairs), '0 <= rtmin < rtmax is not fullfilled for all peaks!'


def _compare(pairs):
    return all([(0<=p[0]<=p[1]) for p in pairs])    


def _find_postfixes(t, colnames):
    return t.supportedPostfixes(colnames)
     
    
####################################################################
# check other types

def _is_mf(v):
    try:
        formula(v)
        return True
    except:
        return False


def is_peakmap(pm):
    assert isinstance(pm, PeakMap), 'Function requires PeakMap.'\
                                    'You provided an object of type %s' %type(pm)  


                                    
#######################################################################################
#
# DEFAULT SETTINGS
#
#######################################################################################

def default_ffmetabo_config():
    default=dict(common_noise_threshold_int=1000.0,
                common_chrom_peak_snr=3.0,
                common_chrom_fwhm=5.0,
                mtd_mass_error_ppm=15.0,
                mtd_reestimate_mt_sd='true',
                mtd_trace_termination_criterion='outlier',
                mtd_trace_termination_outliers=5,                
                mtd_min_sample_rate=0.5,                
                mtd_min_trace_length=3.0,
                mtd_max_trace_length=350.0,
                epdet_width_filtering='auto',
                epdet_min_fwhm=3.0,
                epdet_max_fwhm=60.0,
                epdet_masstrace_snr_filtering='true',
                ffm_local_rt_range=10.0,
                ffm_local_mz_range=10.0,
                ffm_charge_lower_bound=0, 
                ffm_charge_upper_bound=4, 
                ffm_report_summed_ints='false',
                ffm_disable_isotope_filtering='true',
                ffm_use_smoothed_intensities='true',
                ms_level=1)
    return default                                


def default_config():
    default=dict(project_folder=None,
                 subfolders={'source_dir':None, 'result_dir':'RESULT', 
                                  'config_dir': 'TOOLBOX'},
                 data_files=[],
                 parameters={},
                 current_result_file=None)
    return default