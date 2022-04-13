import sys
sys.path.append("..")
sys.path.append(".")
import datetime
from requests_html import HTMLSession, HTMLResponse
from base64 import encode
from tools.PySqlTemplate import PySqlTemplate
from tools import setupDataSource
import os
from functools import reduce
import json

setupDataSource()
c = []


def put(url):
    session = HTMLSession()
    site: HTMLResponse = session.get(url)
    title = site.html.find('.rich_media_title', first=True)
    s = '2022年'+title.text.split('（')[0]
    date = datetime.datetime.strftime(
        datetime.datetime.strptime(s.replace('【最新】',''), '%Y年%m月%d日'), r'%m%d')
    
    with open(date+'.html', "w", encoding="utf-8") as f:
        f.write(site.html.full_text)


urls = [
    'https://mp.weixin.qq.com/s/vxFiV2HeSvByINUlTmFKZA',
    'https://mp.weixin.qq.com/s/gQDyFLtdILP2NuSBgcjUxg',
    'https://mp.weixin.qq.com/s/gQDyFLtdILP2NuSBgcjUxg',
    'https://mp.weixin.qq.com/s/2VWTo6e9gmWJ0vxeZ4PhIw',
    'https://mp.weixin.qq.com/s/uj4TYASUn2YJZQMg2aUvdw',
    'https://mp.weixin.qq.com/s/MkKsQkgvUWbwj8z9jG_Zng',
    'https://mp.weixin.qq.com/s/djwW3S9FUYBE2L5Hj94a3A',
    'https://mp.weixin.qq.com/s/hnrGo4KvUvxhpjFyiE8-sQ',
    'https://mp.weixin.qq.com/s/K6jT1wRMSScBhvxcB2yV4g',
    'https://mp.weixin.qq.com/s/SSFVzOSXPTj-aLzR1tdtxw',
    'https://mp.weixin.qq.com/s/656rotFOMeDScnKSt6OmyQ',
    'https://mp.weixin.qq.com/s/OZGM-pNkefZqWr0IFRJj1g',
    'https://mp.weixin.qq.com/s/MkKsQkgvUWbwj8z9jG_Zng',
    'https://mp.weixin.qq.com/s/uj4TYASUn2YJZQMg2aUvdw',
    'https://mp.weixin.qq.com/s/2VWTo6e9gmWJ0vxeZ4PhIw',

]
if __name__ == '__main__':
    # for a in urls:
    #     put(a)
    #     print(a)
    PySqlTemplate.save("UPDATE estate set lane=SUBSTRING(lane FROM locate(?, lane)+1) where lane like ? ",')','%)%')
