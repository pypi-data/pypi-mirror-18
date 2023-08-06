from albatross_extras.lib import stats
from time import time


class StatsdMiddleware:
    def __init__(self, **kwargs):
        stats.connect_statsd(**kwargs)

    async def process_request(self, req, res, handler):
        name = getattr(handler, 'name', handler.__class__.__name__)
        req._start_time = time()
        stats.incr('%s.%s.incoming' % (name, req.method))

    async def process_response(self, req, res, handler):
        status_code = res.status_code.split()[0]
        duration = time() - req._start_time
        name = getattr(handler, 'name', handler.__class__.__name__)

        stats.incr('%s.%s.status_code.%s' % (name, req.method, status_code))
        stats.timing('%s.%s' % (name, req.method), int(duration * 1000))
