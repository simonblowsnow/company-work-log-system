#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''

from src.common.base import WorkRecord


def create_record(user, category, task_id, module_id, project_id, workday, \
                  progress, content="", mark="", leader=""):
    d = WorkRecord(category, project_id, module_id, task_id, None)
    d.set_data(user, workday, progress, content, mark, leader)
    d.create()
    
    
if __name__ == '__main__':
    create_record("admin", 0, None, None, None, "2020-10-26", 98, "写文档", "无", "刘备")
    
    pass