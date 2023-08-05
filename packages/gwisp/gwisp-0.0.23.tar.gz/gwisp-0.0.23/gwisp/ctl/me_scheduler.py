from falcon import HTTPNotFound, HTTP_204, HTTPBadRequest
from bson import ObjectId

from ..repo import SchedulerRepo, CSchedulerRepo
from ..util import parse_selector


class MeSchedulerCtl(object):
    def __init__(self, db, protector):
        self._repo = CSchedulerRepo(db)
        self._protector = protector

    def on_get(self, req, res):
        auth = self._protector.check(req)
        selector = parse_selector(req)

        res.body = self._repo.search_by_cloner(auth.account_id, selector)

        if len(res.body) == 0:
            raise HTTPNotFound(description='Not found your scheduler')

    def on_put(self, req, res):
        auth = self._protector.check(req)

        self._repo.update_cloner(auth.account_id)

        res.status = HTTP_204


class MeSchedulerItemCtl(object):
    def __init__(self, db, protector):
        self._sched_repo = SchedulerRepo(db)
        self._repo = CSchedulerRepo(db)
        self._protector = protector

    def on_get(self, req, res, id):
        auth = self._protector.check(req)

        try:
            sched_id = ObjectId(id)
        except Exception:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Identity is invalid'
            )

        res.body = self._repo.find_by_cloner_and_id(
            auth.account_id, sched_id
        )
        if res.body is None:
            raise HTTPNotFound(description='Not found cloned scheduler')

    def on_put(self, req, res, id):
        auth = self._protector.check(req)

        sched_id = None
        try:
            sched_id = ObjectId(id)
        except Exception:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Identity is invalid'
            )

        self._repo.sync_cloned(auth.account_id, sched_id)

        res.status = HTTP_204

    def on_post(self, req, res, id):
        auth = self._protector.check(req)

        sched_id = None
        try:
            sched_id = ObjectId(id)
        except Exception:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Identity is invalid'
            )

        real_item = self._sched_repo.find_by_id(sched_id)
        if real_item is None:
            raise HTTPNotFound(description='Not found scheduler')

        self._repo.clone_one(auth.account_id, real_item)

        res.status = HTTP_204
        res.append_header(
            'Location', '/me/scheduler/{}'.format(real_item['_id'])
        )

    def on_delete(self, req, res, id):
        auth = self._protector.check(req)

        sched_id = None
        try:
            sched_id = ObjectId(id)
        except Exception:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Identity is invalid'
            )

        self._repo.remove_cloned(auth.account_id, sched_id)

        res.status = HTTP_204
