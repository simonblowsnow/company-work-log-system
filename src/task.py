#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''
from src.libs.database import Database
from src.common.base import Task


def create_task(project_id, module_id, create_user, name, is_multi, plan_end_time, description=""):
    m = Task(project_id, module_id, None)
    m.set_data(is_multi, name, create_user, description, plan_end_time)
    flag = m.create()
    return flag if flag != -1 else False
    
def get_task_list(mid, create_user, category, department):
    db = Database()
    keys = ['id', 'name', 'moduleId', 'createUser', 'status', 'executor', 'createTime', 'description',
            'category', 'department', 'mark', 'progress', 'planEndTime']
    sql, params = "select " + ','.join(keys) + ", IFNULL(uc, 0) userCount from task t left join \
        (select taskId, count(*) uc from \
            (select taskId, user from record_day where moduleId=%s group by taskId, user) a group by taskId \
        ) r \
        on t.id=r.taskId where t.moduleId=%s", [mid, mid]
    if create_user != '': 
        sql += " and createUser=%s"
        params.append(create_user)
    if category != '': 
        sql += " and category=%s"
        params.append(category)
    if department != '': 
        sql += " and department=%s"
    sql += " order by createTime, status desc"
    
    data = db.read_all(sql, params)
    for line in data: 
        line['planEndTime'] = str(line['planEndTime'])
        line['createTime'] = str(line['createTime']) 
    
    return data
    
    
if __name__ == '__main__':
    # create_task(1, 1, 'david', '任务1', True, "2020-11-12", "HelloKetty")
    print(get_task_list(1, "", "", ""))
    
    pass