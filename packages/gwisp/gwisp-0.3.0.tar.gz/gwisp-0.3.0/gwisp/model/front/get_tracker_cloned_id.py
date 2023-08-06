import copy


from ..lowest import tracker
from ..lowest.ctracker import attr_id as lmodel_ctracker_id
from ..repo import ctracker as rmodel_ctracker


res_body = copy.deepcopy(tracker.storage)
res_body['required'].remove('_id')
res_body['required'].extend(['id', '_updated', '_using'])
res_body['properties'].pop('_id')
res_body['properties'].update({
    'id': lmodel_ctracker_id,
    '_updated': rmodel_ctracker.attr_updated,
    '_using': rmodel_ctracker.attr_using
})
res = {'body': res_body}
