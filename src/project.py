#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''
from src.libs.database import Database 
from src.common.base import Project, Module


def create_project(create_user, name, description=""):
    p = Project(None, name, create_user, description)
    flag = p.create()
    if flag != -1:
        t = Module(flag, None, "其它", create_user)
        t.create()
    
    return flag if flag != -1 else False

def get_project_list(create_user, category, department, page = 0, size = 26):
    db = Database()
    keys = ['id', 'name', 'createUser', 'status', 'manager', 'createTime', 'description',
            'category', 'department', 'mark']
    sql, params = "select " + ','.join(keys) + " from project where 1", []
    if create_user != '': 
        sql += " and createUser=%s"
        params.append(create_user)
    if category != '': 
        sql += " and category=%s"
        params.append(category)
    if department != '': 
        sql += " and department=%s"
    sql += " order by createTime desc"
    data = []
    count, cursor = db.selectPage(sql, params, page, size)
    for item in cursor:            
        line = { k:item[i] for (i, k) in enumerate(keys) }
        line['createTime'] = str(line['createTime'])
        data.append(line)
                
    return {'count': count, 'lines': data}


if __name__ == '__main__':
    create_project("lucy", "p1", "mp number")
    
#     ps = get_project_list("", "", "")
#     print(ps)

        
    pass