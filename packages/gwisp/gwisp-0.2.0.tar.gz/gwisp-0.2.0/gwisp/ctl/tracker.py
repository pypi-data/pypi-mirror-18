from falcon import HTTP_204, HTTP_404, \
                   HTTPNotFound, HTTPForbidden
from bson.objectid import ObjectId

from ..error import NotExistError
from ..util import parse_selector
from ..validator import ctl
from ..repo import TrackerRepo
from ..model.front.post_tracker import req as fmodel_post
from ..model.front.put_tracker_id import req as fmodel_put


class TrackerCtl(object):
    '''
    Tracker resource

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._repo = TrackerRepo(db)

    def on_get(self, req, res):
        '''
        Search trackers

        Request: Query parameters as selector

        Response: List of trackers match with selector
        '''

        res.body = self._repo.search(parse_selector(req))

        if res.body is None:
            res.status = HTTP_404

    @ctl(fmodel_post)
    def on_post(self, req, res):
        '''
        Create new tracker

        Request: Tracker in body, access token in header

        Response: Relative location of new Tracker in header, field
            Location
        '''

        auth = self._protector.check(req, iacc=True)
        item = req.context['body']

        # padding data
        item['author'] = {
            '_id': auth.account_id,
            'name': auth.account['name']
        }

        # save tracker to storage
        inserted_id = self._repo.insert_one(item)

        res.status = HTTP_204
        res.set_header('Location', '/tracker/{}'.format(inserted_id))


class TrackerItemCtl(object):
    '''
    Tracker resource

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._repo = TrackerRepo(db)
        self._protector = protector

    @ctl(None, ObjectId)
    def on_get(self, req, res, id):
        '''
        Query single tracker

        Request: Identify of tracker in request url

        Response: Tracker in body
        '''

        res.body = self._repo.find_by_id(id)

        if res.body is None:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found tracker'
            )

    @ctl(fmodel_put, ObjectId)
    def on_put(self, req, res, id):
        '''
        Update tracker

        Request:
            - Identify of tracker in request url
            - Tracker content in body
            - Authorization header

        Response: No Content
        '''

        auth = self._protector.check(req)
        old_item = self._repo.find_by_id(id)
        if old_item is None:
            raise NotExistError('Tracker is not exist')
        if old_item['author']['_id'] != auth.account_id:
            raise HTTPForbidden(
                title='403 Forbidden',
                description='Can not update item of other account'
            )

        # put data to storage
        self._repo.update_one(id, req.context['body'])

        # result is no content
        res.status = HTTP_204

    @ctl(None, ObjectId)
    def on_delete(self, req, res, id):
        '''
        Remove tracker

        Request: Identify of tracker in request url
        '''

        # authenticate
        auth = self._protector.check(req)

        # ensure item is exist
        item = self._repo.find_by_id(id)
        if item is None:
            raise HTTPNotFound(description='Tracker is not exist')

        # ensure only owner have permission to delete item
        if item['author']['_id'] != auth.account_id:
            raise HTTPForbidden(
                title='403 Forbidden',
                description='Can not delete item of other account'
            )

        # remove item from storage
        self._repo.delete_one(id)

        # result is no content
        res.status = HTTP_204
