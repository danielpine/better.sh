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


@route('/common/has')
class HasHandler(tornado.web.RequestHandler):
    def get(self):
        t = self.get_query_argument('t')
        f = self.get_query_argument('f')
        v = self.get_query_argument('v')
        k = self.get_query_argument('k')
        i = self.get_query_argument('i')
        # 如果是自己重复放行
        page = PySqlTemplate.findOne(
            'select * from %s where %s=? and %s=?' % (t, k, f), i,  v)
        if page:
            self.write({
                'code': 200,
                'msg': 'success',
                'data': None
            })
        else:
            page = PySqlTemplate.findOne(
                'select * from %s where %s=?' % (t, f),  v)
            self.write({
                'code': 200,
                'msg': 'success',
                'data': page
            })


@route('/users/has')
class HasHandler(tornado.web.RequestHandler):
    def get(self):
        page = PySqlTemplate.findOne(
            'select * from user where username=?', self.get_query_argument('username'))
        self.write({
            'code': 200,
            'msg': 'success',
            'data': page
        })


@route('/users/list')
class ListHandler(tornado.web.RequestHandler):
    def get(self):
        page = PySqlTemplate.findList('select * from user')
        for u in page:
            u['passwd'] = Base64Decrypt(u['passwd'])
        self.write({
            'code': 200,
            'msg': 'success',
            'data': page
        })


@route(r'/users/save')
class userAddHandler(tornado.web.RequestHandler):

    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        key = None
        if 'user_id' in form:
            key = form['user_id']
            PySqlTemplate.delete('delete from user where user_id=?', key)
        else:
            key = PySqlTemplate.count(
                'select IFNULL(max(user_id),0) from user')+1
            form['user_id'] = key
        ex = []
        for k in form:
            if k[0] == '_':
                ex.append(k)
        for k in ex:
            form.pop(k)

        if 'passwd' in form:
            form['passwd'] = Base64Encrypt(form['passwd'])

        cols = ['`'+v+'`' for k, v in enumerate(form)]
        vals = tuple(form[v] for k, v in enumerate(form))
        place = ','.join('?'*len(cols))
        colstr = ','.join(cols)
        vals = tuple(form[v] for k, v in enumerate(form))
        place = ','.join('?'*len(cols))
        print(cols)
        print(place)
        print(vals)
        sql = 'INSERT INTO user(%s) VALUES(%s)' % (colstr, place)
        PySqlTemplate.save(sql, *vals)
        self.write({"code": 200, "msg": "done", "data": key})

        self.write(
            {"code": 200, "msg": "done", "data": key})


@route(r'/users/del')
class userDelHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        key = None
        if 'user_id' in form:
            key = form['user_id']
            PySqlTemplate.delete('delete from user where user_id=?', key)
        self.write(
            {"code": 200, "msg": "done", "data": key})
