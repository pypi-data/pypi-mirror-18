
class LoggingMiddleware:
    def __init__(self, logger):
        self.logger = logger

    async def process_request(self, req, res, handler):
        pass

    async def process_response(self, req, res, handler):
        name = getattr(handler, 'name', handler.__class__.__name__)
        status_code = res.status_code.split()[0]
        self.logger.info('Request received', dict(
            route=req.path,
            status_code=status_code,
            method=req.method,
            handler=name,
        ))
