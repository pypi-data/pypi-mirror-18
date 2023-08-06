import copy


from ..lowest import tracker
from ..repo import ctracker as rmodel_ctracker


res_body = copy.deepcopy(tracker.storage)
res_body['required'].extend(['_updated'])
res_body['properties'].update({
    '_updated': rmodel_ctracker.attr_updated
})
res = {'body': res_body}
