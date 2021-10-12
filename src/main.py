#coding: utf8

import json
from flask import Flask, request, current_app, g
from flask_cors import *
from src.login import auth_required, web_login_common, login_out, get_auth_code
from src.config import Web as C
from src.libs.log import L
from src.common.response import NormalResponseJson, ErrorResponseJson, ErrorResponseData
import src.project as P
import src.module as M
import src.task as T
import src.record as RC


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'AreUOK'
app.config['TOKEN_EXPIRATION'] = 7200


@app.route('/')
def index():
    return "Welcome..."

'''验证码'''
@app.route('/securityCode')
def get_code():
    return get_auth_code(app)   

@app.route('/login', methods=['GET', 'POST'])    
def webLogin():
    '''Form field: username, password, securityCode, tms'''
    '''第二个参数传1则无需验证码'''
    return web_login_common(request, 1)

@app.route('/isLogin', methods=['GET', 'POST'])
@auth_required('lv0')
def is_login(user):
    L.info("User %s Request login status" % user)
    return NormalResponseJson({})

@app.route('/loginOut', methods=['GET', 'POST'])
@auth_required('lv0')    
def login_out(user):
    return login_out(user)

'''----------------------------------正式业务开始---------------------------------------'''
@app.route('/createProject', methods=['GET', 'POST'])
@auth_required('lv0')    
def _create_project(user, R):
    name = R.get('name', '')
    description = R.get('description', '')
    if name == '' or description == '': return ErrorResponseJson('项目名和描述不能为空！') 
    data = P.create_project(user, name, description) 
    
    if not data: return ErrorResponseJson('操作失败！')
    
    return NormalResponseJson({'id': data}) 

@app.route('/listProject', methods=['GET', 'POST'])
@auth_required('lv0')    
def _list_project(user, R):
    create_user = R.get('createUser', '')
    category = R.get('category', '')
    department = R.get('department', '')
    page = int(R.get('page', 0))
    size = int(R.get('page', 26))
    data = P.get_project_list(create_user, category, department, page, size)
    
    return NormalResponseJson(data)


@app.route('/createModule', methods=['GET', 'POST'])
@auth_required('lv0')    
def _create_module(user, R):
    pid = R.get('pid', '')
    name = R.get('name', '')
    description = R.get('description', '')
    if pid == "" or name == '' or description == '': return ErrorResponseJson('模块名和描述不能为空！') 
    data = M.create_module(pid, user, name, description)
    
    print(data)
    if not data: return ErrorResponseJson('操作失败，请检查是否填写完整！')
    
    return NormalResponseJson({'id': data}) 

@app.route('/listModule', methods=['GET', 'POST'])
@auth_required('lv0')    
def _list_module(user, R):
    pid = R.get('pid', '')
    create_user = R.get('createUser', '')
    category = R.get('category', '')
    department = R.get('department', '')
    
    data = M.get_module_list(pid, create_user, category, department)
    
    return NormalResponseJson(data)


@app.route('/createTask', methods=['GET', 'POST'])
@auth_required('lv0')    
def _create_task(user, R):
    pid = R.get('pid', '')
    mid = R.get('mid', '')
    name = R.get('name', '')
    multi = {'true': 1, 'false': 0}[R.get('multi')]
    plan_time = R.get('date')
    description = R.get('description', '')
    if mid == "" or name == '' or plan_time == '': return ErrorResponseJson('模块名和描述不能为空！')
    
    data = T.create_task(pid, mid, user, name, multi, plan_time, description)
    if not data: return ErrorResponseJson('操作失败，请检查是否填写完整！')
    
    return NormalResponseJson({'id': data}) 

@app.route('/listTask', methods=['GET', 'POST'])
@auth_required('lv0')    
def _list_task(user, R):
    pid = R.get('mid', '')
    category = R.get('category', '')
    department = R.get('department', '')
    
    data = T.get_task_list(pid, "", category, department)
    
    return NormalResponseJson(data)

@app.route('/getTaskControl', methods=['GET', 'POST'])
@auth_required('lv0')    
def _get_task_control(user, R):
    tid = R.get('tid', '')
    multi = int(R.get('multi'))
    
    data = T.get_task_control(tid, multi, user)
    
    return NormalResponseJson(data)

@app.route('/submitReport', methods=['GET', 'POST'])
@auth_required('lv0')    
def submit_report(user, R):
    params = R.get('params', '{}')
    data = json.loads(params, encoding="utf8")
    if not data: return ErrorResponseJson("参数错误")
    
    jobs = data.get('jobs', [])
    plans = data.get('plans', [])
    
    RC.submit_record(user, jobs, plans)
    
    # params
    
    # d = R.to_dict()
    
    
    # data = T.get_task_control(tid, multi, user)
    
    # for job in jobs:
    #     print(job)
    # print(plans)
    
    res = []
    return NormalResponseJson(res)


if __name__ == '__main__':
    L.info('server start on: %s !' % (C.PORT))
    app.debug=False
    app.run(host='0.0.0.0', port=C.PORT)

