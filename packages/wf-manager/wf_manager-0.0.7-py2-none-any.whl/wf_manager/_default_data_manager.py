# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 10:59:48 2016

@author: pkiefer
"""
import os
from wtbox import in_out
import glob
import emzed
from emzed import gui
from emzed.core.data_types import Table, PeakMap
from shutil import rmtree
#from collections import defaultdict
import hashlib
from copy import deepcopy
###################################################################################################
# default config setup environment

def get_config(config, path, project_dir):
    if not config and os.path.exists(path):
        config=load_config(path)
    if not config:
        config=default_config(project_dir)
    return config

def load_config(path):
    if os.path.exists(path):
        return in_out.load_dict(path)

def get_config_path(project_path, label, foldername='TOOLBOX', configname='config'):
    dir_=os.path.join(project_path, foldername)
    _make_dir(dir_)
    name='_'.join([configname, label])
    name='.'.join([name, 'json'])
    return os.path.join(dir_, name)

def save_config(config, path):
    in_out.save_dict(config, path, True)


def _make_dir(dir_):
    if not os.path.exists(dir_):
        os.mkdir(dir_)
        


def default_config(project_dir):
    config=dict()
    config['batch_ids']=[] # list of all batch ids
    config['batch2params']={} # contains workflow parameters
    config['batch2samples']={} # contains list with sample pathes
    config['batch2result']={} # contains result_path
    config['sidpid2batch']=dict() # allows checking for existing batches
    config['batch2sidpid']=dict()
    config['current_result']=None # contains latest analysis results
    config['project_dir']=project_dir
    return config



def setup_batches(config, my_config_fun, default_params, batch=True):
    loop = True
    individual=_params_setup_mode()    
    first=True
    params=default_params
    while loop:
        data=select_samples(config, batch=True)
        if isinstance(data, dict):
            if first or individual:
                setup_batch2params(my_config_fun, params, data)
                
                params=data['batch2params']
                
            else:
                setup_batch2params(None, params, data)  
            if _check_for_existing(config, data):
                _update_config(config, data)
                first=False
                
            loop=_continue(batch)
        else:
            loop=False


def _check_for_existing(config, data):
    pathes_data=sorted(data['batch2samples'])
    pid_data=_hash_parameters(data['batch2params'])
    for id_ in config['batch2samples'].keys():
        check1=pathes_data==sorted(config['batch2samples'][id_])
        pid=_hash_parameters(config['batch2params'][id_])
        check2=pid==pid_data
        if check1 and check2:
            gui.showWarning('The selected data set and corresponding parameters '\
            'is identical to batch %s. Your selection will be ignored!!' %id_)
            return False
    return True
    
        
def _update_config(config, data):
    id_=data['id_']
    config['batch2samples'][id_]=data['batch2samples']
    config['batch2params'][id_]=data['batch2params']

        

def update_results(config, id_, result_path, samples):
    params=config['batch2params'][id_]
    pid=_hash_parameters(params)
    sid=get_samples_id(samples)
    sidpid=str((sid, pid))
    config['batch2result'][id_]=result_path
    config['sidpid2batch'][sidpid]=id_
    config['batch2sidpid'][id_]=sidpid    
    config['current_result']=result_path
    config['batch_ids'].append(id_)
#############################################################################
# routine to select samples in workflow GUI

def select_samples(config,  batch=True):
    data=dict()
    batch_ids=config['batch2samples'].keys()
    start_at=config['project_dir']
    select=['select_samples', 'select exisisting sample set', 'skip selection']
    # GUI
    def_label=''.join(['set_', str(len(batch_ids))])
    i=0
    while def_label in batch_ids:
        i+=1
        ''.join(['set_', str(len(batch_ids)+i)])
        
    mode, id_, dir_, remove=gui.DialogBuilder('select samples folder')\
    .addChoice('mode of sample selection', select, default=0, help='')\
    .addString('sample set id', def_label, help='name of subfolder containing batch result'\
    'existing ids: %s' % ', '.join(config['batch_ids']))\
    .addDirectory('samples folder', default=start_at)\
    .addBool('remove blanks', default=True, help='removes blank peakmaps from sample list')\
    .show()
   
    while not _check_for_existing_id(id_, config) and mode <2:
        id_=gui.DialogBuilder('choose different data set id')\
        .addString('sample set id', def_label, help='name of subfolder containing batch result'\
        'existing ids: %s' % ', '.join(config['batch_ids']))\
        .show()
    data['id_']=id_
    if mode ==0:
        targets=get_targets(dir_, remove)
        while not  _check_for_peakmaps(targets, dir_):
            dir_=gui.DialogBuilder('choose different sample folder')\
            .addDirectory('samples folder', default=start_at)\
            .show()
            targets=get_targets(dir_, remove)
        samples=_select_samples(targets)
        data['batch2samples']=samples
        return data
    if mode == 1:
        data['batch2samples']=select_from_existing(config)
        return data
    return 
            
    

def _check_for_existing_id(id_, config):
    if id_ in config['batch_ids']:
        gui.showWarning('batch id %s already in project. Please choose another name' %id_)
        return False 
    return True


def _check_for_peakmaps(targets, dir_):
    if not len(targets):
            gui.showWarning('%s contains no peakmap! Please choose another folder' %dir_)
            return False
    return True
        

def get_targets(dir_, filter_blank=True):
    pathes=[]
    for ending in ['*.mzML', '*.mzXML', '*.table']:
       target=os.path.join(dir_, ending) 
       pathes.extend(glob.glob(target))
    if filter_blank:
        pathes=in_out.filter_blanks(pathes)
    pathes.sort()
    return pathes


def _select_samples(targets):
    choice=[os.path.basename(p) for p in targets]
    select=gui.DialogBuilder('select')\
    .addMultipleChoice('select samples', choice, default= range(len(choice)), vertical=3)\
    .show()
    return [targets[i] for i in select]


# potential improvement in next version ....
def select_from_existing(config, inspect_result =False):
    if not len(config['batch2samples'].keys()):
        gui.showWarning('Currently no sample batches exists!')
        return False
    
    class SelectExisting(gui.WorkflowFrontend):
        c=config
        id_=gui.WorkflowFrontend().set_defaults()
        ids=(c['batch2samples'].keys()) if not inspect_result else (c['batch2result'].keys())
        ids.sort()
        confirm=gui.RunJobButton('select set', method_name='set_id')
        show_=gui.RunJobButton('show set details', method_name='show_details')
        config['temp']=None
        
        def show_details(self):
            if self.id_:
                text=[]
                text.append( 'samples of set %s:' %self.id_)
                for path in config['batch2samples'][self.id_]:
                    text.append(path)
                
                if inspect_result:
                    text.append('')
                    text.append('config parameter settings:')
                    for key in config['batch2params'][self.id_]:
                        line='\t'.join( ['%s:'%key, str(config['batch2params'][self.id_][key])])
                        text.append(line)
                text='\n'.join(text)
                print text
                gui.showInformation(text)
            else:
                gui.showInformation('First, please select a set.')
                
            
        def set_id(self):
            pos=gui.DialogBuilder('select_set')\
            .addChoice('set', self.ids, default=0)\
            .show()
            self.id_=self.ids[pos]
            config['temp']=self.id_
            
            
    SelectExisting().show()
    id_=config.pop('temp')
    if inspect_result:
        return id_ 
    return config['batch2samples'].get(id_)

def show_samples(data):
    print data

def _continue(batch):
    if batch:
        if gui.askYesNo('add another set?'):
            return True
    return False
    

def update_start_at(pathes):
    return os.path.dirname(pathes[0]) if pathes else None

###################################################################################################

def remove_batch_dialog(config):
    while True:
        batch_ids=get_ids(config)
        if len(batch_ids):
            pos=gui.DialogBuilder('remove batch from project')\
            .addChoice('select', batch_ids)\
            .show()
            id_=batch_ids[pos]
            if gui.askYesNo('Do you realy want to remove the batch %s  and all results?'%id_):
               remove_batch(config, id_) 
        else:
            gui.showInformation('currently there are no processed batches in project!')
            break
        repeat=gui.askYesNo('remove another analysis?')
        if not repeat:
            break

def remove_batch(config, id_, rerun=False):
    _remove_batch_path(config, id_)
    _remove_id_from_config(config, id_)
    gui.showInformation('batch %s removed from project!' %id_)


def get_ids(config):
    ids_=[]
    keys=['batch2samples', 'batch2params', 'batch2result']
    for key in keys:
        ids_.extend(config[key].keys())
    return sorted(list(set(ids_)))
        

def _remove_batch_path(config, id_):
    result_dir=os.path.join(config['project_dir'], 'RESULTS', id_)
    try:
        rmtree(result_dir)
    except:
        print 'No data found for %s' %id_

     
def _remove_id_from_config(config, id_):
    keys=['batch2samples', 'batch2params', 'batch2result']
    if config['batch2result'].get(id_)==config['current_result']:
        config['current_result']=None
    for key in keys:
        try:
            x=config[key].pop(id_) # suppresses pop up
            del x
        except:
            pass
    if id_ in config['batch_ids']:
        config['batch_ids'].remove(id_)
    try: 
        sidpid=config['batch2sidpid'].pop(id_)
        x=config['sidpid2batch'].pop(sidpid)
#        while id_ in values:
#            values.remove(id_)
#        if len(values):
#            print 'this message should never occur!!!'
#        else:
#            sidpid
    except:
        pass
    
        
##################################################################################################
# general method to setup workflow dependent parameters

def setup_batch2params( gui_fun, default_params, data):
    inspect=True if gui_fun else False
    param2value=deepcopy(default_params)
    data['batch2params']=param2value
    if inspect:
        # inspect
        gui_fun(param2value)
        data['batch2params']=param2value


def _params_setup_mode():
    # individual, process only new, reprocess if modified
    ind=gui.DialogBuilder('modify parameters for batch processing')\
    .addBool('individual parameter configuration for each set', default=False)\
    .show()
    return ind


def _get_config_params(batch2params, default, individual):
    if len(batch2params):
       return batch2params.values()[0] if identic_parameters(batch2params) else default
    return default
    

def identic_parameters(batches2params):
    params=sorted_parameter_values(batches2params)
    return all([param==params[0] for param in params])


def identitic_pathes(p1, p2):
    from filecmp import cmpfiles
    dirname=os.path.dirname
    basename=os.path.basename
    if basename(p1)==basename(p2):
        match, __, __=cmpfiles(dirname(p1), dirname(p2), [basename(p1)]) 
        if len(match):
            return True
    return False
 
 
 #################################################################################################
# check samples and configs  
def check_and_get_samples(config, id_):
    parameter_dict=config['batch2params'][id_]
    samples=load_samples(config, id_)
    pid, sid=parameter_and_sample_id(samples, parameter_dict)
    former=config['sidpid2batch'].get(str((sid, pid)))
    if former:
        gui.showWarning('Data set %s already exists in batch %s. Analysis of %s will be therefore'\
        ' skipped and setup removed from configuration!!')
        _reset_result(config, id_)
        return
    return samples

def _reset_result(config, id_):
    for key in ['batch2samples', 'batch2params']:
        x=config[key].pop(id_)
    

def parameter_and_sample_id(samples, parameter_dict):
     param_hash=_hash_parameters(parameter_dict)
     samples_hash=get_samples_id(samples)
     return param_hash, samples_hash


def get_samples_id(samples):
    pairs=[]
    for sample in samples:
         sample_hash=_get_unique_id(sample)
         pairs.append(sample_hash,)
    pairs.sort()
    return '_'.join(pairs)


def load_samples(config, id_):
    pathes=config['batch2samples'][id_]
    return [_load(p) for p in pathes]    


def _load(path):
    basename=os.path.basename(path)
    if basename.endswith('.table'):
        return emzed.io.loadTable(path)
    elif basename.endswith('.mzXML') or basename.endswith('.mzML'):
        return emzed.io.loadPeakMap(path)
    else:
        type_=basename.split('.')[-1]
        assert False, 'Only peakmap or tables are accepted and not %s' % type_
        
##################################################################################################
#  Run analysis

def main_analyze_batches(config, analysis_fun, save_excel=True):
    id2results=dict()
    workflow_label=analysis_fun.func_name
    project_path=config['project_dir']
    config_path=get_config_path(project_path, workflow_label)
    for id_ in get_ids_for_processing(config):
      params=config['batch2params'][id_]
      samples=check_and_get_samples(config, id_)
      
      if samples:
          result=analysis_fun(samples, params)
          result_path=save_result(result, id_, config, workflow_label, save_excel=save_excel)
          if result_path: # update only in case of successful saving 
              update_results(config, id_, result_path, samples)
              id2results[id_]=result
              save_config(config, config_path)
      else:
          save_config(config, config_path)
          
    return id2results
     

def _get_unique_id(item):
    assert isinstance(item, Table) or isinstance(item, PeakMap), 'sample must be of type Table or'\
            'PeakMap and not of Type %s' %type(item)
    return item.uniqueId()
   
    
def identic_items(item1, item2):
    return True if item1.uniqueId() == item2.uniqueId() else False


def _hash_parameters(parameters):
    params=str(sorted_parameter_values(parameters))
    return hashlib.md5(params).hexdigest()
    

def sorted_parameter_values(name2params):
    params=[]
    for key in sorted(name2params.keys()):
        values=[]
        if isinstance(name2params[key], dict):
            values.extend(sorted_parameter_values(name2params[key]))
        else:
            value=name2params[key]
            try:
                values.extend(sorted([value]))
            except:
                values.extend(value)
        params.append(values)
    return params


def get_ids_for_processing(config):
    processed=set(config['batch2result'].keys())
    samples=set(config['batch2samples'].keys())
    return samples - processed

def _select_batches(ids):
    if len(ids):
        ids=list(ids)
        selected=gui.DialogBuilder('select batches for analysis')\
        .addMultipleChoice('select', ids, default=range(len(ids)))\
        .show()
        return set([ids[i] for i in selected])
    return ids
##################################################################################################
# I/O results based on default config structure for batch processing workflows

def save_result(result, id_, config, workflow_label=None, path=None, save_excel=True):
    """ Function save_result saves table or list of tables if all tables have the same column 
    names, types and formats -> see emzed.io.stackTables; result -> table or list of tables; 
    id_: batch id; config: dictionary containing workflow parameters; workflow_label [optional]: 
        name of the workflow analysis function; path [optional]: saving path
    """
    Table=emzed.core.data_types.Table
    if isinstance(result, Table):
        result=[result]
    # add config settings to table meta data
    result[0].meta['config']=config
    assert all([isinstance(t, Table) for t  in result]), 'result must be a table or a list of'\
            'tables!'
    if not path:
        dir_=_make_save_dir(config, id_)
        path=_make_save_path(dir_, workflow_label)
    
    print 'saving ...' ,
    in_out.save_list_of_tables(result, path, force_overwrite = True)
    # save result as excel
    if save_excel:
        _save_as_excel(result, path)
    config['current_result']=path
    config['batch2result'][id_]=path
    print 'saved at %s' %path
    return path

def _make_save_dir(config, id_):
    result_dir=os.path.join(config['project_dir'], 'RESULTS')
    _make_dir(result_dir)
    dir_=os.path.join(result_dir, id_)
    _make_dir(dir_)
    return dir_
    
def _make_save_path(dir_, workflow_label):
    project_dir, id_=os.path.split(dir_)
    __, project = os.path.split(project_dir)
    name='_'.join([project, id_, workflow_label, 'result'])
    name='.'.join([name, 'tables'])
    return os.path.join(dir_, name)

def _save_as_excel(result, path):
   print 'save result as excel file ...'
   fields=path.split('.')[:-1]
   fields.append('xlsx')
   path='.'.join(fields)
   in_out.save_tables_as_excel(result, path, force_overwrite=True)
   print 'Done'

##################################################################################################
    