from base64 import encode
from requests_html import HTMLSession, HTMLResponse
import json
c = []

session = HTMLSession()
site: HTMLResponse = session.get('https://sh.ke.com/xiaoqu/pudong/')
collect = site.html.find('.title .maidian-detail')
# print('start page 1')
for item in collect:
    # print(item.attrs['href'], item.attrs['title'])
    site2: HTMLResponse = session.get(item.attrs['href'])
    Lane = site2.html.find('.sub', first=True)
    # print(Lane.text)
    c.append({
        'name': item.attrs['title'],
        'lane': Lane.text
    })
# print('end page 1')
for i in range(2, 101):
    session = HTMLSession()
    url = 'https://sh.ke.com/xiaoqu/pudong/pg%d/' % i
    # print(url)
    site3: HTMLResponse = session.get(url)
    collect = site3.html.find('.title .maidian-detail')
    # print('start page %d' % i)
    for item in collect:
        # print(item.attrs['href'], item.attrs['title'])
        site2: HTMLResponse = session.get(item.attrs['href'])
        Lane = site2.html.find('.sub', first=True)
        # print(Lane.text)
        c.append({
            'name': item.attrs['title'],
            'lane': Lane.text
        })
    # print('end   page %d' % i)
with open('estates.json', "w", encoding="utf-8")as f:
    json.dump(c, f, ensure_ascii=False, indent=4)
