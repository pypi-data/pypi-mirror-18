# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 15:36:49 2016

@author: pkiefer
"""

##################################################################################################
# inspect and modify results
import emzed
from emzed import gui
from wtbox.utils import process_time
from wtbox.table_operations import split_table_by_columns
from wtbox._fix_inspector_bug import fix_ms2_inspect_integration_bug as _inspect

def inspect_and_modify(result, inspect_split_cols=(None,), modify=True, fun=None, 
                       modify_split_cols=(None,), fun_kwargs=None, diff_col='area', max_diff=100):
    """
    """
    if modify:
        reminder=extract_result_before_inspection(result)
        gui.showInformation('you can modify values of column %s in the table explorer, '\
                            'changes will be saved.' %diff_col)
    results=prepare_for_inspection(result, inspect_split_cols)
    # ms2 visualization bug
    _inspect(results)
    if modify:
        after = rebuild_result(results)
        return process_time(calculate,(reminder, after, fun, fun_kwargs, diff_col, 
                                       modify_split_cols, max_diff))
    return results, False

def extract_result_before_inspection(result):
    if isinstance(result, list):
       _add_split_id(result)
       m=0
       for r  in result:
           r.addColumn('id_', range(m, len(r)+m), type_=int)
           m+=len(r)
       return emzed.utils.stackTables(result)
    elif isinstance(result, emzed.core.data_types.Table):
         result.addColumn('id_', range(len(result)), type_=int)
         return result.copy()
    assert False, 'result must be list of Tables or Table and not %s' %type(result) 


def _add_split_id(tables):
    [r.addColumn('split_id', i, type_=int) for r,i in zip(tables, range(len(tables)))]     


def prepare_for_inspection(result, split_cols):
    if all(v is not None for v in split_cols):
        if isinstance(result, list):
            result=emzed.utils.stackTables(result)
        assert result.hasColumns(*split_cols), 'columns are missing in result or set function'\
                                                'argument `split`=False!'
        results=split_table_by_columns(result, split_cols)
        _add_title_to_tables(results, split_cols)
        return results
    else:
        return result


def _add_title_to_tables(tables, title_cols):
    for t  in tables:
        t.title='_'.join([str(t.getColumn(title_col).uniqueValue()) for title_col in title_cols])


def rebuild_result(results):
    if isinstance(results, list):
        result=emzed.utils.stackTables(results)
        if result.hasColumn('splitter'):
            result.dropColumns('splitter')
        return result
    return results # since it is already a table
        

def calculate(reminder, after, fun, fun_kwargs, diff_col, modify_split_cols, max_diff):
    modified=[]
    changed=False  
    tables=prepare_for_post_processing(after, modify_split_cols)
    for t in tables:
        if different_values(reminder, t, value=diff_col, max_diff=max_diff):
            print 'recalculating modified values ....' \
#            % compound.getColumn('compound').uniqueValue()
            if fun: # if funtion for recalculation was provided
                modified.append(fun(t, fun_kwargs))
            else: # manualy changes are kept without further reprocessing
                modified.append(t)
            changed=True
        else:
            modified.append(t)
    modified=emzed.utils.stackTables(modified)
    print 'Done.'
    modified.dropColumns('id_')
    if modified.hasColumn('split_id'):
        modified=modified.splitBy('split_id')
        [m.dropColumns('split_id') for m in modified]
    return modified, changed


def prepare_for_post_processing(t, split_cols):
    try: 
      return split_table_by_columns(t, split_cols)
    except:
        if t.hasColumn('split_id'):
            return t.splitBy('split_id')
        return [t]


def different_values(before, after, max_diff=100, id_='id_', value='area'):
    comp=after.fastJoin(before, id_)
    c=comp.getColumn
    if max_diff:
        comp.addColumn('diff', (c(value)-c(''.join([value,  '__0']))).apply(abs)<=max_diff, 
                              type_=bool)
    else:
        comp.addColumn('diff', (c(value)==c(''.join([value,  '__0']))).thenElse(True, False))
    return not all(comp.diff.values)
#############################################################################