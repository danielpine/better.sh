import logging
import os
import platform
import tornado.ioloop
import tornado.web

from controller import routes
from tools import routeScan, setupDataSource
from tools.common import getPythonDataBase

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s %(levelname)s] [%(pathname)s:%(lineno)s] [%(message)s]")

log = logging.getLogger(__name__)

routeScan('controller')
setupDataSource()
profile = os.getenv('PY_DB_TP')

if __name__ == "__main__":
    #profile is not None
    application = tornado.web.Application(routes, debug=True, static_path=os.path.join(
        os.path.dirname(__file__), "static"))
    plat = platform.system().lower()

    if plat == 'windows':
        application.listen(8000)
    elif plat == 'linux':
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.bind(8000)
        http_server.start(num_processes=12)
    log.info('started tornado sever...')
    tornado.ioloop.IOLoop.current().start()
