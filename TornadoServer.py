import logging
import os
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
    app = tornado.web.Application(routes, debug=True, static_path=os.path.join(
        os.path.dirname(__file__), "static"))
    app.listen(8000)
    log.info('started tornado sever...')
    tornado.ioloop.IOLoop.current().start()
