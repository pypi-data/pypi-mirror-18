from tests.base import ServerTest
from albatross_extras.handler.health import HealthHandler, ProfileHandler


class FileHandlerTest(ServerTest):

    def test_health(self):
        self.server.add_route('/health', HealthHandler())
        response, body = self.request('/health')
        assert response.status == 200
        assert body == 'OK'

    def test_profiler(self):
        profiling_handler = ProfileHandler('secret-key')
        self.server.add_route('/profile', profiling_handler)
        response, body = self.request('/profile?t=0')
        assert response.status == 404
        response, body = self.request('/profile?t=0&key=wrong-key')
        assert response.status == 404
        response, body = self.request('/profile?t=0&key=secret-key')
        assert response.status == 200
        assert body
