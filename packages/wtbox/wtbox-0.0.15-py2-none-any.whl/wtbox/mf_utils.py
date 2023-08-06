# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:26:40 2015

@author: pkiefer
"""
import emzed
#import utils
import numpy as np
import re

############################################################################################

def count_element(el, mf):
    """ count_element(el, mf) counts number of element el in molecular formula mf 
    """
    assert isinstance(el, str) and isinstance(mf, str)
    def num2str(v):
        if v=='':
            return 1
        else:
            return int(v) 
    fields = re.findall("([A-Z][a-z]?)(\d*)", mf)
    selected=[num2str(number) for element, number in fields if element==el]
    return int(sum(selected))

###############################################################################################

def restrict_db(db, C = (2,None), H=(0,None), N= (0,None), O=(0,None), 
                P=(0,None), S= (0,None), el2range=None, mass_range=None):
    """
    Funtion restrict_db(db, C = (2,None), H=(0,None), N= (0,None), O=(0,None), 
                P=(0,None), S= (0,None)el2range=None, mass_range=None) filters data_base db  
                for compounds composed of  C, H, N, O, P, S. Further elements can be included
    by el2range  with allowed elements are keys and tuple values defining the lower and upper 
    limit for each element. If upper limit equals None no 
    upper limit is given.  If a formula contains elements not present in the dictionary or 
    the number of elements is not in predifined range, the formula will be removed. Example: 
    if you set el2range={'Fe': (1,2)} and keep default values for plot only formula containing
    1-2 Fe and at least 2 C will be selected. Optional a global mass range for the data base 
    can be defined with mass_range.
    """
    
    if not el2range:
        el2range=dict()
    for key, arg in zip('CHNOPS',(C, H, N, O, P, S)):
        el2range[key]=arg
    
    def fun(mf, el2range):
        ok=[]
        for el in el2range.keys():
            num=count_element(el, mf)
            min_, max_=el2range[el]
            if max_!=None:
                check=True if min_<=num<=max_ else False
            else:
                check=True if min_<=num else False
            ok.append(check)
        return all(ok)
                
    # restrict db to mf with num C >=2
    db.updateColumn('select',db.apply(fun, (db.mf, el2range)), type_=int)
    t=db.filter(db.select==True)
    # restrict to elements
    elements=el2range.keys()
    t=t.filter(t.mf.containsOnlyElements(elements)==True)
    print len(t)
    t.dropColumns('select')
    db.dropColumns('select')
    # restrict min mass to 100
    if not mass_range:
        mass_range=(db.m0.min(), db.m0.max())
    return t.filter(t.m0.inRange(*mass_range))

#def get_default_el2range():
#    return {'C': (2,None), 'H':(0,None), 'N': (0,None), 'O':(0,None), 'P':(0,None), 'S': (0,None)}


def build_mf_restriction_lib(mass, dm=70, db=None, el2range=None):
    """
    build_mf_restriction_lib(mass, dm=70, db=None) returns number range of elements C, H , N , O,
    P, and S for for all formulas found in data base db within mass range (mass-dm; mass + dm) for
    heuristic restriction of the solution space. The output is a dictionary with element as key 
    and observed element distribution tuple as value with entries (min, mean, std, max)
    example {C:(2, 14, 11, 24), 'O': (0, 3, 6, 12)}. If no data base is provided 
    emzed pubchem data base will be used. Prior to analyis applied data_base will be filtered 
    by dictionary el2range default el2range={'C': (2,None), 'H':(0,None), 'N': (0,None), 
    'O':(0,None), 'P':(0,None), 'S': (0,None)}, where allowed elements are keys and
    the tuple defines the lower and upper limit for each element, if upper limit equals None
    no upper limit is given. If a formula contains elements not present in the dictionary the 
    formula will be removed.
        
    """
    if not db:
        db=emzed.db.load_pubchem()
    db=restrict_db(db, el2range=el2range)
    return build_mass2CHNOPS_restriction(db, mass, dm=dm)

def build_mass2CHNOPS_restriction(t, mass, dm=70):
    t=t.filter(t.m0.inRange(mass-dm,mass+dm))
    mfs= t.mf.values
    print 'number of formulas:', len(mfs)
    return {el:_min_max_el(el, mfs)for el in 'CHNOPS'}


def _min_max_el(el, mfs):
    count=count_element
    nums=[count(el, mf) for mf in mfs]
    return min(nums), int(round(np.mean(nums))), int(round(np.std(nums)*2.576)), max(nums)


############################################################
# Missing Rules from 7 golden rules paper to restrcict 
# possible mf found with emzed.utils.formulaTable


def restricted_formula_table(min_mass, max_mass, C=(0, None), H=(0, None), N=(0, None), 
                             O=(0, None), P=(0, None), S=(0, None), prune=True, level='extended'):
    """ This is the enlarged version of emzed.utils.formulaTable
        
        This function generates a table containing molecular formulas consisting of
        elements C, H, N, O, P and S having a mass in range
        [**min_mass**, **max_mass**].
        
        If **prune** is *True*, mass ratio rules (from "seven golden rules") and valence
        bond checks are used to avoid unrealistic compounds in the table. Moreover, Rule #4
        and rule #4 – Hydrogen/Carbon element ratio check and rule #5 – heteroatom ratio check, as 
        well # rule 6: element probability check of molecular formula mf will be applied. For rule
        #4 and # 5 2 levels of inclusion can be applied: common: 99.7 % of all formulas are covered, 
        extended: 99.99% of all formulas are covered. To cover molecules like BPG or FBP 'extended'
        mode is required. 
       
       For each element one can provide an given count or an inclusive range of
        atom counts considered in this process.
        Putting some restrictions on atomcounts, eg **C=(0, 100)**, can speed up
        the process tremendously.
    """
    formulatab=emzed.utils.formulaTable
    args=[min_mass, max_mass, C, H, N, O, P, S, prune]
    def rule_4(mf, level=level):
#        print all([x2c_check(mf, el, level) for el in 'HNOPS'])
        return all([x2c_check(mf, el, level) for el in 'HNOPS'])
    def rule_6(keep, mf):
        return el_comb_check(mf) if keep else keep
        
    t=formulatab(*args)
    if prune:
        t.addColumn('keep', t.apply(rule_4, (t.mf, level)), type_=bool)
        t.replaceColumn('keep', t.apply(rule_6,(t.keep, t.mf)), type_=bool)
        t=t.filter(t.keep==True)
        t.dropColumns('keep')
    return t
        
        
        

# Rule 4 AND 5
def x2c_check(mf, el='H', level='extended'):
    """ #Rule #4 – Hydrogen/Carbon element ratio check and rule #5 – heteroatom ratio check  
        from 7 golden rules paper: common: 99.7 % of all formulas are covered, 
        extended: 99.99% of all formulas are covered 
    """
    assert el in 'HNOPS'
    
    el2num=_get_el2num(mf)
    num_x = el2num.get(el)
    num_x = float(num_x) if num_x else 0.0
    num_c= el2num.get('C')
    if not num_c: 
        return False
    x2c=num_x/num_c
    min_, max_=_ratio_limits()[el][level]
    return True if min_ <= x2c <= max_ else False
        
        

def _ratio_limits():
    return {'H': {'common': (0.2, 3.1), 'extended' : (0.1, 6.0)},
            'N': {'common': (0.0, 1.3), 'extended' : (0.0, 4.0)},
            'O': {'common': (0.0, 1.2), 'extended' : (0.0, 4.0)},
            'P': {'common': (0.0, 0.3), 'extended' : (0.0, 2.0)},
            'S': {'common': (0.0, 0.8), 'extended' : (0.0, 3.0)}}
    
# Rule 6: element probability check

def el_comb_check(mf):
    """# Rule 6: element probability check of molecular formula mf from 7 golden rules paper. 
    Additional filter function for function emzed.utils.formulaTable.
    """
    el2num=_get_el2num(mf)
    checks=[]
    if all([el2num.get(el)>1 for el in 'NOPS']):
        check=all([el2num['N']<10, el2num['O']<20, el2num['P']<4, el2num['S']<3])
        checks.append(check)
    else:
        checks.append(True)
    if all([el2num.get(el)>3 for el in 'NOP']):
        check=all([el2num['N']<11, el2num['O']<22, el2num['P']<6])
        checks.append(check)
    else:
        checks.append(True)
    if all([el2num.get(el)>1 for el in 'OPS']):
        check=all([el2num['O']<14, el2num['P']<3, el2num['S']<3])
        checks.append(check)
    else:
        checks.append(True)
    if all([el2num.get(el)>1 for el in 'PSN']):
        check=all([el2num['P']<3, el2num['S']<3, el2num['N']<4])
        checks.append(check)
    else:
        checks.append(True)
    if all([el2num.get(el)>6 for el in 'NOS']):
        check=all([el2num['N']<19, el2num['O']<14, el2num['S']<8])
        checks.append(check)
    else:
        checks.append(True)
    return all(checks)

def _get_el2num(mf):
    if isinstance(mf, str):
        mf=emzed.utils.formula(mf)
    try:
        d=mf.asDict()
        return {key[0]: d[key] for key in d.keys()}    
    except:
        return {}