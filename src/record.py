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
import src.task as T



def has_submit(user, db):
    sql = "select from "


def submit_record(user, jobs, plans):
    db = Database()
    comands = []
    
    jps, keys, texts = [{}, {}], ["job", "plan"], ["任务", "计划"]
    for i, rs in enumerate([jobs, plans]):  
        for r in rs: 
            w = WorkRecord()
            w.load_data(user, r)
            sql, params = w.get_sql(i)
            comands.append([sql, params])
            
            if w.task_id == None:
                if w.task == "": return False, "任务不能为空！" 
                continue 
            if int(w.task_id) == -1: continue
            if w.task_id in jps[i]: return False, "%s项重复！" % texts[i]
            jps[i][w.task_id] = w.progress 
            
            flag, msg = check_record(w, jps[0], db, keys[i])
            if not flag: return flag, msg 
        '''End For 2'''
    '''End For 1'''
    
    flag, data = db.Transaction(comands)
    if not flag: data = "请检查数据问题或今日是否已提交"
    
    return flag, data


def check_record(record, jps, db, key="plan"):
    word = {'plan': "计划", 'job': "完成"}[key]
    tid, p, user = record.task_id, record.progress, record.user
    '''计划进度不能小于本日进度'''
    if key=="plan" and p < jps.get(tid, 0): 
        return False, "任务的计划进度不能小于本日完成进度！"
    
    info = T.get_task_control(tid, user, db)
    if p < info['min']: 
        return False, "%s进度不能小于当前进度，请核对或先进行任务计划变更！" % word
    if key=="job" and info['progress'] != None: 
        return False, "该任务进度本日已有协作成员提交，请核对或先进行任务计划变更！"
    
    return True, "核验通过"

def create_record(user, category, task_id, module_id, project_id, workday, \
                  progress, content="", mark="", leader=""):
    d = WorkRecord(category, project_id, module_id, task_id, None)
    d.set_data(user, workday, progress, content, mark, leader)
    d.create()
    
    
if __name__ == '__main__':
    create_record("admin", 0, None, None, None, "2020-10-26", 98, "写文档", "无", "刘备")
    
    pass