import copy

from ..lowest import tracker as lmodel_tracker
from ..repo import ctracker as rmodel_ctracker
from ..lowest.ctracker import attr_id as lmodel_ctracker_id

res_body = copy.deepcopy(lmodel_tracker.storage)
res_body['required'].remove('_id')
res_body['required'].extend(['id', '_updated'])
res_body['properties'].pop('_id')
res_body['properties'].update({
    'id': lmodel_ctracker_id,
    '_updated': rmodel_ctracker.attr_updated
})
res = {'body': res_body}
