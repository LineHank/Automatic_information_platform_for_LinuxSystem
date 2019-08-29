from flask import Flask, request, jsonify,g
import json
import pymysql.cursors
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app, supports_credentials=True) # 用于处理跨域问题


@app.route('/add/student/', methods=['post'])
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    student = request.data
    print(type(student))
    student = request.data.decode('utf-8')
    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定

    print(student)
    print(type(student))
    student_json = json.loads(student)
    # 把区获取到的数据转为JSON格式。
    return jsonify(student_json)
    # 返回JSON数据。

def do_the_login(username,password):
    if username =='' or password=='':
        msg = 'username or password is error'
    else:
        username = username
        password = password
        msg = 'welcome %s to join us' % username
    return msg

def show_the_login_form():
    return 'username = %s,password =%s ' % (g.username,g.password)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method ==  'POST ':
        data = request.get_data()
        print("data = %s" % data)
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)
        username = json_data.get("username")
        password = json_data.get("password")
        print("request.form = %s" % request.form)
        print("request.values = %s" % request.values)
        print('username = %s , password =%s' % (username,password))
        msg = do_the_login(username,password)
    else:
        msg = show_the_login_form()
    return msg



if __name__ == '__main__':
    app.run()
    # 这里指定了地址和端口号。