import json
import logging
import sys
import time

import tornado
from tools.PySqlTemplate import PySqlTemplate

from controller import route
from controller.login import getUserInfoByToken
from tools.common import Base64Decrypt, Base64Encrypt, extract
from tools.shpub import putData

sys.path.append("..")
sys.path.append(".")
log = logging.getLogger(__name__)


@route('/record/apply')
class ApplyHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        row = json.dumps(form['row'], ensure_ascii=False)
        print(row)
        PySqlTemplate.save(
            'insert into apply(`row`,`mode`) values(?,?)', row, form['mode'])


@route('/record/save')
class SaveHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_query_argument('name')
        lane = self.get_query_argument('lane')
        PySqlTemplate.save(
            '''insert into estate(`name`,lane,`from`) values(?,?,?)''', name, lane, 'Stranger')
        self.write({
            'code': 200,
            'msg': 'success',
        })


@route('/record/has')
class HasHandler(tornado.web.RequestHandler):
    def get(self):
        t = self.get_query_argument('t')
        total = PySqlTemplate.count(
            '''SELECT count(*) FROM estate where name=?''', t)
        self.write({
            'code': 200,
            'msg': 'success',
            'data': total
        })


@route('/record/stat')
class StatHandler(tornado.web.RequestHandler):
    def get(self):
        data = PySqlTemplate.findOne(
            '''SELECT * FROM stat where id=?''', 1)
        self.write({
            'code': 200,
            'msg': 'success',
            'data': data
        })


@route('/record/like')
class LikeHandler(tornado.web.RequestHandler):
    def get(self):
        data = PySqlTemplate.save(
            '''update stat set `like`=`like`+1 where id=?''', 1)
        data = PySqlTemplate.findOne(
            '''SELECT * FROM stat where id=?''', 1)
        self.write({
            'code': 200,
            'msg': 'success',
            'data': data
        })


@route('/record/sheep')
class ListHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.get_query_argument('url')
        data = putData(url, True, True)
        self.write({
            'code': 200,
            'msg': 'success',
            'data': data
        })


@route('/record/list')
class ListHandler(tornado.web.RequestHandler):

    def handleMultiSearch(self, state, pageSize, current, dd):
        fields = extract(state)
        print(fields)
        vals = []
        statements = []
        if '小区' in fields:
            s = ['%'+'%'.join(st)+'%' for st in fields['小区']]
            t = [' name like ? ' for st in fields['小区']]
            vals += s
            statements += t

        if '地址' in fields:
            s = ['%' + st + '%' for st in fields['地址']]
            t = [' lane like ? ' for st in fields['地址']]
            vals += s
            statements += t
        vals = tuple(v for v in vals)
        sql = 'or'.join(statements)
        if sql:
            sql = ' WHERE '+sql

        countSql = '''SELECT count(name) FROM  estate %s''' % sql

        total = PySqlTemplate.count(countSql, *vals)
        print(total)
        # where r.mark_date>=?
        page = PySqlTemplate.findList(
            ''' SELECT e.*, r.mark_date, r.`name` AS pubname FROM 
            ( SELECT * FROM estate %s ORDER BY NAME LIMIT ?,? ) e 
            LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0  ORDER BY e.NAME''' % sql,
            *vals,
            (int(current)-1)*int(pageSize), int(pageSize)
        )
        print(page)
        self.write({
            'code': 200,
            'msg': 'success',
            'total': total,
            'data': page
        })

    def get(self):
        page = []
        total = 0
        state = self.get_query_argument('state')
        pageSize = self.get_query_argument('pageSize')
        log.info(pageSize)
        current = self.get_query_argument('current')
        log.info(current)
        dd = self.get_query_argument('date')
        log.info(dd)
        if '@' in state:
            self.handleMultiSearch(state, pageSize, current, dd)
        else:
            if len(state) > 0:
                lane = '%'+state+'%'
                state = '%'+'%'.join(state)+'%'
                total = PySqlTemplate.count(
                    '''SELECT count(*) FROM  estate  where name like ? or lane like ?''', state, lane)
                page = PySqlTemplate.findList(
                    ''' SELECT e.*, r.mark_date, r.`name` AS pubname FROM ( SELECT * FROM estate WHERE NAME LIKE ? OR lane LIKE ? ORDER BY NAME LIMIT ?,? ) e LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0  ORDER BY e.NAME''', state, state, (int(#where r.mark_date>=?
                        current)-1)*int(pageSize), int(pageSize)#, dd
                )
                if len(page) == 0:
                    total = PySqlTemplate.count(
                        '''SELECT count(*) FROM  record  where name like ?''', state)
                    page = PySqlTemplate.findList(
                        ''' SELECT mark_date,name,name as lane FROM  record  and name like ? ORDER BY NAME LIMIT ?,?''',   state,   (int(# where mark_date>=?
                            current)-1)*int(pageSize), int(pageSize)
                    )
            else:
                total = PySqlTemplate.count('select count(*) from estate')
                page = PySqlTemplate.findList(
                    '''SELECT E.*, R.mark_date, R.`NAME` AS pubname FROM ( SELECT * FROM estate ORDER BY NAME LIMIT ?,? ) E LEFT JOIN record R ON LOCATE(R.`NAME`, E.LANE) > 0   ORDER BY E. NAME''', (int(current)-1)*int(pageSize), int(pageSize))#where R.mark_date>=?, dd)
            self.write({
                'code': 200,
                'msg': 'success',
                'total': total,
                'data': page
            })
