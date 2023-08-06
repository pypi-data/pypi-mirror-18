import falcon
from pymongo.errors import DuplicateKeyError
from jwt.exceptions import DecodeError, ExpiredSignatureError
from jsonschema.exceptions import ValidationError

from .handler import dupkey_handle, jwt_decode_handle, \
                     unauthorized_handle, forbidden_handle, jwt_sign_handle, \
                     validation_handle, not_exist_handle, \
                     bad_request_handle
from .error import AuthenticateError, AuthorizeError, NotExistError
from .validator import CtlArgError
from .dbclient import DbClient
from .dbtool import DbTool
from .middleware import RequireJSON, JsonTranslator, FormTranslator, EnableCORS
from .ctl import OauthCtl, AuthCodeCtl, \
                 RootCtl, LoginUrlCtl, LoginCtl, MeCtl, \
                 TrackerItemCtl, TrackerCtl, \
                 TrackerAccountCtl, TrackerAccountItemCtl, \
                 TrackerMeCtl, \
                 TrackerUsingCtl, TrackerUsingItemCtl, \
                 TrackerClonedCtl, TrackerClonedItemCtl
from .protector import Protector


class Worker(object):
    '''
    Create WSGI application with gwisp http interface.
    No real serve anythings. After get application from ``start()``,
    use that application to serve though ``guicorn`` server

    :param str db_url: Url to mongo database server
    :param str client_id: Google client identity, use for oauth-2
    :param str client_secret: Google client secret, use for oauth-2
    :param str redirect_uri: Callback url after confirm google login
    :param str jwt_key: Secret words use to sign token of service
    '''
    def __init__(self, db_url,
                 client_id, client_secret, redirect_uri, jwt_key):
        self._db_url = db_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._jwt_key = jwt_key

        # Connect to mongodb server
        # All of task must use only this connection
        self._dbc = DbClient(self._db_url)
        self._dbc.connect()

        # Protector use to authenticate and authorize
        self._protector = Protector(
            self._dbc.db,
            self._client_id,
            self._client_secret,
            [
                'https://www.googleapis.com/auth/plus.me',
                'profile',
                'email'
            ],
            self._redirect_uri,
            self._jwt_key
        )

    def reg_root(self, email, passwd):
        '''
        Register root account. Name is gwisp

        :param str email: Email of root account
        :param str passwd: Password in plain text
        '''

        account = {
            'name': 'gwisp',
            'email': email,
            'subject': '0',
            'language': 'en',
            'groups': ['root'],
            'avatar': 'http://static.gwisp/avatar/gwisp.jpg'
        }

        self._protector.create_account(account, passwd)

    def start(self):
        '''
        Create an WSGI application

        :return: WSGI application
        :rtype: falcon.API
        '''

        # Create collection if database is empty
        if self._dbc.is_empty() is True:
            self._dbc.renew()

        # Check indexes of collection in database
        self._dbc.check_indexs()

        # Shortcut for connection to database
        db = self._dbc.db

        # Http application
        app = falcon.API(middleware=[
            EnableCORS(),
            RequireJSON(),
            JsonTranslator(),
            FormTranslator()
        ])

        # Error handle
        app.add_error_handler(ValidationError, validation_handle)
        app.add_error_handler(DuplicateKeyError, dupkey_handle)
        app.add_error_handler(DecodeError, jwt_decode_handle)
        app.add_error_handler(ExpiredSignatureError, jwt_sign_handle)
        app.add_error_handler(AuthenticateError, unauthorized_handle)
        app.add_error_handler(AuthorizeError, forbidden_handle)
        app.add_error_handler(NotExistError, not_exist_handle)
        app.add_error_handler(CtlArgError, bad_request_handle)

        # Controllers
        app.add_route('/', RootCtl(db))

        app.add_route('/oauth', OauthCtl(self._protector))
        app.add_route('/oauth/code', AuthCodeCtl())
        app.add_route('/oauth/url', LoginUrlCtl(self._protector))
        app.add_route('/oauth/callback', LoginCtl(self._protector))

        app.add_route('/me', MeCtl(db, self._protector))

        app.add_route('/tracker/using', TrackerUsingCtl(db, self._protector))
        app.add_route(
            '/tracker/using/{id}',
            TrackerUsingItemCtl(db, self._protector)
        )

        app.add_route('/tracker', TrackerCtl(db, self._protector))
        app.add_route('/tracker/{id}', TrackerItemCtl(db, self._protector))

        app.add_route(
            '/tracker/account',
            TrackerAccountCtl(db, self._protector)
        )
        app.add_route(
            '/tracker/account/{id}',
            TrackerAccountItemCtl(db, self._protector)
        )

        app.add_route('/tracker/me', TrackerMeCtl(db, self._protector))

        app.add_route('/tracker/cloned', TrackerClonedCtl(db, self._protector))
        app.add_route(
            '/tracker/cloned/{id}',
            TrackerClonedItemCtl(db, self._protector)
        )

        return app

    def stop(self):
        '''
        Close connection to database, free other resource. If want to
        run new worker, create an new instance instead of reuse old worker
        after stop
        '''

        self._dbc.close()
        self._dbc = None
        self._protector = None

    def renew_db(self):
        '''
        Ensure database have correct index and empty data
        '''

        self._dbc.renew()

    def setup(self, asset_dir, email, password):
        '''
        Drop database if it is exist. Create new database with correct
        indexs. Install sample data

        :param str asset_dir: Path to asset directory.
            See :ref:`api_asset_dir`
        '''

        self._dbc.renew()

        avatar = '''
        https://github.com/kevin-leptons/gwisp/raw/master/asset/gwisp-64.png
        '''
        account = {
            'email': email,
            'name': 'gwisp',
            'subject': '0',
            'language': 'en',
            'groups': ['root'],
            'avatar': avatar
        }

        dbtool = DbTool(
            self._dbc.db, self._protector, asset_dir, account, password
        )
        dbtool.install()
