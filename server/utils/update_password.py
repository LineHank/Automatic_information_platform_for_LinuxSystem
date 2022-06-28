# -*- coding: utf-8 -*-
# pip install paramiko
# pip install xlrd==1.2.0
# 使用paramiko 修改密码 （此脚本只适合改密码  因为改密码需要二次确认）
# 使用paramiko 修改密码 （）
import os
import platform
import sys
import time
import paramiko
import xlrd


def update_password(ip, username, password, new_password):
    """
        用于修改密码
    :param ip:
    :param username:
    :param password:
    :param new_password:
    :return:
    """
    stdin = None
    stdout = None
    stderr = None
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(ip, username=username, password=password, port=22)

    ssh_c = ssh.invoke_shell()

    time.sleep(0.1)
    # 先判断提示符，然后下一步在开始发送命令，这样大部分机器就都不会出现问题
    buff = ''
    while not buff.endswith('# '):
        if buff.endswith(' '):
            break
        resp = ssh_c.recv(9999)
        buff += resp.decode('utf8')
        time.sleep(0.1)
    ssh_c.send('export LANG=en_US.UTF-8 \n export LANGUAGE=en \n')  # 解决错误的关键，编码问题
    # ssh_c.send('export LANG=en_US.UTF-8 \n export LANGUAGE=en \n su - \n')  # 解决错误的关键，编码问题
    # buff = ''
    # while not buff.endswith('Password: '):  # true
    #     resp = ssh_c.recv(9999)
    #     buff += resp.decode('utf8')
    # ssh_c.send(password + '\n')
    buff = ''
    while not buff.endswith('# '):
        resp = ssh_c.recv(9999)
        buff += resp.decode('utf8')
        if buff.endswith(' '):
            break
        if 'failure' in buff:
            stderr = buff
            print({'stdin': stdin, 'stdout': stdout, 'stderr': stderr})
    command = 'sudo passwd %s' % username + '\n'
    ssh_c.send(command)  # 放入要执行的命令
    print('running %s' % command)

    buff = ''
    while not buff.endswith('password: '):  # true
        time.sleep(1)
        resp = ssh_c.recv(9999)
        buff += resp.decode('utf8')
    ssh_c.send(new_password + '\n')

    buff = ''
    while not buff.endswith('password: '):  # true
        time.sleep(1)
        resp = ssh_c.recv(9999)
        buff += resp.decode('utf8')
    ssh_c.send(new_password + '\n')

    buff = ''
    while not buff.endswith('# '):
        time.sleep(1)
        # 接收到服务器返回值
        if ssh_c.recv_ready():
            stdout = ssh_c.recv(9999).decode('utf-8')
            buff = stdout
        if ssh_c.recv_stderr_ready():
            stderr = ssh_c.recv_stderr(9999).decode('utf-8')
            print({'stdin': stdin, 'stdout': stdout, 'stderr': stderr})
        if buff.endswith(' '):
            break

    stdin = command
    return {'stdin': stdin, 'stdout': stdout, 'stderr': stderr}


def cmd(ip, username, password, new_password):
    """
        执行命令
    :param ip:
    :param username:
    :param password:
    :param new_password:
    :return:
    """
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(ip, username=username, password=password, port=22)
    stdin, stdout, stderr = ssh.exec_command('sudo passwd %s %s' % (username, new_password))
    result = stdout.read().decode('utf8')
    error = stderr.read().decode('utf8')
    print({'result': result, 'error': error})


if __name__ == '__main__':
    print({'file is :': sys.argv[1]})
    result = os.popen('pip list')
    res = result.read()
    for package in ['paramiko', 'xlrd']:
        if package not in res:
            os.popen('pip install paramiko')
            os.popen('pip install xlrd==1.2.0')
    if len(sys.argv) < 2:
        print('请传入excel文件名 包含后缀')
        raise Exception
    local_dir = os.path.dirname(os.path.abspath(__file__))
    local_file = '%s/%s' % (local_dir, sys.argv[1])
    if not os.path.isfile(local_file):
        if platform.system() == 'Windows':
            local_file = local_file.replace('\\', '\\')
    import_file = sys.argv[1]
    _file_type = import_file[::-1].split('.')[0][::-1]
    if _file_type not in ['xls', 'xlsx']:
        print('上传失败，请上传 .xls 或 .xlsx 类型的文件！')
        raise Exception
    workbook = xlrd.open_workbook(local_file)
    book_sheet = workbook.sheet_by_index(0)
    n_rows = book_sheet.nrows
    # 检查导入的execl数据头信息
    standard_headers = {0: 'ip', 1: 'username', 2: 'password', 3: 'new_password'}
    for _index, _standard_header in standard_headers.items():
        if book_sheet.row_values(0)[_index] == _standard_header:
            continue
        print('第 %s 列的第一行标题有误 %s' % (_index, _standard_header))
        raise Exception

    # file = open('%s/%s' % (local_dir, 'update_password_result.log'), 'w+')
    # file.write('IP\t原密码\t新密码\t成功标识\t异常原因\n')
    with open('%s/%s' % (local_dir, 'update_password_result.log'), 'w+', encoding="utf-8") as f:
        f.write('IP\t原密码\t新密码\t成功标识\t异常原因\n')
        for _index in range(n_rows):
            if _index == 0:
                continue
            row_data = book_sheet.row_values(_index)
            ip = str(row_data[0]).strip()
            username = str(row_data[1]).strip()
            password = str(row_data[2]).strip()
            new_password = str(row_data[3]).strip()
            info = {
                'ip': ip,
                'username': username,
                'password': password,
                'new_password': new_password,
            }
            print(info)
            try:
                rsp = update_password(**info)
                if rsp['stderr']:
                    f.write('{ip}\t{password}\t{new_password}\t{status}\t{abnormal}\n'.
                            format(ip=ip, password=password, new_password=new_password, status=0, abnormal=rsp['stderr']))
                f.write(
                    '{ip}\t{password}\t{new_password}\t{status}\n'.
                        format(ip=ip, password=password, new_password=new_password, status=1))
            except Exception as error:
                f.write(
                    '{ip}\t{password}\t{new_password}\t{status}\t{abnormal}\n'.
                        format(ip=ip, password=password, new_password=new_password, status=0,  abnormal=error))
                print({'error': error})
