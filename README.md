# Automatic_information_platform_for_LinuxSystem
对多个Linux系统自动获取其系统信息的平台


首先现在本地或者Linux等系统上安装mysql数据库

进入server下运行以下命令
# flask_migrate相关的命令：
# python manage.py db init：初始化一个迁移脚本的环境，只需要执行一次。
# python manage.py db migrate：将模型生成迁移文件，只要模型更改了，就需要执行一遍这个命令。
# python manage.py db upgrade：将迁移文件真正的映射到数据库中。每次运行了migrate命令后，就记得要运行这个命令。
# 表名要放在manage里面
