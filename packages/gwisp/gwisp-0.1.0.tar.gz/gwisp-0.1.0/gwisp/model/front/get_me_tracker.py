import copy

from ..lowest import tracker as lmodel_tracker
from ..repo import ctracker as rmodel_ctracker


res_body = copy.deepcopy(lmodel_tracker.storage)
res_body['required'].extend(['_updated'])
res_body['properties'].update({
    '_updated': rmodel_ctracker.attr_updated
})
res = {'body': res_body}
