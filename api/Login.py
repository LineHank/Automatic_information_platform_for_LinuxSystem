# -*- coding: utf-8 -*-

import pymysql.cursors
from flask import Flask, request, session, redirect, url_for, render_template, make_response, jsonify
from flask_cors import CORS
app = Flask(__name__)
app.debug = True
CORS(app, supports_credentials=True) # 用于处理跨域问题

# token加密解密

@app.route('/index')
def index():
    token = request.headers.get('token')
    if token:
        return jsonify({'code': 200, 'data': {'love': 'lp'}})
    return jsonify({'code': 400})



@app.route('/register', methods=('POST', ))
def register():
    ip = request.json.get('ip')
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password and ip:
        # 连接数据库
        connection = pymysql.connect(host='192.168.150.8', port=3306, user='howe', password='1224', db='system_information', charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # 插入数据
        insertSql = "INSERT INTO `os_information` (`ip`, `name`,`password`) VALUES ( '"+ip + "','" + username + "','" + password + "')"
        print(insertSql)
        cursor.execute(insertSql)
        # 提交
        connection.commit()
        return  jsonify({'code': 200})
    return jsonify({'code': 400})





if __name__ == '__main__':
    app.run(debug=True)
