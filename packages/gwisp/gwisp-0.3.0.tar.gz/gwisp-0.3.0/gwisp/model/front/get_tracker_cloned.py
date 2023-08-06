import copy

from .get_tracker import res_body as get_tracker_res_body
from ..lowest.ctracker import attr_id as lmodel_ctracker_id
from ..repo import ctracker as rmodel_ctracker

res_body = copy.deepcopy(get_tracker_res_body)
res_body['items']['required'].remove('_id')
res_body['items']['required'].extend(['id', '_updated', '_using'])
res_body['items']['properties'].pop('_id')
res_body['items']['properties'].update({
    'id': lmodel_ctracker_id,
    '_updated': rmodel_ctracker.attr_updated,
    '_using': rmodel_ctracker.attr_using
})
res = {'body': res_body}
