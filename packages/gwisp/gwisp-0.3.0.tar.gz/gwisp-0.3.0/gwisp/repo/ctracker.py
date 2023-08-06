import re
from math import ceil
from time import time
from bson import ObjectId

from .tracker import TrackerRepo

from ..error import NotExistError
from ..util import Selector
from ..validator import method
from ..model.engine import ctracker as emodel_ctracker


search_by_author_fields = {
    'tags': 0, 'tasks': 0, 'notes': 0
}
search_by_cloner_fields = {
    'tags': 0, 'tasks': 0, 'notes': 0, '_cloner': 0
}


class CTrackerRepo(object):
    '''
    Provide methods to manage cloned trackers. It will help user use
    trackers without affected from updating by author of trackers

    :param pymongo.MongoClient db: Instance of connection to mongdb server
    '''
    def __init__(self, db):
        self._tracker_repo = TrackerRepo(db)
        self._tracker_coll = db['tracker']
        self._ctracker_coll = db['ctracker']
        self._acc_coll = db['account']

    @method(ObjectId, ObjectId)
    def clone_one(self, cloner, tracker_id):
        '''
        Create an cloned tracker belong account if it is not early cloned.
        Replace data of tracker if it is early cloned

        :param bson.objectid.ObjectId cloner: Account identity
            which is clone tracker
        :param bson.objectid.ObjectId tracker_id: Tracker identity to clone
        '''

        # Find tracker to clone
        real_tracker = self._tracker_repo.find_by_id(tracker_id)
        if real_tracker is None:
            raise NotExistError('Tracker is not exist')

        # padding data
        real_tracker['id'] = tracker_id
        real_tracker['_cloner'] = cloner
        real_tracker['_cloned_date'] = int(time())

        # remove data
        del real_tracker['_id']

        # modifing data
        real_tracker['num_user'] += 1

        # validate data
        emodel_ctracker.validate_insert(real_tracker)

        # insert or update tracker depend on it is early exists or not
        if (self._is_exist(cloner, tracker_id)):
            self._ctracker_coll.update_one(
                {'id': tracker_id, '_cloner': cloner},
                {'$set': real_tracker}
            )
        else:
            self._ctracker_coll.insert_one(real_tracker)

        # update real tracker
        self._tracker_coll.update_one(
            {'_id': tracker_id},
            {'$inc': {'num_user': 1}}
        )

    @method(ObjectId, Selector)
    def search_on_uview(self, observer, selector=Selector()):
        '''
        Search trackers on user view correspond with observer.
        On that view, observer see that trackers is cloned by they or not.
        And if trackers is cloned by they, it is updated with real trackers
        or not.
        Two field are added to each trackers: **_cloned** and **_updated**

        :param bson.objectid.ObjectId observer: Identity of account
        :param gwisp.Selector selector: Keyword and pagging information
        :return: List of tracker match with selector. None on not found
        :rtype: list
        :rtype: None
        '''

        # find tracker is using by cloner
        account = self._acc_coll.find_one({'_id': observer})
        utracker = None
        if 'tracker' in account:
            utracker = account['tracker']

        # search real trackers
        real_items = self._tracker_repo.search(selector)
        if real_items is None:
            return None

        # search cloned trackers of account
        real_ids = [i['_id'] for i in real_items]
        cloned_cusor = self._ctracker_coll.find({
            '_cloner': observer,
            'id': {'$in': real_ids}
        })
        cloned_items = list(cloned_cusor)

        # compare real and cloned trackers to mark '_cloned', '_updated'
        # and '_using'
        cloned_ids = [i['id'] for i in cloned_items]
        cloned_index = {i['id']: i for i in cloned_items}
        for item in real_items:

            # tracker is not cloned
            if item['_id'] not in cloned_ids:
                item['_cloned'] = False
                item['_updated'] = False
                item['_using'] = False
                continue

            # tracker is cloned
            item['_cloned'] = True
            cloned_item = cloned_index[item['_id']]
            if item['modified'] > cloned_item['_cloned_date']:
                item['_updated'] = False
            else:
                item['_updated'] = True

            # mark '_using'
            item['_using'] = False
            if utracker is not None:
                if utracker['id'] == item['_id']:
                    item['_using'] = True

        return real_items

    @method(ObjectId, Selector)
    def search_on_cview(self, cloner, selector=Selector()):
        '''
        Search cloned trackers on cloner view itself. On that view,
        cloner see that cloned trackers is updated with real trackers
        or not. One field added: '_updated'

        :param bson.objectid.ObjectId cloner: Account identity
        :param gwisp.Selector selector: Search information
        :return: List of trackers was found. None on not found
        :rtype: list
        '''

        # find tracker is using by cloner
        account = self._acc_coll.find_one({'_id': cloner})
        utracker = None
        if 'tracker' in account:
            utracker = account['tracker']

        # search trackers is cloned by account
        filters = {'$and': [{'_cloner': cloner}]}
        if selector.keyword is not None:
            filters['$and'].append(self._gen_filter(selector.keyword))

        cloned_cusor = self._ctracker_coll.find(
            filters,
            search_by_cloner_fields,
            skip=selector.skip,
            limit=selector.page_size
        )
        cloned_items = list(cloned_cusor)
        if len(cloned_items) == 0:
            return None

        # search real trackers correspond with cloned trackers
        cloned_ids = [i['id'] for i in cloned_items]
        real_items = self._tracker_coll.find(
            {'_id': {'$in': cloned_ids}},
            {'notes': 0, 'tags': 0, 'tasks': 0, 'author': 0}
        )

        # compare cloned trackers with real trackers to mark '_updated'
        # and '_using'
        real_indexs = {i['_id']: i for i in real_items}
        for item in cloned_items:
            del item['_id']

            if real_indexs[item['id']]['modified'] > item['_cloned_date']:
                item['_updated'] = False
            else:
                item['_updated'] = True

            # remove data
            del item['_cloned_date']

            # set number user of real item
            item['num_user'] = real_indexs[item['id']]['num_user']

            item['_using'] = False
            if utracker is not None:
                if utracker['id'] == item['id']:
                    item['_using'] = True

        return cloned_items

    @method(ObjectId, ObjectId)
    def find_by_id_on_uview(self, observer, tracker_id):
        '''
        Find one tracker on user view correspond with observer.
        On that view, observer see that tracker is cloned by they or not.
        And if tracker is cloned by they, it is updated with real tracker
        or not. Two fields are added: **_cloned** and **_updated**

        :param bson.objectid.ObjectId observer: Account identity
        :param bson.objectid.ObjectId tracker_id: Tracker identity
        :return dict: Real tracker data on found. None on not found
        :rtype: dict
        :rtype: None
        '''

        # find tracker is using by cloner
        account = self._acc_coll.find_one({'_id': observer})
        utracker = None
        if 'tracker' in account:
            utracker = account['tracker']

        # search real tracker
        real_item = self._tracker_repo.find_by_id(tracker_id)
        if real_item is None:
            return None

        # search cloned tracker
        cloned_item = self._ctracker_coll.find_one({
            'id': tracker_id,
            '_cloner': observer
        })

        # tracker is not cloned
        if cloned_item is None:
            real_item['_cloned'] = False
            real_item['_updated'] = False
            real_item['_using'] = False
            return real_item

        # tracker is cloned, mark '_updated' field
        real_item['_cloned'] = True

        if real_item['modified'] > cloned_item['_cloned_date']:
            real_item['_updated'] = False
        else:
            real_item['_updated'] = True

        # mark '_using'
        real_item['_using'] = False
        if utracker is not None:
            if utracker['id'] == real_item['_id']:
                real_item['_using'] = True

        return real_item

    @method(ObjectId, ObjectId)
    def find_by_id_on_cview(self, cloner, tracker_id):
        '''
        Find cloned tracker on cloner view itself. On that view, cloner see
        that cloned tracker is updated with real tracker or not.
        One field added: ‘_updated’

        :param bson.objectid.ObjectId cloner: Cloner identity
        :param bson.objectid.ObjectId tracker_id: Tracker identity
        :return: Cloned tracker data on found. None on not found
        :rtype: dict
        :rtype: None
        '''

        # find tracker is using by cloner
        account = self._acc_coll.find_one({'_id': cloner})
        utracker = None
        if 'tracker' in account:
            utracker = account['tracker']

        # find real tracker
        real_item = self._tracker_repo.find_by_id(tracker_id)
        if real_item is None:
            return None

        # find cloned tracker
        cloned_item = self._ctracker_coll.find_one(
            {'id': tracker_id, '_cloner': cloner}
        )
        if cloned_item is None:
            return None
        del cloned_item['_id']

        # compare real and cloned tracker to mark '_updated' field
        if real_item['modified'] > cloned_item['_cloned_date']:
            cloned_item['_updated'] = False
        else:
            cloned_item['_updated'] = True

        # compare real and cloned tracker to mark '_using' field
        cloned_item['_using'] = False
        if utracker is not None:
            if utracker['id'] == cloned_item['id']:
                cloned_item['_using'] = True

        # remove data
        del cloned_item['_cloner']
        del cloned_item['_cloned_date']

        # modifing data
        cloned_item['num_user'] = real_item['num_user']

        return cloned_item

    @method(ObjectId, ObjectId)
    def use_tracker(self, account_id, tracker_id):
        '''
        Make account with account_id use tracker with tracker_id.
        If tracker is not cloned, clone it.
        Then copy cloned version to account.tracker

        :param bson.objectid.ObjectId account_id: Account identity
        :param bson.objectid.ObjectId tracker_id: Tracker identity
        '''

        # find cloned tracker
        cloned_item = self._ctracker_coll.find_one({
            '_cloner': account_id,
            'id': tracker_id
        })

        # if tracker is not cloned, clone it
        if cloned_item is None:
            cloned_item = self._tracker_repo.find_by_id(tracker_id)
            if cloned_item is None:
                raise NotExistError('Tracker is not exists')

            cloned_item['id'] = tracker_id
            cloned_item['_cloner'] = account_id
            cloned_item['_cloned_date'] = int(time())
            cloned_item['num_user'] += 1

            del cloned_item['_id']

            self._ctracker_coll.insert_one(cloned_item)

            # update real tracker
            self._tracker_coll.update_one(
                {'_id': tracker_id},
                {'$inc': {'num_user': 1}}
            )

        # copy cloned tracker to account.tracker
        if '_id' in cloned_item:
            del cloned_item['_id']
        del cloned_item['_cloner']
        self._acc_coll.update_one(
            {'_id': account_id},
            {'$set': {'tracker': cloned_item}}
        )

    @method(ObjectId)
    def update_all_cloned(self, cloner):
        '''
        Update all of cloned trackers is cloned by cloner with real
        trackers

        :param bson.objectid.ObjectId cloner: Account identity
        '''

        # find trackers is using by account
        account = self._acc_coll.find_one(
            {'_id': cloner},
            {'email': 0, 'avatar': 0, 'groups': 0, 'subject': 0}
        )
        if account is None:
            raise NotExistError('Account is not exist')

        # prepare for cloned trackers
        number_item = self._ctracker_coll.count({'_cloner': cloner})
        page_size = 16
        number_of_page = ceil(number_item / page_size)

        # clone each page of trackers
        for page_index in range(number_of_page):
            # query page of cloned trackers
            cloned_cusor = self._ctracker_coll.find(
                {'_cloner': cloner},
                {
                    'tags': 0, 'tasks': 0, 'notes': 0, 'author': 0,
                    'modified': 0
                },
                skip=page_index*page_size,
                limit=page_size
            )
            cloned_items = list(cloned_cusor)

            # query page of real trackers
            cloned_ids = [i['id'] for i in cloned_items]
            real_cusor = self._tracker_coll.find(
                {'_id': {'$in': cloned_ids}}
            )
            real_items = list(real_cusor)

            # find trackers is using by account then update
            # and padding meta data for each real trackers
            for item in real_items:
                item['id'] = item['_id']
                item['_cloned_date'] = int(time())

                del item['_id']

                if 'tracker' in account:
                    if item['id'] == account['tracker']['id']:
                        self._acc_coll.update_one(
                            {'_id': cloner},
                            {'$set': {'tracker': item}}
                        )

                item['_cloner'] = cloner

            # remove all of cloned trackers in page by cloner
            self._ctracker_coll.remove({
                '_cloner': cloner,
                'id': {'$in': cloned_ids},
            })

            # create new cloned trackers
            self._ctracker_coll.insert(real_items)

    @method(ObjectId, ObjectId)
    def update_one_cloned(self, cloner, tracker_id):
        '''
        Update one cloned tracker.
        If tracker is using by cloner, update it

        :param bson.objectid.ObjectId cloner: Account identity
        :param bson.objectid.ObjectId tracker_id: Tracker identity
        '''

        # find real tracker
        real_item = self._tracker_coll.find_one({'_id': tracker_id})
        if real_item is None:
            raise NotExistError('Not found tracker')

        # find account
        account = self._acc_coll.find_one({'_id': cloner})
        if account is None:
            raise NotExistError('Account is not exist')

        # find cloned tracker
        cloned_item = self._ctracker_coll.find_one({
            'id': tracker_id,
            '_cloner': cloner
        })
        if cloned_item is None:
            raise NotExistError('Tracker is not cloned')

        # padding meta data to tracker
        real_item['id'] = tracker_id
        real_item['_cloned_date'] = int(time())

        del real_item['_id']

        # update using tracker if match
        if 'tracker' in account and account['tracker']['id'] == tracker_id:
                self._acc_coll.update_one(
                    {'_id': cloner},
                    {'$set': {'tracker': real_item}}
                )

        # update cloned tracker
        self._ctracker_coll.update_one(
            {'id': tracker_id, '_cloner': cloner},
            {'$set': real_item}
        )

    @method(ObjectId, ObjectId)
    def remove_one_cloned(self, cloner, tracker_id):
        '''
        Remove cloned tracker from account.
        If cloned tracker is using by account, remove it

        :param bson.objectid.ObjectId cloner: Account identity
        :param bson.objectid.ObjectId tracker_id: Tracker identity
        '''

        # remove cloned tracker
        result = self._ctracker_coll.delete_one({
            'id': tracker_id,
            '_cloner': cloner
        })
        if result.deleted_count == 0:
            raise NotExistError('Tracker is not exist')

        # remove using tracker if match
        account = self._acc_coll.find_one({'_id': cloner})
        if account is None:
            raise NotExistError('Account is not exist')
        if 'tracker' in account and account['tracker']['id'] == tracker_id:
            self._acc_coll.update_one(
                {'_id': cloner},
                {'$unset': {'tracker': None}}
            )

    @method(ObjectId, ObjectId)
    def _is_exist(self, account_id, tracker_id):
        '''
        Check tracker is cloned by account

        :param bson.objectid.ObjectId account_id: Account identity
        :param bson.objectid.ObjectId tracker_id: Tracker identity
        :return: True on tracker is cloned by account
        :return: False on tracker is not cloned by account
        :rtype: bool
        '''

        key = {'_cloner': account_id, 'id': tracker_id}
        return self._ctracker_coll.find_one(key) is not None

    def _gen_filter(self, keyword):
        '''
        Generate query filter of mongodb

        :param str keyword: Keyword to search
        :return: Filter
        :rtype: dict
        '''
        return {'$or': [
            {'name': {'$regex': re.compile(keyword)}},
            {'tags': {
                '$elemMatch': {
                    '$regex': re.compile(keyword)
                }
            }}
        ]}
