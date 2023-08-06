# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 17:25:38 2016

@author: pkiefer
"""
from copy import deepcopy
import emzed

def fix_ms2_inspect_integration_bug(t):
    PeakMap=emzed.core.data_types.PeakMap
    t.replaceColumn('peakmap', t.apply(modify_peakmap,(t.peakmap, 1)), type_=PeakMap)
    emzed.gui.inspect(t)
    t.replaceColumn('peakmap', t.apply(modify_peakmap,(t.peakmap, 2)), type_=PeakMap)



def modify_peakmap(pm, level=1):
    pm_ = deepcopy(pm)
    for spec in pm_.spectra:
        spec.msLevel=level
    return pm_
    



    