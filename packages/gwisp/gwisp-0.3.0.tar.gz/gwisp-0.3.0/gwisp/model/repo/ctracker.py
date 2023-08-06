import copy

from ..lowest.ctracker import attr_id as ctracker_id
from ..repo import tracker as rmodel_tracker


#: Show tracker is cloned by user or not
attr_cloned = {'type': 'boolean'}

#: Show tracker is updated or not
attr_updated = {'type': 'boolean'}

#: Show tracker is using or not
attr_using = {'type': 'boolean'}

find_on_cview = copy.deepcopy(rmodel_tracker.find)
find_on_cview['required'].remove('_id')
find_on_cview['required'].extend(['id', '_updated', '_using'])
find_on_cview['properties'].pop('_id')
find_on_cview['properties'].update({
    'id': ctracker_id,
    '_updated': attr_updated,
    '_using': attr_using
})

find_on_uview = copy.deepcopy(rmodel_tracker.find)
find_on_uview['required'].extend(['_cloned', '_updated', '_using'])
find_on_uview['properties'].update({
    '_cloned': attr_cloned,
    '_updated': attr_updated,
    '_using': attr_using
})

search_on_cview = copy.deepcopy(rmodel_tracker.search)
search_on_cview['items']['required'].remove('_id')
search_on_cview['items']['required'].extend(['id', '_updated', '_using'])
search_on_cview['items']['properties'].pop('_id')
search_on_cview['items']['properties'].update({
    'id': ctracker_id,
    '_updated': attr_updated,
    '_using': attr_using
})

search_on_uview = copy.deepcopy(rmodel_tracker.search)
search_on_uview['items']['required'].extend(['_cloned', '_updated', '_using'])
search_on_uview['items']['properties'].update({
    '_cloned': attr_cloned,
    '_updated': attr_updated,
    '_using': attr_using
})
