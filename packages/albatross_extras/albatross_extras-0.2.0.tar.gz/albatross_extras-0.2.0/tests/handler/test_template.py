from tests.base import ServerTest
from albatross_extras.handler.template import TemplateHandler


class TemplateHandlerTest(ServerTest):

    def test_template(self):
        TemplateHandler.set_template_directory('tests')
        self.server.add_route('/hello', TemplateHandler('test_template.j2'))
        response, body = self.request('/hello')
        assert response.status == 200
        assert body == '<h1>Good job!</h1>\n', repr(body)
