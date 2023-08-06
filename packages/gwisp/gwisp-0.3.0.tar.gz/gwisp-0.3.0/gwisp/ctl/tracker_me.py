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
        auth = self._protector.check(req, True)
        selector = parse_selector(req)
        utracker = None
        if 'tracker' in auth.account:
            utracker = auth.account['tracker']

        res.body = self._repo.search_by_author(auth.account_id, selector)
        if res.body is None:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found tracker'
            )
        else:
            for item in res.body:
                # remove data
                del item['author']

                # mark '_using'
                item['_using'] = False
                if utracker is not None:
                    if item['_id'] == utracker['id']:
                        item['_using'] = True
