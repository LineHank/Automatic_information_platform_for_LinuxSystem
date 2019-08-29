from flask import Flask, request, session, redirect, url_for, render_template, make_response, jsonify,g
import json
import pymysql.cursors
from flask_cors import CORS
from conf import config
import paramiko
import time

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


def check():
    # 默认返回内容
    return_dict = {'code': '200', 'msg': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

def get_Linux_information(id,ip,username,password):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    register_information_get()[0]['username']
    # 连接服务器
    ssh.connect(hostname=ip, port=22, username=username, password=password)
    cmd = 'getconf LONG_BIT'
    # cmd = 'ls -l;ifconfig'       #多个命令用;隔开
    stdin, stdout, stderr = ssh.exec_command(cmd)#stdin为输入的命令  stdout为命令返回的结果  stderr为命令错误时返回的结果
    res, err = stdout.read(), stderr.read()
    result = res if res else err

    #获取CPU型号
    stdin, stdout, stderr = ssh.exec_command('cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c ')
    res, err = stdout.read(), stderr.read()
    cpu_in = res if res else err

    # 获取内存  dmidecode |grep -A16 "Memory Device$"|grep Size|grep -v No             cat /proc/meminfo |grep MemTotal
    stdin, stdout, stderr = ssh.exec_command('cat /proc/meminfo |grep MemTotal')
    res, err = stdout.read(), stderr.read()
    memory_in = res if res else err

    # 获取硬盘空间大小   df -lh | grep sda | awk '{print $2}'
    stdin, stdout, stderr = ssh.exec_command("df -lh | grep sda | awk '{print $2}'")
    res, err = stdout.read(), stderr.read()
    disk_in = res if res else err


    #CPU可用率 top -bn 1 -i -c | grep "id" | awk '{print $8}'
    stdin, stdout, stderr = ssh.exec_command("top -bn 1 -i -c | grep id | awk '{print $8}'")
    res, err = stdout.read(), stderr.read()
    cpu_rate_in = res if res else err

    #32或64   getconf LONG_BIT
    stdin, stdout, stderr = ssh.exec_command('getconf LONG_BIT')
    res, err = stdout.read(), stderr.read()
    and_32_64_in = res if res else err

    #获取发行版  cat /etc/redhat-release
    stdin, stdout, stderr = ssh.exec_command('cat /etc/redhat-release')
    res, err = stdout.read(), stderr.read()
    information_in = res if res else err

    # 获取PCI lspci | grep bridge | head -n 4
    stdin, stdout, stderr = ssh.exec_command('lspci | grep bridge | head -n 1')
    res, err = stdout.read(), stderr.read()
    pci_in = res if res else err
    ssh.close()  # 关闭连接

    # 连接数据库
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db('system_information')
    # 创建游标
    cursor = conn.cursor()
    # 插入数据
    cursor.execute("update os_information set cpu='"+cpu_in.decode('utf-8')+"',memory='"+ memory_in.decode('utf-8')+"',disk='" + disk_in.decode('utf-8') +"',cpu_rate='" + cpu_rate_in.decode('utf-8')+"',and32_64='"+and_32_64_in.decode('utf-8')+"',information='"+information_in.decode('utf-8')+"',pci='"+pci_in.decode('utf-8')+"'where id='"+id+"'")
    conn.close()
    return result

# register添加数据进myslq数据库
def register_mysql(ip,username,password):
    # 连接数据库
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db('system_information')
    # 创建游标
    cursor = conn.cursor()
    # 插入数据
    cursor.execute("INSERT INTO `os_information` (`ip`, `username`,`password`,`tableState`) VALUES ( '"+ip + "','" + username+ "','" + password + "','" + "更新" + "')")
    # print('total records:', cursor.rowcount)
    # result = cursor.fetchall()
    conn.close()
    # return result[0]

#获取数据库信息
def register_information_get():
    conn = pymysql.connect(**config)
    conn.autocommit(1)
    conn.select_db('system_information')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM os_information')
    # print('total records:', cursor.rowcount)
    result = cursor.fetchall()
    conn.close()
        # get_Linux_information("41",r['ip'],r['username'],r['password'])
        # get_Linux_information('41','192.168.150.8','howe','1224')
    return result


@app.route('/register', methods=('POST',))
def register():
    check()
    ip = request.json.get('ip')
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password and ip:
        register_mysql(ip,username,password)
        return jsonify({'code': 200})
    return jsonify({'code': 400})

@app.route('/register_get', methods=('GET',))
def register_get():
    check()
    return json.dumps(register_information_get(), ensure_ascii=False)

@app.route('/register_update', methods=('GET',))
def register_update():
    check()
    mysql_result = register_information_get()
    for r in mysql_result:
        print(r["id"], type(str(r["id"])))
        get_Linux_information(str(r['id']), r['ip'], r['username'], r['password'])
    return json.dumps(register_information_get(), ensure_ascii=False)














if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
    # 这里指定了地址和端口号。