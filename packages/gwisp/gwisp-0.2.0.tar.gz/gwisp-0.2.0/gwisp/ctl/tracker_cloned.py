from falcon import HTTPNotFound, HTTP_204
from bson import ObjectId

from ..validator import ctl
from ..util import parse_selector
from ..repo import CTrackerRepo


class TrackerClonedCtl(object):
    def __init__(self, db, protector):
        self._ctracker_repo = CTrackerRepo(db)
        self._protector = protector

    def on_get(self, req, res):
        selector = parse_selector(req)
        auth = self._protector.check(req)

        res.body = self._ctracker_repo.search_on_cview(
            auth.account_id, selector
        )

        if res.body is None:
            raise HTTPNotFound(description='Not found your trackers')

    def on_put(self, req, res):
        auth = self._protector.check(req)

        self._ctracker_repo.update_all_cloned(auth.account_id)

        res.status = HTTP_204


class TrackerClonedItemCtl(object):
    def __init__(self, db, protector):
        self._ctracker_repo = CTrackerRepo(db)
        self._protector = protector

    @ctl(None, ObjectId)
    def on_get(self, req, res, id):
        auth = self._protector.check(req)

        res.body = self._ctracker_repo.find_by_id_on_cview(auth.account_id, id)

        if res.body is None:
            raise HTTPNotFound(description='Not found cloned trackers')

    @ctl(None, ObjectId)
    def on_put(self, req, res, id):
        auth = self._protector.check(req)

        self._ctracker_repo.update_one_cloned(auth.account_id, id)

        res.status = HTTP_204

    @ctl(None, ObjectId)
    def on_post(self, req, res, id):
        auth = self._protector.check(req)

        self._ctracker_repo.clone_one(auth.account_id, id)

        res.status = HTTP_204
        res.append_header(
            'Location', '/tracker/cloned/{}'.format(id)
        )

    @ctl(None, ObjectId)
    def on_delete(self, req, res, id):
        auth = self._protector.check(req)

        self._ctracker_repo.remove_one_cloned(auth.account_id, id)

        res.status = HTTP_204
