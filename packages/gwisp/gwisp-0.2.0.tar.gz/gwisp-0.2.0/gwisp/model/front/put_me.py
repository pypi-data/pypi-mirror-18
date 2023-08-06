from ..lowest import account as lmodel_account


req_body = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'language': lmodel_account.attr_language,
        'avatar': lmodel_account.attr_avatar
    }
}
req = {'body': req_body}
