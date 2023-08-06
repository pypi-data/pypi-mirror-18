from tests.base import ServerTest
from albatross_extras.middleware.logging import LoggingMiddleware
from albatross_extras.handler.health import HealthHandler
from unittest import mock


class LoggingMiddlewareTest(ServerTest):

    def test_logging_middleware(self):

        logger = mock.Mock()
        self.server.add_middleware(LoggingMiddleware(logger))
        self.server.add_route('/health', HealthHandler())

        response, body = self.request('/health')
        assert response.status == 200
        assert body == 'OK'
        assert logger.info.called
        call = logger.info.call_args[0]
        assert call[0] == 'Request received'
        assert call[1] == {
            'route': '/health',
            'status_code': '200',
            'handler': 'HealthHandler',
            'method': 'GET'
        }
