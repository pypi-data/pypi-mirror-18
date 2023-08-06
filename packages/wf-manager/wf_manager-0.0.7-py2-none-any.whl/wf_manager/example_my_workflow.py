# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 10:48:01 2016

@author: pkiefer
Simple example workflow
I separated peak_extraction from mid calculation since now it is possible to reuse the function
`analysis peaks` for the inspect_and_modify functionality.
To integrate your workflow into the workflow_builder extension see workflow_builder.app
"""
import emzed
from wtbox.feature_extraction import targeted_peaks_ms
from wtbox.feature_analysis import calculate_mid


def my_main_workflow(peakmaps, config):
    peaks=get_peaks(peakmaps, config)
    results=analyze_peaks(peaks, config)
    return results

def get_peaks(pms, config):
    peaks_table=emzed.io.loadTable(config['peaks_table'])
    keys=['min_area']
    kwargs={key: config[key] for key in keys}
    return [targeted_peaks_ms(pm, peaks_table, **kwargs ) for pm in pms]

    
def analyze_peaks(peaks, config):
    return [modify_peak(peak, config) for peak in peaks]
    
    
def modify_peak(peak, config):
    keys=['id_col']#id_col='feature_id', quantity_col='area', result_col='mi_fraction'
    kwargs={key: config[key] for key in keys}
    return calculate_mid(peak, **kwargs)