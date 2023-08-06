import functools
import jsonschema
from falcon import HTTPBadRequest
from jsonschema import ValidationError
from inspect import getargspec


class ArgTypeError(TypeError):
    '''
    Use to raise exception when Argument type is invalid

    :param string func_name: Name of function
    :param int arg_oder: Order of arugment of function, base on zero
    :param object arg_value: Value of argumen
    :param string req_arg_type: Name of argument type is requiredt
    '''

    def __init__(self, func_name, arg_oder, arg_value, req_arg_type):
        self.error = 'The argument {} of {}() is not a {}. It is {}'.format(
            arg_oder, func_name, req_arg_type, type(arg_value)
        )

    def __str__(self):
        return self.error


class ArgNumberError(TypeError):
    '''
    Use to raise exception when number required arguments is not equal
    with number of function arguments

    :param string fn_name: Name of fucntion
    :param int num_args: Number of arguments in function
    '''

    def __init__(self, fn_name, num_args):
        self.error = 'Required full spec for {} arguments in {}()'.format(
            num_args, fn_name
        )

    def __str__(self):
        return self.error


class CtlArgError(TypeError):
    '''
    Use to raise exception when convert type in pre-controller processing

    :param object arg_value: Data to convert
    :param type req_arg: Required type
    '''

    def __init__(self, arg_value, req_arg):
        self.error = 'Can not convert <{}> to {} type'.format(
            arg_value, req_arg
        )

    def __str__(self):
        return self.error


def validate_args(fn_name, fn_args, req_args):
    '''
    Validate arguments of function. If type of element in req_args is dict,
    supported to validate by jsonschema. If type of element in req_args is,
    type, supported to compare type

    :param string fn_name: Name of function to be check
    :param tuple fn_args: Instance of arguments in order
    :param tuple req_args: Required type of arguments in Order

    :raise gwisp.validator.ArgNumberError: On number of required arguments
        is not enough
    :raise gwisp.validator.ArgTypeError: On type of arguments in function
        is invalid
    :raise jsonschema.exceptions.ValidationError: On value of arguments
        in function invalid jsonschema
    '''

    args = enumerate(zip(fn_args, req_args))

    for arg_num, (fn_arg, req_arg) in args:
        req_arg_type = type(req_arg)

        # check function type vs required type
        if req_arg_type is type:
            if type(fn_arg) is not req_arg:
                raise ArgTypeError(fn_name, arg_num, fn_arg, req_arg)

        # check function value with jsonschema
        elif req_arg_type is dict:
            jsonschema.validate(fn_arg, req_arg)

        # do not supported other case
        else:
            raise TypeError('Does not supported type of arguments')


def method(*req_args):
    '''
    This is decorator. Use to be check type of arguments in methods

    :param req_args: List of required arguments

    :raise gwisp.validator.ArgNumberError: On number of required arguments
        is not enough
    :raise gwisp.validator.ArgTypeError: On type of arguments in function
        is invalid
    :raise jsonschema.exceptions.ValidationError: On value of arguments
        in function invalid jsonschema
    '''

    def accept_decorator(fn):
        @functools.wraps(fn)
        def decorator_wrapper(*fn_args):
            argspec = getargspec(fn)
            fn_args_full = fn_args
            if argspec.defaults is not None:
                default_num = len(argspec.args) - len(fn_args)
                if default_num > 0:
                    fn_args_full = fn_args + argspec.defaults[-default_num:]

            if len(req_args) is not (len(fn_args_full) - 1):
                raise ArgNumberError(fn.__name__, len(fn_args_full))

            validate_args(fn.__name__, fn_args_full[1:], req_args)

            return fn(*fn_args)

        return decorator_wrapper

    return accept_decorator


def validate_req_msg(req_model, req):
    '''
    Validate HTTP message request of falcon.
    If req_model is None, do nothing. If req_model is not None, and it
    does not contains 'header' or 'body' key, TypeError will be raise.

    :param dict req_model: Data model of request in jsonschema. It include
        two key: header and body
    :param falcon.Request req: Request object
    :raise HTTPBadRequest: On request is invalid
    :raise TypeError: On req_model is invalid
    '''

    if req_model is None:
        return

    if 'header' not in req_model and 'body' not in req_model:
        raise TypeError('Request model is invalid')

    if 'body' not in req.context:
        raise HTTPBadRequest('400 Bad Request', 'Body is empty')

    try:
        if 'header' in req_model:
            jsonschema.validate(req.headers, req_model['header'])
        if 'body' in req_model:
            jsonschema.validate(req.context['body'], req_model['body'])
    except ValidationError as e:
        raise HTTPBadRequest(title='400 Bad Request', description=str(e))


def ctl(req_model, *req_args):
    '''
    This is decorator, use to validate request message and route url of
        falcon controller

    :param dict req_model: Data model of request in jsonschema. It include
        two key: header and body
    :param req_args: List of required type of arguments
    :raise HTTPBadRequest: On request is invalid
    :raise TypeError: On req_model is invalid
    '''

    def ctl_decorator(fn):
        @functools.wraps(fn)
        def decorator_wrapper(ctl_obj, req, res, **fn_args):
            # convert and validate route arguments
            route_args = getargspec(fn).args[3:]
            args = enumerate(zip(route_args, req_args))
            new_fn_args = []
            for i, (route_arg, req_arg) in args:
                try:
                    new_fn_args.append(req_arg(fn_args[route_arg]))
                except:
                    raise CtlArgError(fn_args[route_arg], req_arg)

            # validate request message
            validate_req_msg(req_model, req)

            # execute controller
            return fn(ctl_obj, req, res, *new_fn_args)

        return decorator_wrapper

    return ctl_decorator
