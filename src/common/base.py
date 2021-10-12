#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''

from datetime import datetime
from src.libs.database import Database 


class Project():
    def __init__(self, id_=None, name="", create_user="", description=""):
        self.id = id_
        self.name = name
        self.create_user = create_user
        self.description = description
    
    def create(self):
        db = Database()
        sql = "insert into project (name, createUser, description) values (%s, %s, %s)"
        flag = db.execute(sql, (self.name, self.create_user, self.description))
        
        return flag
    
class Module():
    def __init__(self, project_id=None, id_=None, name="", create_user="", description=""):
        self.project_id = project_id 
        self.id = id_
        self.name = name
        self.create_user = create_user
        self.description = description
    
    def create(self):
        db = Database()
        sql = "insert into module (projectId, name, createUser, description) values (%s, %s, %s, %s)"
        flag = db.execute(sql, (self.project_id, self.name, self.create_user, self.description))
        
        return flag
        
        
class Task():
    def __init__(self, project_id=None, module_id=None, id_=None):
        self.project_id = project_id
        self.module_id = module_id 
        self.id = id_
            
    def set_data(self, is_multi, name, create_user, description, plan_end_time, executor=None):
        self.is_multi = is_multi
        self.name = name
        self.create_user = create_user
        self.description = description
        self.plan_end_time = plan_end_time 
        self.executor = executor if executor else self.create_user
       
    def create(self):
        db = Database()
        sql = "insert into task (projectId, moduleId, name, createUser, description, planEndTime, executor) \
            values (%s, %s, %s, %s, %s, %s, %s)"
        flag = db.execute(sql, (self.project_id, self.module_id, self.name, self.create_user
                                , self.description, self.plan_end_time, self.executor))
        return flag
       

class WorkRecord():
    def __init__(self, category=0, project_id=None, module_id=None, task_id=None, id_=None):
        self.category = category
        self.project_id = project_id
        self.module_id = module_id 
        self.task_id = task_id
        self.id = id_
        self.task = None
        '''本表暂时设为空，理论上由任务表关联得出'''
        self.leader = None
        
    def load_data(self, user, d):
        self.user = user
        self.category = d['type']
        self.project_id = d['pid']
        self.module_id = d['mid'] 
        self.task_id = d['tid']
        self.task = d['task']
        self.workday = str(datetime.now())[:10]
        self.progress = d['progress']
        self.content = d['content']
        self.mark = d.get('mark', None)
        
        '''若未选择任务，则使用文本填充于task字段，暂不开放填报日志时不选择任务直接新建任务'''
        if self.task_id == -1: self.task_id = None 
        
        
    def set_data(self, user, workday, progress, content="", mark="", leader=""):
        self.user = user
        self.workday = workday
        self.progress = progress
        self.content = content
        self.mark = mark 
        self.leader = leader
    
    def get_sql(self):
        sql = '''insert into record_day (user, workday, category, projectId, moduleId, taskId,
            task, progress, content, mark, leader) values 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (self.user, self.workday, self.category, self.project_id, self.module_id, 
                                self.task_id, self.task, self.progress, self.content, self.mark, self.leader)
        return sql, params
     
    def create(self):
        db = Database()
        sql, params = self.get_sql()
        flag = db.execute(sql, params)
        return flag
        
        
        