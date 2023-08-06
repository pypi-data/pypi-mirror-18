# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 11:29:19 2016

@author: pkiefer
"""

from _default_data_manager import get_config, get_config_path, save_config, select_from_existing
from _default_data_manager import setup_batches, main_analyze_batches, remove_batch_dialog
from _default_data_manager import load_config as _load_config
from inspect_and_modify import inspect_and_modify
from _default_data_manager import save_result
from emzed import gui
from wtbox import in_out

def manage_config(config, project_path, my_config_fun, my_default_params, label='my_workflow'):
    config_path=get_config_path(project_path, label, foldername='TOOLBOX', configname='config')
    config=get_config(config, config_path, project_path)
    default_params=my_default_params()
    setup_batches(config, my_config_fun, default_params, batch=True)
    save_config(config, config_path)
    gui.showInformation('configuration setup finished')
    return config


def load_config(project_path, label):
    config_path=get_config_path(project_path, label, foldername='TOOLBOX', configname='config')
    return _load_config(config_path)


def run_workflow(config, my_workflow, save_excel=True):
    if not len(config['batch2params']) and len(config['batch2samples']):
        gui.showWarning('no data sets configured. Please configure your set first!')
    result=main_analyze_batches(config, analysis_fun=my_workflow, save_excel=save_excel)
    gui.showInformation('Finished')
    return result, config
    
    
##################################################################################################
def inspect_and_modify_results(id2results, config, calc_fun, kwargs, save_excel=True):
    while True:
        id_=select_from_existing(config, inspect_result=True)
        if id_:
            fun_kwargs=config['batch2params'][id_]
            result=_get_result(id2results, config, id_)
            result, modified=inspect_and_modify(result, fun=calc_fun, fun_kwargs=fun_kwargs, **kwargs)
            if modified:
                id2results[id_]=result
                path=config['batch2result'][id_]
                save_result(result, id_, config, path=path, save_excel=save_excel)
        if not gui.askYesNo('continue inspection?'):
            break
#    return id2results
    

def _select_batch(config):
    ids=config['batch2result'].keys()
    pos=gui.DialogBuilder('select result from batch')\
    .addChoice('select_batch_id', ids)\
    .show()
    return ids[pos]


def _get_result(id2results, config, id_):
    
    if id2results.has_key(id_):
        return id2results[id_]
    else:
        path=config['batch2result'][id_]
        print 'loading result %s ...' %path
        return in_out.load_list_of_tables(path)    
    assert False, 'if this assertion occurs there is a bug with config handling. '\
                    'Contact Patrick Kiefer pkiefer@ethz.ch'
############################################################################################


def remove_batches(config, project_path, label):
    remove_batch_dialog(config)
    config_path=get_config_path(project_path, label, foldername='TOOLBOX', configname='config')
    save_config(config, config_path)