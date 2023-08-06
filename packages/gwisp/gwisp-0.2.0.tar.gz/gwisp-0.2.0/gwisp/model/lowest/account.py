import copy
import jsonschema

from .ess import account_id, account_name, email, url
from .tracker import storage as tracker_storage


#: Identity
attr_id = account_id

#: Name
attr_name = account_name

#: Email
attr_email = email

#: Identity of oauth account
attr_subject = {
    'type': 'string'
}

#: Groups which is account belong
attr_groups = {
    'type': 'array',
    'items': {
        'type': 'string',
        'pattern': '^[a-z0-9]{1,8}$'
    }
}

#: Tracker using by account
attr_tracker = copy.deepcopy(tracker_storage)
attr_tracker['required'].extend(['_cloned_date'])
attr_tracker['properties'].update({
    '_cloned_date': {'type': 'integer'}
})

#: Language
attr_language = {
    'type': 'string',
    'pattern': '^[a-z]{2}$'
}

#: Avatar link
attr_avatar = url

#: Model store in database
storage = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        '_id', 'name', 'email',
        'groups', 'language', 'avatar', 'tracker'
    ],
    'properties': {
        '_id': attr_id,
        'name': attr_name,
        'groups': attr_groups,
        'language': attr_language,
        'avatar': attr_avatar,
        'email': attr_email,
        'subject': attr_subject,
        'tracker': attr_tracker
    }
}


def validate_groups(groups):
    '''
    Validate groups of account

    :param object item: Account object
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(groups, attr_groups)
