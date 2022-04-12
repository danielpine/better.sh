from tools.PySqlTemplate import DataSource, DBTypes, PySqlTemplate
import os
import uuid
import sys
sys.path.append("..")
sys.path.append(".")


def generateAccessToken():
    return ''.join(str(uuid.uuid4()).split('-'))


def setupDataSource():
    PySqlTemplate.set_data_source(
        DataSource(
            dbType=DBTypes.MySql,
            user='root',
            password='root',
            ip='127.0.0.1',
            port=3306,
            db='better')
    )


def routeScan(folder):
    for _ in os.listdir(folder):
        if os.path.splitext(_)[1] == '.py':
            file = _.split('.')[0]
            __import__(folder+'.'+file)
