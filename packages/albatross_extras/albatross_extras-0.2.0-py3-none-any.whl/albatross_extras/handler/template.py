
from jinja2 import Environment, FileSystemLoader


class TemplateHandler:
    """

    server.add_route('/login', TemplateHandler('login.jinja2'))
    """
    @classmethod
    def set_template_directory(cls, path):
        loader = FileSystemLoader(path)
        cls.env = Environment(loader=loader)

    env = None

    def get_context(self, req):
        return {
            'user': getattr(req, 'user', None)
        }

    def __init__(self, template_path, content_type='text/html; charset=utf-8'):
        self.template = self.env.get_template(template_path)
        self.content_type = content_type

    async def on_get(self, req, res):
        res.headers['Content-Type'] = self.content_type
        res.write(self.template.render(**self.get_context(req)))

TemplateHandler.set_template_directory('templates')
