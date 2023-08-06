import json
import glob
from os import path
from gwisp.repo import TrackerRepo


class DbTool(object):
    '''
    Controll install sample data into database

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param str asset_dir: Path to static asset directory. That's directory
        must contains file specifications. See :ref:`api_asset_dir`
    '''
    def __init__(self, db, protector, asset_dir, account, password):
        self._db = db                   #: Instance of mongodb client
        self._asset_dir = asset_dir     #: Path to asset directory

        self._tracker_repo = TrackerRepo(db)    #: Tracker repository

        #: Register account
        self._account = account
        self._acc_id = protector.create_account(account, password)

    def install(self):
        '''
        Install sample data into database

        :return: Number of data files has been readed
        :rtype: int
        '''

        return self.install_tracker()

    def install_tracker(self):
        '''
        Install sample tracker into database

        :return: Number of data files has been readed
        :rtype: int
        '''

        files = glob.glob(path.join(self._asset_dir, 'tracker-*.json'))
        items = []
        nfiles = 0

        for file in files:
            nfiles += 1

            with open(file) as f:
                item = json.load(f)
                item['author'] = {
                    '_id': self._acc_id,
                    'name': self._account['name']
                }
                items.append(item)

            if len(items) == 128:
                self._tracker_repo.insert_many(items)
                items = []

        if len(items) > 0:
                self._tracker_repo.insert_many(items)

        return nfiles
