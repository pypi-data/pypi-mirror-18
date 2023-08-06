# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 17:05:28 2016

@author: pkiefer
"""
from emzed import gui
def_dir=r'\\gram\biol_micro_gr_vorholt\OMICS'
#from emzed.core.data_types import PeakMap, Table
import workflow_manager as manager
#################################################################################################
def run_workflow(my_workflow, my_config, my_config_gui=None, modify=True,  
                 my_calculation=None, diff_col='area', max_diff= 100.0, inspect_split_cols=(None,),  
                 modify_split_cols=(None,), save_excel=True):

    """ Main function of the workflow_builder module: Function arguments:
        - my_workflow: 
        Main function of the workflow you want to execute in workflow_builder environment. 
        -my_config: 
        Contains parameter2value dictionary of your workflow main function
        - my_config_gui [optional]: you can provide configuration graphical user interface to change
        workflow parameters by the user. If none values from my_config are used for anaylsis
        - modify [optional]: if True all changes of column specified in diff col are taken into 
        account and will be saved.
        - my_calculation [optional]: 
        Function used to recalculate values after resutl inspection and manual
        changes. Typicaly the user reintegrates peaks manuyally and the corresponding values are
        calculated again by function my_calculation. If my calulation is None only manual changes
        are taken into account.
        - inspect_split_cols [optional]: 
        Result table will be splited by column names listed in argument such
        as each of the column contains only unique values. Example: Your result table contains  
        a column compound_name and you want to expect your result compound-wise. To do so define
        inspect_split_cols = (compound_name,). If you want to expect your result compound-wise and
        sample-wise (typically column name is source) define inspect_split_cols=(compound_name, source).
        - modify_split_cols [optional]: 
        Allows accelerationg recalculation process. It splits the table into
        tables which can be correctly processed by the function my calculation. For instance you
        determine the mass isotopologue distributiuon of different features in different samples
        and you want to repocess only those features where peaks have been reintegrated, you split 
        the result table into tables where each subtable contains 1 feature (column name = fid) 
        and one sample (column name = source) by defining modify_split_col=(fid, source).
        - save_excel: If True results are additionaly saved in excel sheet
    """
    kwargs={'modify' : modify,  'inspect_split_cols':inspect_split_cols,  
            'modify_split_cols':modify_split_cols ,'diff_col':diff_col, 'max_diff':max_diff}
            
    class DefaultMainGui(gui.WorkflowFrontend):
        """
        """
        workflow_label=my_workflow.func_name # identifyer from function name
        id2results=gui.WorkflowFrontend().set_defaults()
        config=gui.WorkflowFrontend().set_defaults()
        project_path=gui.DirectoryItem('project path', default=def_dir, 
                                       help='enter main project folder path. '\
                                    'If a new project is initialized enter path with LC-MS data.'\
                                    'A new project structure will be built automaticaly')
        settings=gui.RunJobButton('parameter_settings', method_name='config_settings')
        start=gui.RunJobButton('run_workflow', method_name='start_analysis')
        inspect_result=gui.RunJobButton('inspect result', method_name='inspect')
        reset_params=gui.RunJobButton('remove_sets', method_name='reset')
        
        
        def config_settings(self):
            
           self.config = manager.manage_config(self.config, self.project_path, my_config_gui, 
                                               my_config, label= self.workflow_label)
        
        def start_analysis(self):
            """ import the script where you put all pieces of your workflow together.
                example
                self.result, self.config=your_script.run_analysis(self.config)
            """
            self.load_config()
            if self.config:
            #self.result, self.config=your_script.run_analysis(self.config)
                self.id2results, self.config=manager.run_workflow(self.config, my_workflow, 
                                                                  save_excel=save_excel)
                # load samples
            else:
                gui.showWarning('parameters have to be configured first !!')
                    
            
        def inspect(self):
            #  checks for existing config data
            self.load_config()
            if not self.id2results:
                self.id2results=dict()
            manager.inspect_and_modify_results(self.id2results, self.config, my_calculation, kwargs,
                                               save_excel=save_excel)
            
        
        def load_config(self):
            if not self.config: 
                self.config=manager.load_config(self.project_path, self.workflow_label)
                
                    
        
        def reset(self):
            self.load_config()
            manager.remove_batches(self.config, self.project_path, self.workflow_label)
            
            
    DefaultMainGui().show()
        
    
