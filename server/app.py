#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, session, redirect, url_for, render_template, make_response, jsonify,g
from models.exts import db
from flask_cors import CORS
import json
from models.system_informations import Os_infotmation
from utils import ping
from utils import ssh_message
import paramiko


app = Flask(__name__)
# 配置数据库的地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://howe:XXXX@192.168.150.8:3306/system_information'
# 跟踪数据库的修改，不建议开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
app.debug = True
CORS(app, supports_credentials=True) # 用于处理跨域问题

@app.route('/')
def hello_world():
    return 'Hello World!'

# token加密解密
@app.route('/index')
def index():
    token = request.headers.get('token')
    if token:
        return jsonify({'code': 200, 'data': {'love': 'lp'}})
    return jsonify({'code': 400})


def check():
    # 默认返回内容
    return_dict = {'code': '200', 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

def ping_inter_and_ssh():
    os = Os_infotmation.query.filter(Os_infotmation.tableState == "编辑").all()
    sult = ping.get_id(os)
    for s in sult:
        if s['result'] == "True":
            os2 = Os_infotmation.query.filter(Os_infotmation.ip == s['ip']).all()
            for o in os2:
                o.ping = '网络可用'
                db.session.commit()
        else:
            os2 = Os_infotmation.query.filter(Os_infotmation.ip == s['ip']).all()
            for o in os2:
                o.ping = '网络不可用'
                db.session.commit()
    os2 = Os_infotmation.query.filter(Os_infotmation.tableState == "编辑", Os_infotmation.ping == "网络可用").all()
    result_list = ssh_message.get_message(os2)
    for l in result_list:
        message = Os_infotmation.query.get(l["id"])
        if l["ping"] == "用户或密码错误":
            message.ping = l["ping"]
            db.session.commit()
        elif l["ping"] == "Linux信息已更新":
            message.ping = l["ping"]
            message.cpu = l["cpu"]
            message.memory = l["memory"]
            message.disk = l["disk"]
            message.cpu_rate = l["cpu_rate"]
            message.and32_64 = l["and32_64"]
            message.information = l["information"]
            message.pci = l["pci"]
            db.session.commit()

@app.route('/register', methods=('POST',))
def register():
    check()
    ip = request.json.get('ip')
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password and ip:
        s = Os_infotmation(ip=ip,username=username,password=password,tableState='编辑')
        db.session.add(s)
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code': 400})

@app.route('/update_delete', methods=('POST',))
def update_delete():
    check()
    id = request.json.get('id')
    if id:
        message = Os_infotmation.query.get(id)
        message.tableState = "删除"
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code': 400})


@app.route('/dialogdeicde_update', methods=('POST',))
def dialogdeicde_update():
    check()
    id = request.json.get('id')
    ip = request.json.get('ip')
    username = request.json.get('username')
    password = request.json.get('password')
    if id:
        message = Os_infotmation.query.get(id)
        message.ip=ip
        message.username=username
        message.password=password
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code': 400})

@app.route('/register_get', methods=('GET',))
def register_get():
    check()
    os = Os_infotmation.query.filter(Os_infotmation.tableState == "编辑").all()
    result = []
    for r in os:
        result.append(r.to_json())
    if result == "":
        return jsonify({'code': 400})
    else:
        return json.dumps(result, ensure_ascii=False)


@app.route('/register_update', methods=('GET',))
def register_update():
    check()
    ping_inter_and_ssh()     #查看网络和跑ssh
    os = Os_infotmation.query.filter(Os_infotmation.tableState == "编辑").all()
    result = []
    for r in os:
        result.append(r.to_json())
    if result == "":
        return jsonify({'code': 400})
    else:
        return json.dumps(result, ensure_ascii=False)

@app.route('/currentPage_pagesize', methods=('post',))
def currentPage_pagesize():
    check()
    currentPage = request.json.get('currentPage')
    pagesize = request.json.get('pagesize')
    os = Os_infotmation.query.filter(Os_infotmation.tableState == "编辑").paginate(int(currentPage),int(pagesize), False)
    result = []
    for r in os.items:
        result.append(r.to_json())
    if result == "":
        return jsonify({'code': 400})
    else:
        return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
    # 这里指定了地址和端口号。
