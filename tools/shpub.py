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
    uc = PySqlTemplate.count(
        'select count(*) from urls where url=?', url.strip())
    if uc == 0:
        session = HTMLSession()
        site: HTMLResponse = session.get(url)
        title = site.html.find('.rich_media_title', first=True)
        s = '2022年'+title.text.split('（')[0]
        date = datetime.datetime.strftime(
            datetime.datetime.strptime(s.replace('【最新】',''), '%Y年%m月%d日'), r'%m%d')
        collect = site.html.find('span')
        district = ''
        with open(date+'.txt', "w", encoding="utf-8") as f:
            for item in collect:
                if '分别居住于' in item.text and '2022年' in item.text:
                    district = item.text.split('区')[0].split('，')[
                        1].replace('新', '')
                    print(district)
                    f.write(district)
                    f.write('\n')
                if len(item.text) > 2 and (item.text[-1] == '，' or item.text[-1] == '。') and '已对相关' not in item.text and '无症状感染者' not in item.text and '微信平台' not in item.text and '本土确诊病例'  not in item.text:
                    names = item.text.replace('，', '').replace('。', '').strip()
                    if names:
                        l=[names]
                        if '、' in names:
                            l=names.split('、')
                        for  name in l:    
                            f.write(name)
                            f.write('\n')
                            print(name)
                            try:
                                c = PySqlTemplate.count(
                                    'select count(*) from estate where lane like ?', '%'+name+'%')
                                if c == 0:
                                    PySqlTemplate.save(
                                        '''insert into estate(`name`,lane,`from`) values(?,?,?)''',
                                        name, '(%s) %s' % (district, name), 'System')
                            except:
                                print('error when:'+name)

                            try:
                                PySqlTemplate.save(
                                'insert into record(name,mark_date,year) values(?,?,?)', name, date, '2022')
                            except:
                                print('error when:'+name)
        PySqlTemplate.save(
        'insert into urls(url) values(?)', url.strip())
    else:
        print('has recorde '+url)


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
    for a in urls:
        put(a)
        print(a)
