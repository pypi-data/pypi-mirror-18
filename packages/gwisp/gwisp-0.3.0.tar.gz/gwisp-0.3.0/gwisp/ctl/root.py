import pkg_resources

from ..repo import AccountRepo, TrackerRepo


class RootCtl(object):
    '''
    Information of service. Read only resource
    '''

    def __init__(self, db):
        '''
        :param pymongo.MongoClient db: Instance of connection to mongodb server
        '''

        self._acc_repo = AccountRepo(db)
        self._tracker_repo = TrackerRepo(db)

    def on_get(self, req, res):
        '''
        Response: Essential information of service
        '''

        res.body = {
            'name': 'gwisp service',
            'notes': 'service to store/retrieve time tracker',
            'version': pkg_resources.get_distribution('gwisp').version,
            'source': 'https://github.com/kevin-leptons/gwisp',
            'doc': 'http://gwisp.readthedocs.io/en/latest/',
            'num_user': self._acc_repo.count(),
            'num_tracker': self._tracker_repo.count()
        }
