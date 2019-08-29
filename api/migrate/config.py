DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'howe'
PASSWORD = '1224'
HOST = '192.168.150.8'
PORT = '3306'
DATABASE = 'system_information'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False