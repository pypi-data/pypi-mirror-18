from falcon import HTTPNotFound, HTTPInternalServerError, HTTP_204
from bson import ObjectId

from ..validator import ctl
from ..repo import TrackerRepo, CTrackerRepo


class TrackerUsingCtl(object):
    def __init__(self, db, protector):
        self._tracker_repo = TrackerRepo(db)
        self._protector = protector

    def on_get(self, req, res):
        auth = self._protector.check(req, iacc=True)

        if 'tracker' not in auth.account:
            raise HTTPNotFound(description='No tracker is using')
        target = auth.account['tracker']

        real_item = self._tracker_repo.find_by_id(target['id'])
        if real_item is None:
            raise HTTPInternalServerError(
                title='500 Internal Server Error',
                description='Not found real tracker'
            )

        # mark tracker is updated with real tracker or not
        if real_item['modified'] > target['_cloned_date']:
            target['_updated'] = False
        else:
            target['_updated'] = True

        # remove data
        del target['_cloned_date']

        # modifing data
        target['num_user'] = real_item['num_user']

        res.body = target


class TrackerUsingItemCtl(object):
    def __init__(self, db, protector):
        self._protector = protector
        self._ctracker_repo = CTrackerRepo(db)

    @ctl(None, ObjectId)
    def on_put(self, req, res, id):
        auth = self._protector.check(req)

        self._ctracker_repo.use_tracker(auth.account_id, id)

        res.status = HTTP_204
