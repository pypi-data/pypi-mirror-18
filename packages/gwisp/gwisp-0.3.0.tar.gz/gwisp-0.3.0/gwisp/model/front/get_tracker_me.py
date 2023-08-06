import copy

from .get_tracker import res_body as get_tracker_res_body
from ..repo import ctracker as rmodel_ctracker


res_body = copy.deepcopy(get_tracker_res_body)
res_body['items']['required'].remove('author')
res_body['items']['required'].extend(['_using'])
res_body['items']['properties'].pop('author')
res_body['items']['properties'].update({
    '_using': rmodel_ctracker.attr_using
})
res = {'body': res_body}
