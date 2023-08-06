import asyncio
import cProfile as cprof
import io
import pstats
from albatross import HTTPError, HTTP_404


class HealthHandler:
    """A very simple handler.
    """
    async def on_get(self, req, res):
        res.write('OK')


class ProfileHandler:
    """Allows you to profile your server. Note this slows your server down,
    so the route is protected by the ``profiling_key``.

    """
    def __init__(self, profiling_key):
        self.profiling_key = profiling_key

    async def on_get(self, req, res):
        time = int(req.query.get('t', 10))
        secret = req.query.get('key')
        if secret != self.profiling_key:
            raise HTTPError(HTTP_404)

        prof = cprof.Profile()
        prof.enable()
        await asyncio.sleep(time)
        prof.disable()
        prof.create_stats()
        s = io.StringIO()
        stats_obj = pstats.Stats(prof, stream=s).sort_stats("cumulative")
        stats_obj.print_stats()
        res.write(s.getvalue())
