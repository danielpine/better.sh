# import sys

# from tools.common import extract
# sys.path.append("..")
# sys.path.append(".")
# import datetime
# from requests_html import HTMLSession, HTMLResponse
# from base64 import encode
# from tools.PySqlTemplate import PySqlTemplate
# from tools import setupDataSource
# import os
# from functools import reduce
# import json

# setupDataSource()
# state = '@小区:怡东@小区:白杨@地址:浦东@地址:古楼'

# fields = extract(state)
# if '小区' in fields:
#     ['%'+'%'.join(st)+'%' for st in fields['小区']]
#     pass

# countSql = '''SELECT count(*) FROM  estate  where name like ? or lane like ?'''

# total = PySqlTemplate.count(countSql)
# page = PySqlTemplate.findList(
#     ''' SELECT e.*, r.mark_date, r.`name` AS pubname FROM ( SELECT * FROM estate WHERE NAME LIKE ? OR lane LIKE ? ORDER BY NAME LIMIT ?,? ) e LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0 and r.district=e.district where r.mark_date>=? ORDER BY e.NAME''', state, state, (int(
#         current)-1)*int(pageSize), int(pageSize), dd
# )