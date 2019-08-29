from exts import db

# flask_migrate相关的命令：
# python manage.py db init：初始化一个迁移脚本的环境，只需要执行一次。
# python manage.py db migrate：将模型生成迁移文件，只要模型更改了，就需要执行一遍这个命令。
# python manage.py db upgrade：将迁移文件真正的映射到数据库中。每次运行了migrate命令后，就记得要运行这个命令。
# 表名要放在manage里面


class Os_infotmation(db.Model):
    __tablename__ = 'os_information'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cpu = db.Column(db.String(100), nullable=True)
    memory = db.Column(db.String(100), nullable=True)
    disk = db.Column(db.String(100), nullable=True)
    cpu_rate = db.Column(db.String(100), nullable=True)
    and32_64 = db.Column(db.String(100), nullable=True)
    information = db.Column(db.String(100), nullable=True)
    pci = db.Column(db.String(100), nullable=True)
    tableState = db.Column(db.String(100), nullable=True)

