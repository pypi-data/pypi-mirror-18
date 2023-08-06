import copy

from .get_tracker import res_body as get_tracker_res_body


res_body = copy.deepcopy(get_tracker_res_body)
res_body['items']['required'].remove('author')
res_body['items']['properties'].pop('author')
res = {'body': res_body}
