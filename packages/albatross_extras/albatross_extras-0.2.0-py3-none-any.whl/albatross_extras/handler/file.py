import mimetypes
import gzip
import os.path as op


class StaticFileHandler:
    """Handler to serve a single (optionally compressed) file.

    handler = StaticFileHandler.file('/path/to/my/file.jpg', can_gzip=False)
    server.add_route('/file.jpg', handler)

    handler = StaticFileHandler(b'a_binary_blob', can_gzip=True)
    server.add_route('/very/secret/key', handler)
    """

    @classmethod
    def file(cls, file_path, can_gzip=True):
        with open(file_path, 'rb') as f:
            raw_body = f.read()
        content_type = (mimetypes.guess_type(file_path)[0]
                        or 'application/octet-stream')
        if content_type.startswith('text/'):
            content_type += '; charset=utf-8'
        return cls(raw_body, content_type, can_gzip=can_gzip)

    def __init__(self, raw_body, content_type, can_gzip=True):
        self.content_type = content_type
        self.can_gzip = can_gzip
        self.body = raw_body
        self.gzipped_body = gzip.compress(raw_body) if can_gzip else None

    async def on_get(self, req, res):
        res.headers['Content-Type'] = self.content_type
        if self.can_gzip and 'gzip' in req.headers.get('Accept-Encoding', ''):
            res.headers['Content-Encoding'] = 'gzip'
            res.write_bytes(self.gzipped_body)
        else:
            res.write_bytes(self.body)


class StaticDirectoryHandler:
    """Handler to serve a directory of assets.

    handler = StaticDirectoryHandler('public/')
    app.add_regex_route('/static/(?P<path>[\.a-zA-Z0-9/]+)', handler)

    js_handler = StaticDirectoryHandler('public/js/', file_arg='fname')
    app.add_route('/static/js/{fname}', js_handler)
    """

    def __init__(self, directory, file_arg='path', can_gzip=True):
        self.can_gzip = can_gzip
        self.directory = directory
        self.file_arg = file_arg

    async def on_get(self, req, res):
        path = req.args[self.file_arg]
        fpath = op.join(self.directory, path)

        with open(fpath, 'rb') as f:
            contents = f.read()

        content_type = (mimetypes.guess_type(path)[0]
                        or 'application/octet-stream')
        res.headers['Content-Type'] = content_type
        if self.can_gzip and 'gzip' in req.headers.get('Accept-Encoding', ''):
            contents = gzip.compress(contents)
            res.headers['Content-Encoding'] = 'gzip'
        res.write_bytes(contents)
