

class CORSMiddleware:
    """Add CORS headers to your responses so that you can
    receive AJAX requests from multiple domains.

    app.add_middleware(CORSMiddleware(['http://localhost:3000']))

    """

    def __init__(self, allow_origins):
        self.allowed_origins = ', '.join(allow_origins)

    async def process_request(self, req, res, handler):
        res.headers['Access-Control-Allow-Origin'] = self.allowed_origins
        res.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS,PUT,DELETE'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    async def process_response(self, req, res, handler):
        pass
