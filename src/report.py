#coding: utf8
'''
==================================================================================
Created on 2020-10-26
Author: Simon
==================================================================================
'''

from datetime import datetime, timedelta
from src.libs.database import Database


def is_today(tm): return str(datetime.now())[:10] == str(tm)[:10]
def pre_days(count=7):
    return str(datetime.now() - timedelta(days = count))[:10]
def f(d): return d if d else ""


def list_report_day(user=None, department=None):
    r = Report()
    return r.list_report_day(user, department)



class Report():
    def __init__(self):
        pass
    
    '''获取近七天日报'''
    def list_report_day(self, user=None, department=None):
        records = self._list_report_day("record", user, department)
        plans = self._list_report_day("plan", user, department)
        
        dts = {}
        for workday, rs in records.items():
            if workday not in dts: 
                dts[workday] = {'workday': workday, "plan": "", "pcount": 0}
            dts[workday]['record'] = self.collect_day(rs, "record")
            dts[workday]['rcount'] = len(rs)
            
        for workday, ps in plans.items():
            if workday not in dts: continue
            dts[workday]['plan'] = self.collect_day(ps, "plan")
            dts[workday]['pcount'] = len(ps)
        
        print(dts)
        lines = sorted(dts.values(), key=lambda x:x["workday"], reverse=True)
        print(lines)
        
        return lines 

    
    '''完成内容 & 计划通用过程·从数据库获取记录'''
    def _list_report_day(self, key="record", user=None, department=None):
        db = Database()
        table = "record_day" if key == "record" else "plan_day"
        params = [pre_days(), pre_days(-1)]
        sql = '''select user, workday, project, module, task, content,
            r.progress progress, r.category category, planEndTime from {} r 
            left join task t on t.id=r.taskId 
            where workday between %s and %s'''.format(table)
        if user:
            sql += " and user=%s"
            params.append(user)
        if department:
            sql += " and user in (select username from user where orgId=%s)"
            params.append(department)
        res = db.read_all(sql, params)
        '''按天归类'''
        dts = {}
        for d in res:
            day = str(d['workday'])[:10]
            if day not in dts: dts[day] = []
            dts[day].append(d)
        '''End For'''
        
        return dts

    '''将一天的日志汇总并格式化'''
    def collect_day(self, records, key="record"):
        projects = {}
        '''按项目汇总'''
        for d in records:
            pj = d['project'] if d['project'] else "其它" 
            if pj not in projects: projects[pj] = []
            line = "%s.%s；" % (len(projects[pj]) + 1, format_report(d, key))
            projects[pj].append(line)
            
        content = ""
        for name, vs in projects.items():
            content += "[%s]<br>%s" % (name, "<br>".join(vs))
        
        return content

'''-----------------------------------End Class------------------------------'''    

def format_report(line, key="record"):
    if key == "record": return format_record(line)
    if key == "plan": return format_plan(line)

'''计划格式化过程'''
def format_plan(line):
    p, m = int(line['progress']), f(line['module'])
    main = m + ('' if m=='' else '-') + line['task']
    plan = "，预计完成{}%".format(p)
    return main + plan
    
'''日志格式化核心过程'''    
def format_record(line):    
    if not line['planEndTime']: line['planEndTime'] = datetime.now() 
    p, ptm = int(line['progress']), str(line['planEndTime'])[:10]
    m = f(line['module'])
    main = m + ('' if m=='' else '-') + line['task']
    plan = "，计划%s完成" % ("今日" if is_today(ptm) else ptm)
    prog = "，已完成" if p == 100 else "，完成{}%".format(p)
    '''具体工作细节'''
    detail = "" if f(line['content']) == "" else "<br>(%s)" % line['content']  
    return main + plan + prog + detail


# def report_day():
#     db = Database()
#
#







    



if __name__ == '__main__':
    d = list_report_day()
    
    # d = is_today(datetime.now())
    print(d)
    pass
