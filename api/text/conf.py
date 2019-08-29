#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql,os


# ============================ Global parameter ==============================
proDir = os.path.split(os.path.realpath(__file__))[0]
print(proDir)
xlsPath = os.path.join(proDir, 'testFile')
#============================ DB Config ==============================

config = {
    'host': '192.168.150.8',
    'port': 3306,
    'user': 'howe',
    'passwd': '1224',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}