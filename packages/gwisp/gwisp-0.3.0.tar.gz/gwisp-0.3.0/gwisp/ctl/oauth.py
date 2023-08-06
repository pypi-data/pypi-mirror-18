from falcon import HTTPBadRequest, HTTP_204

from ..error import AuthenticateError
from ..validator import ctl
from ..repo import AccountRepo
from ..model.front import put_me as fmodel_put_me


class OauthCtl(object):

    '''
    Implement oauth-2 endpoint by essential supported

    :param gwisp.protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_post(self, req, res):
        params = req.context['body']

        if 'grant_type' not in params:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='grant_type must be specific'
            )

        if params['grant_type'] == 'password':
            self._grant_by_passwd(req, res)
        elif params['grant_type'] == 'refresh_token':
            self._grant_by_rtoken(req, res)
        else:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Not support grant_type'
            )

    def _grant_by_passwd(self, req, res):
        params = req.context['body']

        if 'username' not in params:
            raise AuthenticateError('Username is not set')
        if 'password' not in params:
            raise AuthenticateError('Passowrd is not set')

        res.body = self._protector.login_by_passwd(
            params['username'],
            params['password']
        )

    def _grant_by_rtoken(self, req, res):
        params = req.context['body']

        if 'refresh_token' not in params:
            raise AuthenticateError('Refresh token is not set')

        res.body = self._protector.refresh_token(params['refresh_token'])


class LoginUrlCtl(object):
    '''
    Information about how to login

    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_get(self, req, res):
        '''
        Response: Login url
        '''

        res.body = {
            'url': self._protector.login_url
        }


class LoginCtl(object):
    '''
    Support login by google oauth-2

    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_get(self, req, res):
        '''
        Request: Login code from google as query param

        Response: Token string
        '''

        res.body = self._protector.login_by_code(req.params['code'])


class AuthCodeCtl(object):
    '''
    Return google code to login
    '''

    def __init__(self):
        pass

    def on_get(self, req, res):
        if 'code' not in req.params:
            res.status = HTTPBadRequest
            return

        tmp = '''
        <html>
        <body style="text-align: center">
            <style>
                button {
                    font-size: 2em;
                    padding 4px;
                }
            </style>
            <script>
                function copyCode() {
                    var codeElem = document.getElementById('code')
                    var range = document.createRange();
                    var selection = window.getSelection()

                    range.selectNode(codeElem)
                    selection.removeAllRanges()
                    selection.addRange(range)
                    document.execCommand('copy')
                }
            </script>
            <h1>Code</h1>
            <h2 id="code">{{code}}</h2>
            <button onclick=copyCode()>Copy code to clipboard</button>
        </body>
        </html>
        '''

        res.body = tmp.replace('{{code}}', req.params['code'])


class MeCtl(object):
    '''
    Account information

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._acc_repo = AccountRepo(db)

    def on_get(self, req, res):
        '''
        Request: Token in header

        Response: Account information
        '''

        info = self._protector.check(req, True)

        res.body = info.account
        del res.body['subject']

    @ctl(fmodel_put_me.req)
    def on_put(self, req, res):
        '''
        Request: Token in header and content in body

        Response: No Content
        '''

        auth = self._protector.check(req)

        self._acc_repo.update_one(auth.account_id, req.context['body'])

        res.status = HTTP_204
