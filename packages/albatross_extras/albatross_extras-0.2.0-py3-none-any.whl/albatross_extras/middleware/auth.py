import jwt
from albatross.http_error import HTTPError
from albatross.status_codes import HTTP_401, HTTP_302
from urllib.parse import quote


def encode_payload(payload, signing_key):
    """Payload contains the parameters you need to restore state.
    ``signing_key`` must be the same parameter passed to the ``AuthorizationMiddleware``.

    token = encode_payload({"user_uuid": user_uuid}, 'my-secret-key')

    """
    token = jwt.encode(payload, signing_key, algorithm='HS256')
    return token.decode()


class AuthorizationMiddleware:
    def __init__(self, signing_key, aget_user, get_token):
        self.signing_key = signing_key
        self.aget_user = aget_user
        self.get_token = get_token

    def handle_not_authorized(self, req, res, handler):
        if handler.use_auth == 'redirect':
            res.redirect('/login?next=%s' % quote(req.path))
            raise HTTPError(HTTP_302)
        else:
            raise HTTPError(HTTP_401)

    async def process_request(self, req, res, handler):
        if not getattr(handler, 'use_auth', False):
            return
        token = self.get_token(req)
        if not token:
            self.handle_not_authorized(req, res, handler)

        payload = jwt.decode(token, self.signing_key, algorithms=['HS256'])
        user = await self.aget_user(payload)

        if user is None:
            raise HTTPError(HTTP_401)
        req.user = user

    async def process_response(self, req, res, handler):
        pass
