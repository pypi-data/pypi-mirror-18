import jsonschema

from ..repo import tracker

req_body = tracker.update
req = {'body': req_body}


def validate_put(item):
    jsonschema.validate(item, req_body)
