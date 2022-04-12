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
            total = PySqlTemplate.count('''SELECT
                                              count(*) 
                                            FROM
                                                estate
                                            where name like ? or lane like ?''',
                                        state, state)
            page = PySqlTemplate.findList(
                '''
                SELECT
                    e.*,r.mark_date,r.`name` as pubname
                FROM
                    (SELECT
                            *
                        FROM
                            estate
                        where name like ? or lane like ?    
                        ORDER BY
                            NAME
                        LIMIT ?,?
                    ) e
                LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0
                ORDER BY
                    e. NAME,
                    mark_date
                ''', state, state, (int(current)-1)*int(pageSize), int(pageSize)
            )
        else:
            total = PySqlTemplate.count('select count(*) from estate')
            page = PySqlTemplate.findList(
                '''
                SELECT
                    e.*,r.mark_date,r.`name` as pubname
                FROM
                    (
                        SELECT
                            *
                        FROM
                            estate
                        ORDER BY
                            NAME
                        LIMIT ?,?
                    ) e
                LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0
                ORDER BY
                    e. NAME,
                    mark_date
                ''', (int(current)-1)*int(pageSize), int(pageSize))
        self.write({
            'code': 200,
            'msg': 'success',
            'total': total,
            'data': page
        })
