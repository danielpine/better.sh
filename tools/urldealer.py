
import sys
sys.path.append("..")
sys.path.append(".")
import json
from functools import reduce
import os
from tools import setupDataSource
from tools.PySqlTemplate import PySqlTemplate
setupDataSource()
from base64 import encode
from requests_html import HTMLSession, HTMLResponse
import json
c = []

url = 'https://mp.weixin.qq.com/s/XVA8da4v3i0CJ0t8f6ZaKg'
date='0411'

session = HTMLSession()
site: HTMLResponse = session.get(url)
collect = site.html.find('span')

for item in collect:
    if 'style' in item.attrs and item.attrs['style'] == 'font-size: 16px;text-indent: 45px;':
        name = item.text.replace('、', '').replace('。', '').strip()
        if name:
            print(name)
            PySqlTemplate.save(
                    'insert into record(name,mark_date,year) values(?,?,?)', name, date, '2022')
