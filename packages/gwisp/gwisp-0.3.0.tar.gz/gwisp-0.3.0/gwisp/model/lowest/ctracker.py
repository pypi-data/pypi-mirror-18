import copy

from .ess import account_id
from .tracker import storage as tracker_storage
from .tracker import attr_id as tracker_id

#: Account identity who is used this tracker
attr_cloner = account_id

#: Cloned tracker id
attr_id = tracker_id

#: Cloned date
attr_cloned_date = {
    'type': 'integer'
}

#: Model store in database
storage = copy.deepcopy(tracker_storage)
storage['required'].extend(['id', '_cloner', '_cloned_date'])
storage['properties'].update({
    'id': attr_id,
    '_cloner': attr_cloner,
    '_cloned_date': attr_cloned_date
})
