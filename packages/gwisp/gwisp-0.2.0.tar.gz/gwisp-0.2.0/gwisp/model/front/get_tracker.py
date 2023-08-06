import copy

from ..repo import tracker as rmodel_tracker


res_body = copy.deepcopy(rmodel_tracker.search)

res = {'body': res_body}
