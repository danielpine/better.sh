import datetime
from requests_html import HTMLSession, HTMLResponse
import json
import sys
sys.path.append("..")
sys.path.append(".")


def putData(url, unique, save):
    from tools import setupDataSource
    from tools.PySqlTemplate import PySqlTemplate
    setupDataSource()
    year = '2022'
    uc = 0
    data = {}
    if unique:
        uc = PySqlTemplate.count(
            'select count(*) from urls where url=?', url.strip())

    if uc == 0:
        session = HTMLSession()
        site: HTMLResponse = session.get(url)
        title = site.html.find('.rich_media_title', first=True)
        s = '2022年'+title.text.split('（')[0]
        date = datetime.datetime.strftime(
            datetime.datetime.strptime(s.replace('【最新】', ''), '%Y年%m月%d日'), r'%m%d')
        collect = site.html.find('p')
        district = ''
        maps = {}
        data['sheep'] = maps
        for item in collect:
            if '分别居住于' in item.text and '区' in item.text:
                district = item.text.split('区')[0]
                district = district.replace('新', '')
                if '，' in district:
                    district = district.split('，')[1]
                print(district)
                maps[district] = []
                continue
            if not district:
                continue
            if (('已对相关' not in item.text
                and '无症状感染者' not in item.text
                and '微信平台' not in item.text
                and '滑动查看更多' not in item.text
                and '2022' not in item.text
                and '各区卫健委' not in item.text
                and '新闻办' not in item.text
                and '编辑' not in item.text
                and '微信扫一扫' not in item.text
                and '1例为' not in item.text
                 )):
                names = item.text.replace('，', '').replace(
                    '。', '').replace(',', '').strip()
                if names:
                    l = [names]
                    if '、' in names:
                        l = names.split('、')
                    for name in l:
                        name = name.strip()
                        if name:
                            maps[district].append(name)
        with open('data/'+date+'.json', "w", encoding="utf-8")as f:
            json.dump(maps, f, ensure_ascii=False, indent=4)
        if save:
            PySqlTemplate.delete('delete from record where mark_date=?', date)
            for d in maps:
                print('===')
                print(d)
                print('===')
                for name in maps[d]:
                    print(name)
                    try:
                        PySqlTemplate.delete(
                            'delete from estate where name=? and district=?', name, d)
                        PySqlTemplate.save(
                            '''insert into estate(`name`,lane,`from`,district) values(?,?,?,?)''',
                            name, name, 'System', d)
                    except:
                        print('error when:'+name)
                    try:
                        PySqlTemplate.save(
                            'insert into record(name,mark_date,year,district) values(?,?,?,?)', name, date, year, d)
                    except:
                        print('error when:'+name)
                print('---')
        if unique:
            PySqlTemplate.save('insert into urls(url) values(?)', url.strip())
        PySqlTemplate.save(
            '''update stat set `pubdt`=? where id=?''', '%s-%s-%s' % (year, date[:2], date[2:]), 1)
        PySqlTemplate.save(
            '''update stat set `updatetm`=? where id=?''', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
    else:
        print('has recorde '+url)
        data['info'] = 'has recorde '+url
    return data


urls = [
    'https://mp.weixin.qq.com/s/656rotFOMeDScnKSt6OmyQ',  # 0328
    'https://mp.weixin.qq.com/s/K6jT1wRMSScBhvxcB2yV4g',  # 0329
    'https://mp.weixin.qq.com/s/SSFVzOSXPTj-aLzR1tdtxw',  # 0330
    'https://mp.weixin.qq.com/s/hnrGo4KvUvxhpjFyiE8-sQ',  # 0331
    'https://mp.weixin.qq.com/s/gQDyFLtdILP2NuSBgcjUxg',  # 0401
    'https://mp.weixin.qq.com/s/2VWTo6e9gmWJ0vxeZ4PhIw',  # 0402
    'https://mp.weixin.qq.com/s/uj4TYASUn2YJZQMg2aUvdw',  # 0403
    'https://mp.weixin.qq.com/s/MkKsQkgvUWbwj8z9jG_Zng',  # 0404
    'https://mp.weixin.qq.com/s/djwW3S9FUYBE2L5Hj94a3A',  # 0405
    'https://mp.weixin.qq.com/s/8bljTUplPh1q4MXb6wd_gg',  # 0406
    'https://mp.weixin.qq.com/s/_Je5_5_HqBcs5chvH5SFfA',  # 0407
    'https://mp.weixin.qq.com/s/79NsKhMHbg09Y0xaybTXjA',  # 0408
    'https://mp.weixin.qq.com/s/HTM47mUp0GF-tWXkPeZJlg',  # 0409
    'https://mp.weixin.qq.com/s/u0XfHF8dgfEp8vGjRtcwXA',  # 0410
    'https://mp.weixin.qq.com/s/vxFiV2HeSvByINUlTmFKZA',  # 0411
    'https://mp.weixin.qq.com/s/OZGM-pNkefZqWr0IFRJj1g',  # 0412
    'https://mp.weixin.qq.com/s/L9AffT-SoEBV4puBa_mRqg',  # 0413
    'https://mp.weixin.qq.com/s/5T76lht3s6g_KTiIx3XAYw',  # 0414
    'https://mp.weixin.qq.com/s/ZkhimhWpa92I2EWn3hmd8w',  # 0415
    'https://mp.weixin.qq.com/s/dRa-PExJr1qkRis88eGCnQ',  # 0416

]
if __name__ == '__main__':
    for a in urls:
        putData(a, True, True)
        print(a)
