from tests.base import ServerTest
from albatross_extras.handler.health import HealthHandler
from albatross_extras.middleware.statsd import StatsdMiddleware
from albatross_extras.lib.stats import connect_statsd
from unittest import mock


class StatsdMiddlewareTest(ServerTest):

    @mock.patch('statsd.StatsClient')
    def test_statsd_middleware(self, StatsMock):
        conn = mock.Mock()
        StatsMock.return_value = conn
        connect_statsd()
        auth = StatsdMiddleware()
        self.server.add_middleware(auth)
        self.server.add_route('/health', HealthHandler())

        response, body = self.request('/health')
        assert response.status == 200
        assert body == 'OK'
        assert StatsMock.called
        assert len(conn.method_calls) == 3
        calls = conn.method_calls

        assert calls[0][0] == 'incr'
        assert calls[0][1] == ('HealthHandler.GET.incoming', 1, 1)
        assert calls[1][0] == 'incr'
        assert calls[1][1] == ('HealthHandler.GET.status_code.200', 1, 1)
        assert calls[2][0] == 'timing'
        assert calls[2][1] == ('HealthHandler.GET', 0, 1)
