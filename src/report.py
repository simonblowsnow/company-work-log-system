#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''

from datetime import datetime, timedelta
from src.libs.database import Database


def pre_days(count=7):
    return str(datetime.now() - timedelta(days = count))[:10]

def report_day():
    db = Database()
    

def f(d): return d if d else ""
def is_today(tm): return str(datetime.now())[:10] == str(tm)[:10]


def format_report(line):
    if not line['planEndTime']: line['planEndTime'] = datetime.now() 
    p, ptm = int(line['progress']), str(line['planEndTime'])[:10]
    m = f(line['module'])
    main = m + ('' if m=='' else '-') + line['task']
    plan = "，计划%s完成" % ("今日" if is_today(ptm) else ptm)
    prog = "，已完成" if p == 100 else "，完成{}%".format(p)  
    return main + plan + prog 


'''获取近七天日报'''
def list_report_day(user=None, department=None):
    db = Database()
    params = [pre_days(), pre_days(-1)]
    sql = '''select user, workday, project, module, task, r.progress progress, 
        r.category category, planEndTime from record_day r left join task t on t.id=r.taskId 
        where workday between %s and %s'''
    if user:
        sql += " and user=%s"
        params.append(user)
    if department:
        sql += " and user in (select username from user where orgId=%s)"
        params.append(department)
    res = db.read_all(sql, params)
    records = {}
    for d in res:
        day = str(d['workday'])[:10]
        pj = d['project'] if d['project'] else "其它" 
        if day not in records: records[day] = {}
        if pj not in records[day]: records[day][pj] = []
        line = "%s.%s；" % (len(records[day][pj]) + 1, format_report(d))
        records[day][pj].append(line)
    
    data = []
    for day, ps in records.items():
        rec = ""
        for name, vs in ps.items():
            rec += "[%s]<br>%s" % (name, "<br>".join(vs))
        line = {'workday': day, 'record': rec, 'plan': ''}
        data.append(line)
    
    return data




if __name__ == '__main__':
    d = list_report_day()
    
    # d = is_today(datetime.now())
    # print(d)
    pass
