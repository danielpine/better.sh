import json

import tornado
import logging
import sys

from tools.PySqlTemplate import PySqlTemplate
from controller import route
from service import LoginService
from tools import generateAccessToken
from tools.common import Base64Encrypt, RSADecrypt
sys.path.append("..")
sys.path.append(".")
log = logging.getLogger(__name__)
users = {}
loginService = LoginService()


def getUserInfoByToken(token):
    if token in users:
        return users[token]
    else:
        return None


status = {}


@route(r'/logout')
class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        self.write({"code": 200, "msg": "success"})


@route(r'/info')
class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_cookie('token')
        log.info(token)
        if token and token in users:
            self.write({"code": 200, "msg": "success", "data": users[token]})
        else:
            self.write({"code": 401,
                        "msg": "login timed out!"})


@route(r'/login')
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.warn(form)
        token = generateAccessToken()
        user = loginService.findUser(RSADecrypt(
            form['username']), Base64Encrypt(RSADecrypt(form['password'])))
        if user:
            self.write({"code": 200, "msg": "success",
                       "data": {"token": token}})
            users[token] = {
                "name": user['username'],
                'user_id': user['user_id'],
                'role': user['role'],
                "access": [user['role']],
                'token': token,
                "avatar": "https://i.gtimg.cn/club/item/face/img/8/15918_100.gif"}
        else:
            self.write({"code": 400,
                        "msg": "username or password is incorrect!"})
