import json
import logging
import sys
import time
import traceback

import tornado
import tornado.websocket

from controller import route

sys.path.append("..")
sys.path.append(".")
log = logging.getLogger(__name__)

Sockets = []


@route(r'/socket')
class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        '''重写同源检查 解决跨域问题'''
        return True

    def open(self):
        '''新的websocket连接后被调动'''
        # self.write_message('即时消息推送连接成功!')
        Sockets.append(self)
        log.info('connected... curr: %s'% len(Sockets))

    def on_close(self):
        '''websocket连接关闭后被调用'''
        Sockets.remove(self)
        log.info('closed...')

    def on_message(self, message):
        '''接收到客户端消息时被调用'''
        try:
            message = json.loads(message)
            self.write_message(message)  # 向客服端发送
        except Exception as e:
            traceback.log.info_exc()
