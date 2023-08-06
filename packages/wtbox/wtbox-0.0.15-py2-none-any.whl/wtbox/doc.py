# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:38:24 2016

@author: pkiefer
"""
import os
import webbrowser
here = os.path.dirname(os.path.abspath(__file__))

def read():
    path=os.path.join(here, r'docs\workflow_documentation_.htm')
    print path
    print os.path.exists(path)
    webbrowser.open(path)    