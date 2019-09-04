from models.exts import db
import json

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
    ping = db.Column(db.String(100), nullable=True)
    tableState = db.Column(db.String(100), nullable=True)
    def to_json(self):
        json_data = {
            'id': self.id,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'cpu': self.cpu,
            'memory': self.memory,
            'disk': self.disk,
            'cpu_rate': self.cpu_rate,
            'and32_64': self.and32_64,
            'information': self.information,
            'pci': self.pci,
            'tableState': self.tableState,
            'ping': self.ping,
        }
        return json_data

    def __repr__(self):
        return '<Os_infotmation %r>' % self.ip

# 原因就是因为app.run(debug=True)。开启debug模式之后，当我们修改代码的时候，比如将删除表和创建表这两句话注释，然后打开插入数据的注释。这个过程debug模式默认就已经把程序运行一遍了。此时数据库就已经有了数据，当我们再次手动执行的时候，又往数据库中插入了一条数据，这时候就会报错。因为字段的约束是唯一性的unique，所以解决的办法有两种：
#
# 第一种：就是不要将删除表和创建表这两句话注释，每次执行都要带着这两个句话。无论是debug模式自动执行还是我们手动执行程序，都会先删除表然后再创建表，所以执行多少次都不怕。
#
# 第二种：关闭debug模式。就是这样app.run()