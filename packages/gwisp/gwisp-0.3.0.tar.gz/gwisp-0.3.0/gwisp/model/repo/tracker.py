import copy
import jsonschema

from ..lowest import tracker as lmodel_tracker


#: Model use to validate insert data
insert = copy.deepcopy(lmodel_tracker.storage)
insert['required'].remove('_id')
insert['required'].remove('modified')
insert['required'].remove('num_user')
insert['properties'].pop('_id')
insert['properties'].pop('modified')
insert['properties'].pop('num_user')

#: Model use to validate insert multi data
insert_many = {
    'type': 'array',
    'items': insert
}

#: Model use to validate update data
update = copy.deepcopy(lmodel_tracker.storage)
update.pop('required')
update['properties'].pop('_id')
update['properties'].pop('author')
update['properties'].pop('name')
update['properties'].pop('modified')


search = {
    'type': 'array',
    'items': {
        'type': 'object',
        'additionalProperties': False,
        'required': ['_id', 'author', 'name', 'num_user', 'modified'],
        'properties': {
            '_id': lmodel_tracker.attr_id,
            'author': lmodel_tracker.attr_author,
            'name': lmodel_tracker.attr_name,
            'num_user': lmodel_tracker.attr_num_user,
            'modified': lmodel_tracker.attr_modified
        }
    }
}

find = copy.deepcopy(lmodel_tracker.storage)


def validate_insert(items):
    '''
    Validate data use to insert

    :param object items: List or single of data to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    if type(items) is list:
        for item in items:
            jsonschema.validate(item, insert)
    else:
        jsonschema.validate(items, insert)


def validate_update(items):
    '''
    Validate data use to update

    :param object items: List or single of data use to update
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    if type(items) is list:
        for item in items:
            jsonschema.validate(items, update)
    else:
        jsonschema.validate(items, update)
