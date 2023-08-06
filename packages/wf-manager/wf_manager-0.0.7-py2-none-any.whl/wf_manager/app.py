from example_my_workflow import my_main_workflow, modify_peak
from example_my_config import my_config_gui, my_default_config
from run_workflow import run_workflow
"""
run_workflow(my_workflow, my_config, my_config_gui=None, modify=True, my_calculation=None, 
                 diff_col='area', inspect_split_cols=(None,),  modify_split_cols=(None,))
"""
def run():
    print 
    print 'name of executed workflow: %s' %my_main_workflow.func_name
    run_workflow(my_main_workflow, my_default_config, my_config_gui=my_config_gui, modify=True, 
                my_calculation=modify_peak, inspect_split_cols=('source',), diff_col='area', 
                modify_split_cols=('source',), save_excel=True)



if __name__=='__main__':
    run()
    