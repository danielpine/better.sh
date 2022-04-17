import urllib.parse
import logging
import os
import platform
import tornado.ioloop
import tornado.web

from controller import routes
from tools import routeScan, setupDataSource
from tools.PySqlTemplate import PySqlTemplate
from tools.common import getPythonDataBase

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s %(levelname)s] [%(pathname)s:%(lineno)s] [%(message)s]")

log = logging.getLogger(__name__)

routeScan('controller')
setupDataSource()
profile = os.getenv('PY_DB_TP')

# if __name__ == "__main__":
#     plat = platform.system().lower()
#     application = tornado.web.Application(routes, debug=plat == 'windows', static_path=os.path.join(
#         os.path.dirname(__file__), "static"))
#     if plat == 'windows':
#         application.listen(8000)
#     elif plat == 'linux':
#         http_server = tornado.httpserver.HTTPServer(application)
#         http_server.bind(8000)
#         http_server.start(num_processes=12)
#     log.info('started tornado sever...')
#     tornado.ioloop.IOLoop.current().start()

plat = platform.system().lower()

application = tornado.web.Application(routes, debug=plat == 'windows', static_path=os.path.join(
    os.path.dirname(__file__), "static"))


def makeStatistics(request):
    uri = request.uri
    try:
        if uri.startswith('/record/stat'):
            return
        # print(uri)
        if uri.startswith('/static/index.html'):
            # print('访问主页')
            PySqlTemplate.save('update stat set home=home+1 where id=1')
        if uri.startswith('/record/'):
            # print('调用接口 %s' % uri)
            PySqlTemplate.save('update stat set api=api+1 where id=1')
            if uri.startswith('/record/list?state'):
                remote_ip = request.headers.get("X-Real-Ip", "")
                # print(remote_ip)
                PySqlTemplate.save(
                    'insert into search(search,ip) values(?,?)', urllib.parse.unquote(uri), remote_ip)
    except:
        pass


def middleware(request):
    # do whatever transformation you want here
    makeStatistics(request)
    application(request)


if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(middleware, xheaders=True)
    http_server.listen(8000)
    if plat == 'linux':
        http_server.start(num_processes=12)
    log.info('started tornado sever...')
    tornado.ioloop.IOLoop.current().start()
