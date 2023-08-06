import copy
import jsonschema

from ..repo import tracker as rmodel_tracker


req_body = copy.deepcopy(rmodel_tracker.insert)
req_body['required'].remove('author')
req_body['properties'].pop('author')
req = {'body': req_body}

res_header = {
    'type': 'object',
    'required': ['Location'],
    'properties': {
        'Location': {
            'type': 'string',
            'pattern': '^\/tracker\/[a-fA-F0-9]{24}$'
        }
    }
}
res = {'header': res_header}


def validate_post(item):
    jsonschema.validate(item, req_body)
