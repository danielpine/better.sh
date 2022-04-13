import sys
sys.path.append("..")
sys.path.append(".")
from requests_html import HTMLSession, HTMLResponse
from base64 import encode
from tools.PySqlTemplate import PySqlTemplate
from tools import setupDataSource
import os
from functools import reduce
import json

setupDataSource()
c = []


def put(date, url):
    session = HTMLSession()
    site: HTMLResponse = session.get(url)
    collect = site.html.find('span')
    for item in collect:
        if len(item.text) > 2 and (item.text[-1] == '、' or item.text[-1] == '。') and '已对相关' not in item.text and '共话松江' not in item.text:
            name = item.text.replace('、', '').replace('。', '').strip()
            if name:
                print(name)
                # PySqlTemplate.save(
                #     'delete from record where name=? and mark_date=? and year=?', name, date, '2022')
                try:
                  PySqlTemplate.save(
                    'insert into record(name,mark_date,year) values(?,?,?)', name, date, '2022')
                except:
                  print('error when:'+name)    
#https://mp.weixin.qq.com/s/vxFiV2HeSvByINUlTmFKZA
urls = [
    ['0411', 'https://mp.weixin.qq.com/s/XVA8da4v3i0CJ0t8f6ZaKg'],
    ['0410', 'https://mp.weixin.qq.com/s/y_y2RIhbhTx_zM4MQkR_CQ'],
    ['0409', 'https://mp.weixin.qq.com/s/w4sBIrT9jYpvNd4QwpHLYQ'],
    ['0408', 'https://mp.weixin.qq.com/s/N5tX--wqy85Yj8mw6Npq2A'],
    ['0407', 'https://mp.weixin.qq.com/s/pN7llD6zUb_JhbPJyrycCw'],
    ['0406', 'https://mp.weixin.qq.com/s/A9856_EBJbS7HglBdzpx_Q'],
    ['0405', 'https://mp.weixin.qq.com/s/DXo-ykIKyI_-M49MXDn-nA'],
    ['0404', 'https://mp.weixin.qq.com/s/BEjy3EvnAyuhWwrTWNLYww'],
    ['0403', 'https://mp.weixin.qq.com/s/fosWdIhNo_ySJALqrsi-LQ'],
    ['0402', 'https://mp.weixin.qq.com/s/5eJADzttDwjfE4ccfIJeuQ'],
    ['0401', 'https://mp.weixin.qq.com/s/FFElOoGAJt7g-AIA-ly69Q'],
    ['0331', 'https://mp.weixin.qq.com/s/XMQUidxOC1CAFPafcUCRqw'],
    ['0330', 'https://mp.weixin.qq.com/s/cFu4kcRqxPLzYD0-5aj98g'],
    ['0429', 'https://mp.weixin.qq.com/s/ByMvOR93IDt4dx6s_rU6pg'],
    ['0428', 'https://mp.weixin.qq.com/s/aRVkrEVK-qExmh6SUIeKiQ'],
]
if __name__ == '__main__':
    for a in urls:
        put(a[0], a[1])
        print(a[0], a[1])
