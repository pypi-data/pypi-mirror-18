from falcon import HTTPNotFound

from ..repo import TrackerRepo
from ..util import parse_selector


class TrackerMeCtl(object):
    '''
    Allow search trackers by author

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._repo = TrackerRepo(db)
        self._protector = protector

    def on_get(self, req, res):
        auth = self._protector.check(req)
        selector = parse_selector(req)

        res.body = self._repo.search_by_author(auth.account_id, selector)
        if res.body is None:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found tracker'
            )
        else:
            # remove data
            for item in res.body:
                del item['author']
