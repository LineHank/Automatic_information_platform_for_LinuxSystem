# result_list.append(
#             {'id': id, 'ip': ip, 'username': username, 'password': password, 'cpu': cpu_in, 'memory': memory_in,
#              'disk': disk_in, 'cpu_rate': cpu_rate_in, 'and32_64': and_32_64_in, 'information': information_in,
#              'pci': pci_in})
#!/usr/bin/python
# -*- coding:utf-8 -*-

import paramiko
import sys
import getpass
import threading
import os
result_list=[]


def auth(func):
    def wrapper(*args, **keargs):
        for n in range(3):
            try:
                res = func(*args, **keargs)
                return res
            except Exception as e:
                if n < 1:
                    # print('%s\tError\t%s' % (args[0], e))
                    # os = Os_infotmation.query.filter(Os_infotmation.id == args[0]).first()
                    # os.ping = "用户或密码错误"
                    print(str(args[0])+'输入用户密码错误请重新输入！')
                    result_list.append(
                        {'id': str(args[0]), 'ping':"用户或密码错误"})
                else:
                    # print('%s\tError\t%s' % (args[0], e))
                    res = bytes('\033[0;31m主机登陆失败，继续下一主机\033[0m', encoding='utf-8')
                    return res

    return wrapper

def get_message(os):
    @auth
    def rcmd(id, ip, username, password):
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 把要连接的机器添加到known_hosts文件中
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(ip, username=username, password=password, port=22)

        # 获取CPU型号
        stdin, stdout, stderr = ssh.exec_command('cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c ')
        cpu_in = stdout.read().decode('utf8')
        error = stderr.read().decode('utf8')

        # 获取内存  dmidecode |grep -A16 "Memory Device$"|grep Size|grep -v No             cat /proc/meminfo |grep MemTotal
        stdin, stdout, stderr = ssh.exec_command('cat /proc/meminfo |grep MemTotal')
        memory_in = stdout.read().decode('utf8')
        error = error + stderr.read().decode('utf8')

        # 获取硬盘空间大小   df -lh | grep sda | awk '{print $2}'
        stdin, stdout, stderr = ssh.exec_command("df -lh | grep sda | awk '{print $2}'")
        disk_in = stdout.read().decode('utf8')
        eerror = error + stderr.read().decode('utf8')

        # CPU可用率 top -bn 1 -i -c | grep "id" | awk '{print $8}'
        stdin, stdout, stderr = ssh.exec_command("top -bn 1 -i -c | grep id | awk '{print $8}'")
        cpu_rate_in = stdout.read().decode('utf8')
        error = error + stderr.read().decode('utf8')

        # 32或64   getconf LONG_BIT
        stdin, stdout, stderr = ssh.exec_command('getconf LONG_BIT')
        and_32_64_in = stdout.read().decode('utf8')
        error = error + stderr.read().decode('utf8')

        # 获取发行版  cat /etc/redhat-release
        stdin, stdout, stderr = ssh.exec_command('cat /etc/redhat-release')
        information_in = stdout.read().decode('utf8')
        error = error + stderr.read().decode('utf8')

        # 获取PCI lspci | grep bridge | head -n 4
        stdin, stdout, stderr = ssh.exec_command('lspci | grep bridge | head -n 1')
        pci_in = stdout.read().decode('utf8')
        error = error + stderr.read().decode('utf8')
        ssh.close()
        result_list.append(
            {'id': id, 'ip': ip, 'username': username, 'password': password, 'cpu': cpu_in, 'memory': memory_in,
             'disk': disk_in, 'cpu_rate': cpu_rate_in, 'and32_64': and_32_64_in, 'information': information_in,
             'pci': pci_in,'ping':"Linux信息已更新"})
    results=[]
    threads = []
    for r in os:
        results.append(r.to_json())
    for r in results:
        threads.append(threading.Thread(target=rcmd, args=(r["id"],r["ip"],r["username"],r["password"])))
    for t in threads:
        t.start()
        print(t.name)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")
    return result_list