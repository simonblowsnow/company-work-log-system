#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''
from src.libs.database import Database
from src.common.base import Module


def create_module(project_id, create_user, name, description=""):
    m = Module(project_id, None, name, create_user, description)
    flag = m.create()
    return flag if flag != -1 else False
    
    
def get_module_list(pid, create_user, category, department):
    db = Database()
    keys = ['id', 'name', 'projectId', 'createUser', 'status', 'manager', 'createTime', 'description',
            'category', 'department', 'mark']
    sql, params = "select " + ','.join(keys) + " from module where projectId=%s", [pid]
    if create_user != '': 
        sql += " and createUser=%s"
        params.append(create_user)
    if category != '': 
        sql += " and category=%s"
        params.append(category)
    if department != '': 
        sql += " and department=%s"
    sql += " order by createTime desc"
    
    data = db.read_all(sql, params)
    for line in data: line['createTime'] = str(line['createTime']) 
    
    return data
    
    
if __name__ == '__main__':
#     create_module(1, "admin", "模块1", "这是一个模块")
#     print(get_module_list(1, "", "", ""))
    pass

