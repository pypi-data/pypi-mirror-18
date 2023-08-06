# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:24:31 2016

@author: pkiefer
"""
import emzed

def my_default_config():
    config=dict()
    config['peaks_table']=r'Z:\pkiefer\temp\Mike_W\atp_peaks.table'
    config['min_area']=250
    config['id_col']='fid'
    return config

def my_config_gui(config,):
    keys=['peaks_table', 'min_area', 'id_col']    
    params=emzed.gui.DialogBuilder('Configuration')\
    .addFileOpen('select peaks table', formats=['table'], default=config['peaks_table'])\
    .addFloat('min peak area', default=config['min_area'])\
    .addString('feature id column name', config['id_col'])\
    .show()
    for i in range(len(keys)):
        config[keys[i]]=params[i]
    