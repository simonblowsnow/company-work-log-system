#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''

from datetime import datetime
from src.libs.database import Database
from src.common.base import Task, WorkRecord
 

def submit_record(user, jobs, plans):
    db = Database()
    comands = []
    tids = set()
    for job in jobs: 
        w = WorkRecord()
        w.load_data(user, job)
        sql, params = w.get_sql()
        comands.append([sql, params])
        
        if w.task_id in tids: return False, "任务项重复！"
        tids.add(w.task_id)
    
    tids = set()
    for job in jobs:
        w = WorkRecord()
        w.load_data(user, job)
        
        if int(w.task_id) == -1: continue
        if w.task_id in tids: return False, "计划项重复！"
        tids.add(w.task_id)
        
    flag, data = db.Transaction(comands)
    
    return flag, data

def check_plan(tids, db):
    sql = "select taskId, max(progress) from record_day where taskId in (2) group by taskId"
    

def create_record(user, category, task_id, module_id, project_id, workday, \
                  progress, content="", mark="", leader=""):
    d = WorkRecord(category, project_id, module_id, task_id, None)
    d.set_data(user, workday, progress, content, mark, leader)
    d.create()
    
    
if __name__ == '__main__':
    create_record("admin", 0, None, None, None, "2020-10-26", 98, "写文档", "无", "刘备")
    
    pass