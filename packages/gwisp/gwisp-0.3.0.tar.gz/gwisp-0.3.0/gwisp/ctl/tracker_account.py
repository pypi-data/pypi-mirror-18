from falcon import HTTPNotFound
from bson import ObjectId

from ..util import parse_selector
from ..validator import ctl
from ..repo import CTrackerRepo


class TrackerAccountCtl(object):
    '''
    Allow search trackers on user view

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._repo = CTrackerRepo(db)

    def on_get(self, req, res):
        auth = self._protector.check(req)
        selector = parse_selector(req)

        res.body = self._repo.search_on_uview(auth.account_id, selector)
        if res.body is None:
            raise HTTPNotFound(description='Not found trackers')


class TrackerAccountItemCtl(object):
    '''
    Allow query single shceduler on user view point

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._repo = CTrackerRepo(db)

    @ctl(None, ObjectId)
    def on_get(self, req, res, id):
        auth = self._protector.check(req)

        res.body = self._repo.find_by_id_on_uview(auth.account_id, id)
        if res.body is None:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found tracker'
            )
