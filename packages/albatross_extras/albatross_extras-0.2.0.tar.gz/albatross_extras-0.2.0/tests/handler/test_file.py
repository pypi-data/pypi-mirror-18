from tests.base import ServerTest
from albatross_extras.handler.file import StaticFileHandler


class FileHandlerTest(ServerTest):

    def test_health(self):
        self.server.add_route('/readme', StaticFileHandler.file('README.rst'))
        response, body = self.request('/readme')
        assert response.status == 200
        assert body
