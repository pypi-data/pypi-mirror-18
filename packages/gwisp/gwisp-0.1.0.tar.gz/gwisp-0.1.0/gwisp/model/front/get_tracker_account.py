import copy

from .get_tracker import res_body as get_tracker_res_body
from ..repo import ctracker as rmodel_ctracker


res_body = copy.deepcopy(get_tracker_res_body)
res_body['items']['required'].extend(['_cloned', '_updated'])
res_body['items']['properties'].update({
    '_cloned': rmodel_ctracker.attr_cloned,
    '_updated': rmodel_ctracker.attr_updated
})
res = {'body': res_body}
