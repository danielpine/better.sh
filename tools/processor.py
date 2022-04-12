from functools import reduce
import json
import sys
sys.path.append("..")
sys.path.append(".")
import os
from tools import setupDataSource
from tools.PySqlTemplate import PySqlTemplate
setupDataSource()
with open('estates.json', "r", encoding="utf-8") as f:
    es = json.loads(f.read())
    print(es)
    for i in es:
        print(i)
        PySqlTemplate.save(
            'insert into estate(name,lane) values(?,?)', i['name'], i['lane'])
# for filename in os.listdir(r'data'):
#     with open('data/'+filename, "r", encoding="utf-8") as f:
#         print(filename[:-4])
#         es = f.read().split('，')
#         fnl = [str.strip, str]
#         es = [reduce(lambda v, f: f(v), fnl, element) for element in es]
#         for name in es:
#             PySqlTemplate.save(
#             'insert into record(name,mark_date,year) values(?,?,?)', name, filename[:-4],'2022')
