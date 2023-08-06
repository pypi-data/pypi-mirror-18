from tests.base import ServerTest
from albatross_extras.middleware.auth import AuthorizationMiddleware, encode_payload


class UserHandler:
    use_auth = 'reject'

    async def on_get(self, req, res):
        res.write('User %d' % req.user['user_id'])


class FileHandlerTest(ServerTest):

    def test_authorize_user_request(self):
        key = 'key'
        token = encode_payload({'user_id': 101}, key)

        async def aget_user(payload):
            # here you should fetch the user from the database using the payload.
            return {'user_id': payload['user_id']}

        def get_token(req):
            return req.query.get('token')

        auth = AuthorizationMiddleware(key, aget_user, get_token)
        self.server.add_middleware(auth)
        self.server.add_route('/user', UserHandler())

        response, body = self.request('/user')
        assert response.status == 401

        response, body = self.request('/user?token=%s' % token)
        assert response.status == 200
        assert body == 'User 101'
