import paramiko

ssh = paramiko.SSHClient()  # 创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
ssh.connect(hostname='192.168.150.8', port=22, username='howe', password='1224')  # 连接服务器

stdin, stdout, stderr = ssh.exec_command("dmidecode |grep -A16 'Memory Device$'|grep Size|grep -v No")  # 执行命令并获取命令结果
# stdin为输入的命令
# stdout为命令返回的结果
# stderr为命令错误时返回的结果
res, err = stdout.read(), stderr.read()
result = res if res else err
print(result.decode('utf-8'))
print(type(result.decode('utf-8')))
ssh.close()  # 关闭连接