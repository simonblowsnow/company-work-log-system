#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''
from datetime import datetime
from src.libs.database import Database
from src.common.base import Task


def create_task(project_id, module_id, create_user, name, is_multi, plan_end_time, description=""):
    m = Task(project_id, module_id, None)
    m.set_data(is_multi, name, create_user, description, plan_end_time)
    flag = m.create()
    return flag if flag != -1 else False

'''TODO：兼容凌晨提交日志情况'''
def is_today(tm):
    return tm.strftime('%Y-%m-%d') == datetime.now().strftime('%Y-%m-%d')


'''
进度控制：本日进度不能小于历史进度，但可修改计划
进度说明：
        一、非协作任务：
            1.若有最新变更记录（变更后个人未提交过日志），则以记录中进度值为最小值；
            2.若无最新变更记录，则以个人历史最后记录为最小值，无记录则为0；
        二、协作任务：
            1）若有最新变更记录（变更后协作的人均未提交过日志），则以记录中进度值为最小值；
            2）若无最新变更记录：
            1.若当日有人提交过记录，则以此值为最终值，不可编辑；
            2.若当日无人提交过记录，则以个人历史最后记录为最小值，无记录则为0；
    二次修改：
        是否协作任务的逻辑可以统一，以任务为导向，不管人

'''        
def get_task_control(t_id, user=None, db=None):
    if not db: db = Database()
    
    '''取任务下所有人的最后提交记录'''
    sqlR = '''select r.user, updateTime, progress from record_day r right join (
        select max(updateTime) tm from record_day where taskId=%s
    ) a on r.updateTime=a.tm where taskId=%s order by progress desc limit 1
    '''
    '''取任务下的最新变更记录'''
    sqlP = '''select a.executor, updateTime, progress, multiUser from plan_change a right join 
          (select max(updateTime) tm from plan_change b where taskId=%s) b
        on a.updateTime=b.tm where taskId=%s order by progress limit 1  
    '''
    rec = db.selectLine(sqlR, (t_id, t_id))
    pla = db.selectLine(sqlP, (t_id, t_id))
    
    '''逻辑说明：
        1.无计划变更则以最后提交为准，无则为0
        2.有计划变更则以最新时间对应的进度为准
        注：提交时需检查进度合法性
        progress - 是否协作任务且今日已由其他人设置。
        注：若有最新计划变更，则协作任务不受其他成员今日进度限制
    '''
    info = {'min': 0, 'progress': None}
    if rec:
        ru, rt, rp = rec
        info['min'] = rp
        '''今日他人已设置'''
        if user != ru and is_today(rt): info['progress'] = rp
        '''有计划则看时间'''
        if pla and pla[1] > rt: info['min'], info['progress'] = pla[2], None  
    else:
        '''无提交但有计划变更，则以计划为准'''
        if pla: info['min'] = pla[2] 
    '''End If'''
    
    return info
   
   
def get_task_list(mid, create_user, category, department):
    db = Database()
    keys = ['id', 'name', 'moduleId', 'createUser', 'status', 'executor', 'createTime', 'description',
            'category', 'department', 'mark', 'progress', 'planEndTime', 'multiUser']
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
    sql += " order by updateTime, status desc"
    
    data = db.read_all(sql, params)
    for line in data: 
        line['planEndTime'] = str(line['planEndTime'])
        line['createTime'] = str(line['createTime']) 
    
    return data


def add_change(user, t_id, plan_time, progress, reason):
    db = Database()
    '''获取任务基本信息'''
    sql = "select planEndTime, multiUser from task where id=%s"
    cnx, cursor = db.Query(sql, (t_id, ))
    src_time, multi_user = cursor.fetchone()
    
    '''获取历史变更信息'''
    sql = "select id, executor, createTime from plan_change where taskId=%s order by createTime desc limit 1 for update"
    cursor = db.select(sql, (t_id, ))
    line = cursor.fetchone()
    flag = True  
    
    if line:
        _, executor, tm = line
        '''协同任务或该用户已提交计划未执行'''
        if multi_user or executor == user: 
            sql = "select count(*) from record_day where taskId=%s and workday>%s "
            db.select(sql, (t_id, tm), cursor)
            count = cursor.fetchone()[0]
            if count == 0: flag = False
        '''End If 2'''
    '''End If 1'''
             
    '''有已更改的计划暂未实施，不能新增'''
    if not flag: 
        cursor.close()
        return False, "该任务有已更改的计划暂未实施，不能新增''"
    
    sql = "insert into plan_change (taskId, srcTime, planTime, changeUser, executor, progress, reason, multiUser) \
        values (%s, %s, %s, %s, %s, %s, %s, %s)"
    params = (t_id, src_time, plan_time, user, user, progress, reason, multi_user)
    flag, _ = db.Transaction([[sql, params]], cnx, cursor)
    
    return flag, "操作失败"
    
    

    
if __name__ == '__main__':
#     create_task(1, 1, 'david', '任务1', True, "2020-11-12", "HelloKetty")
#     print(get_task_list(1, "", "", ""))
#     get_task_record(1, "admin")
#     print(add_change("admin", 1, "2020-10-31", 32, "啊大大"))
#     print(get_task_record(1, 1, ""))
    get_task_control(2)
    
    pass
