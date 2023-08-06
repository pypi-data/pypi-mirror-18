import copy

from ..lowest import account


res_body = copy.deepcopy(account.storage)
res_body['required'].remove('tracker')
res_body['properties'].pop('tracker')

res = {'body': res_body}
