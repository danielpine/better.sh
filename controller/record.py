import json
import logging
import sys
import time

import tornado
from tools.PySqlTemplate import PySqlTemplate

from controller import route
from controller.login import getUserInfoByToken
from tools.common import Base64Decrypt, Base64Encrypt

sys.path.append("..")
sys.path.append(".")
log = logging.getLogger(__name__)


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


@route('/record/list')
class ListHandler(tornado.web.RequestHandler):
    def get(self):
        page = []
        total = 0
        state = self.get_query_argument('state')
        pageSize = self.get_query_argument('pageSize')
        log.info(pageSize)
        current = self.get_query_argument('current')
        log.info(current)

        if len(state) > 0:
            state = '%'+'%'.join(state)+'%'
            total = PySqlTemplate.count(
                '''SELECT count(*) FROM  estate  where name like ? or lane like ?''', state, state)
            page = PySqlTemplate.findList(
                ''' SELECT e.*, r.mark_date, r.`name` AS pubname FROM ( SELECT * FROM estate WHERE NAME LIKE ? OR lane LIKE ? ORDER BY NAME LIMIT ?,? ) e LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0 ORDER BY e.NAME''', state, state, (int(
                    current)-1)*int(pageSize), int(pageSize)
            )
            if len(page) == 0:
                total = PySqlTemplate.count(
                    '''SELECT count(*) FROM  record  where name like ?''', state)
                page = PySqlTemplate.findList(
                    ''' SELECT mark_date,name,name as lane FROM  record  where name like ? ORDER BY NAME LIMIT ?,?''', state,   (int(
                        current)-1)*int(pageSize), int(pageSize)
                )
        else:
            total = PySqlTemplate.count('select count(*) from estate')
            page = PySqlTemplate.findList(
                '''SELECT E.*, R.MARK_DATE, R.`NAME` AS PUBNAME FROM ( SELECT * FROM estate ORDER BY NAME LIMIT ?,? ) E LEFT JOIN record R ON LOCATE(R.`NAME`, E.LANE) > 0 ORDER BY E. NAME''', (int(current)-1)*int(pageSize), int(pageSize))
        self.write({
            'code': 200,
            'msg': 'success',
            'total': total,
            'data': page
        })
