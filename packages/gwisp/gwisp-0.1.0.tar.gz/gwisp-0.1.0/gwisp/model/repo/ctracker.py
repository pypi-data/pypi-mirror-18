import copy

from ..repo import tracker as rmodel_tracker


#: Show tracker is cloned by user or not
attr_cloned = {'type': 'boolean'}

#: Show tracker is updated or not
attr_updated = {'type': 'boolean'}

find_on_cview = copy.deepcopy(rmodel_tracker.find)
find_on_cview['required'].extend(['_updated'])
find_on_cview['properties'].update({
    '_updated': attr_updated
})

find_on_uview = copy.deepcopy(rmodel_tracker.find)
find_on_uview['required'].extend(['_cloned', '_updated'])
find_on_uview['properties'].update({
    '_cloned': attr_cloned,
    '_updated': attr_updated
})

search_on_cview = copy.deepcopy(rmodel_tracker.search)
search_on_cview['items']['required'].extend(['_updated'])
search_on_cview['items']['properties'].update({
    '_updated': attr_updated
})

search_on_uview = copy.deepcopy(rmodel_tracker.search)
search_on_uview['items']['required'].extend(['_cloned', '_updated'])
search_on_uview['items']['properties'].update({
    '_cloned': attr_cloned,
    '_updated': attr_updated
})
