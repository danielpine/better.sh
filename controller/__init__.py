import logging
import sys
sys.path.append("..")
sys.path.append(".")
log = logging.getLogger(__name__)
routes = []


def route(rule, **options):
    def decorator(handler):
        log.info('mapping %s to %s' % (rule, handler))
        routes.append((rule, handler))
        return handler
    return decorator
