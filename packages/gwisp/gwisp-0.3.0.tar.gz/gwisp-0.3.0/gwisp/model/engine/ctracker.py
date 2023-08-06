import copy
import jsonschema

from ..lowest import ctracker

#: Model use to validate insert data
insert = copy.deepcopy(ctracker.storage)
insert['required'].remove('_id')
insert['properties'].pop('_id')


def validate_insert(item):
    '''
    Validate insert data

    :param dict item: Data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, insert)
