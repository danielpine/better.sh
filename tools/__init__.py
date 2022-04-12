import json
from tools.PySqlTemplate import DataSource, DBTypes, PySqlTemplate
import os
import uuid
import sys

from tools.common import getPythonDataBase
sys.path.append("..")
sys.path.append(".")


def generateAccessToken():
    return ''.join(str(uuid.uuid4()).split('-'))


def setupDataSource():
    conf = {}
    with open('conf/app.json', "r", encoding="utf-8") as f:
        conf = json.loads(f.read())
    PySqlTemplate.set_data_source(
        DataSource(
            dbType=DBTypes.MySql,
            user=conf['user'],
            password=conf['password'],
            ip=conf['ip'],
            port=conf['port'],
            db=conf['db'])
    )


def routeScan(folder):
    for _ in os.listdir(folder):
        if os.path.splitext(_)[1] == '.py':
            file = _.split('.')[0]
            __import__(folder+'.'+file)
