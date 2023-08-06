import logging
from papi.request import parse_request_middleware
from papi.method_override_middleware import method_override_middleware
from papi.exceptions import RestException, \
                            MalformedException, \
                            NotFoundException, \
                            MethodNotAllowedException, \
                            NotAcceptableException, \
                            ConflictException, \
                            UnsupportedMediaException, \
                            ResourceException
from traceback import format_exc
import json
import papi.fp as fp
from functools import partial
from papi.hateoas import hateoas
from papi.mime import match_mime, mime_str, parse_mime_type

logger = logging.getLogger(__name__)

def uncaught_exceptions_middleware(app):
    def wrapped(env, start_response):
        try:
            return app(env, start_response)
        except Exception as e:
            logger.error("Uncaught exception", exc_info=True)
            start_response('500 Internal Server Error',
                [('Content-Type', 'text/json')])
            return '{"error":"internal server error"}'
    return wrapped

def serve_resource(resource, response_writers=None):
    if isinstance(response_writers, dict):
        response_writers = response_writers.items()
    def application(environ, start_response):
        try:
            request = fp.assocs(
                        [
                            ('consumed_path', ()),
                            ('remaining_path', fp.path(['request', 'path'], environ)),
                            ('response_writers', response_writers or []),
                        ],
                        environ['request'])
            try:
                status, headers, body = handle_resource(resource, request)
            except ResourceException as e:
                e.raise_as_rest_exception()
        except RestException as e:
            status = e.get_http_status()
            status_code, status_msg = status
            headers = [('Content-type', 'text/plain;charset=utf8')]
            body = status_msg
        status_str = "{0} {1}".format(*status)
        start_response(status_str, headers)
        if type(body) is str:
            body = body.encode('utf8')
        return body
    middlewares = fp.chain(
        uncaught_exceptions_middleware,
        method_override_middleware,
        parse_request_middleware)
    return middlewares(application)

def handle_resource(resource, request, parent_resource=None):
    if resource is None:
        raise NotFoundException
    remaining_path = fp.prop('remaining_path', request)
    if len(remaining_path) == 0:
        return handle_resource_self(
            resource,
            request,
            parent_resource=parent_resource)
    else:
        child_name, new_request = consume_path_item(request)
        if not hasattr(resource, 'get_child'):
            raise NotFoundException
        child = resource.get_child(child_name)
        if child is None:
            raise NotFoundException
        return handle_resource(
            child,
            new_request,
            parent_resource=resource)

def handle_resource_self(resource, request, parent_resource):
    method = fp.prop('method', request).upper()
    if method == 'GET':
        return handle_resource_get(resource, request, parent_resource)
    elif method == 'POST':
        return handle_resource_post(resource, request, parent_resource)
    elif method == 'PUT':
        return handle_resource_put(resource, request, parent_resource)
    elif method == 'DELETE':
        return handle_resource_delete(resource, request, parent_resource)
    else:
        raise MethodNotAllowedException

def handle_resource_get(resource, request, parent_resource):
    if resource is None:
        raise NotFoundException
    accepts = fp.prop('accept', request)
    for mime_pattern in accepts:
        accepted = handle_resource_get_typed(mime_pattern, resource, request)
        if accepted is not None:
            return accepted
    raise NotAcceptableException

def handle_resource_put(resource, request, parent_resource):
    if parent_resource is None:
        raise NotFoundException
    content_type = fp.prop('content_type', request)
    path = fp.prop('consumed_path', request)
    name = fp.last(path)
    if not hasattr(parent_resource, 'store'):
        raise MethodNotAllowedException

    input = fp.prop('input',  request)
    name, body = parent_resource.store(input, name, content_type)

    return make_json_response(hateoas(path, body))

def handle_resource_delete(resource, request, parent_resource):
    if parent_resource is None:
        raise NotFoundException
    path = fp.prop('consumed_path', request)
    name = fp.last(path)
    if not hasattr(parent_resource, 'delete'):
        raise MethodNotAllowedException

    parent_resource.delete(name)

    return make_empty_response()

def handle_resource_post(resource, request, parent_resource):
    if resource is None:
        raise NotFoundException
    content_type = fp.prop('content_type', request)
    path = fp.prop('consumed_path', request)
    if not hasattr(resource, 'create'):
        raise MethodNotAllowedException

    input = fp.prop('input',  request)
    name, body = resource.create(input, content_type)

    return make_json_response(hateoas(fp.snoc(name, path), body))

def handle_resource_get_typed(mime_pattern, resource, request):
    binary_response = handle_resource_get_binary(mime_pattern, resource, request)
    if binary_response is not None:
        return binary_response
    return handle_resource_get_structured(mime_pattern, resource, request)

def resource_accepts_ranges(resource):
    return hasattr(resource, 'get_typed_body_range')

def parse_range_header(s):
    try:
        unit, rhs = tuple(s.split('=', 1))
    except ValueError:
        raise ResourceException(ResourceException.reason_malformed)
    if unit != 'bytes':
        # Only 'bytes' range is supported
        raise ResourceException(ResourceException.out_of_range)
    try:
        start_str, end_str = tuple(rhs.split('-'))
        start = int(start_str)
        end = int(end_str)
    except ValueError:
        raise ResourceException(ResourceException.reason_malformed)
    return (start, end)

def handle_resource_get_binary(mime_pattern, resource, request):
    if not hasattr(resource, 'get_typed_body'):
        return None
    accepts_ranges = resource_accepts_ranges(resource)
    range_header = request['headers'].get('Range')
    if range_header is None:
        byte_range = None
    else:
        byte_range = parse_range_header(range_header)
    if byte_range is None or not accepts_ranges:
        matched = resource.get_typed_body(mime_pattern)
    else:
        matched = resource.get_typed_body_range(mime_pattern, byte_range)
    if matched is None:
        return None
    if byte_range is None:
        mime_type, body = matched
        actual_range = None
    else:
        mime_type, body, actual_range = matched
    return make_binary_response(
        mime_type, body,
        range=actual_range,
        accepts_ranges=accepts_ranges)

def get_resource_digest(resource):
    try:
        digest = resource.get_structured_body(digest=True)
    except AttributeError:
        digest = resource
    return digest

def get_resource_body(resource):
    try:
        digest = resource.get_structured_body()
    except AttributeError:
        digest = resource
    return digest

def get_resource_response_writers(resource):
    try:
        response_writers = resource.get_response_writers()
    except AttributeError:
        response_writers = []
    if isinstance(response_writers, dict):
        response_writers = response_writers.items()
    return [(parse_mime_type(k), v) for k, v in response_writers]

def int_param(key, request):
    p = fp.path(('query', key), request)
    if p is None or p == '':
        return None
    return int(p)

class Filter(object):
    def __init__(self, propname, value, operator):
        self.propname = propname
        self.value = value
        self.operator = operator

def parse_filter(src):
    propname, raw_value = tuple(src.split(':', 1))
    return Filter(propname, raw_value, "equals")

def parse_filters_param(key, request):
    p = fp.path(('query', key), request)
    if p is None or p == '':
        return None
    return tuple(map(parse_filter, p.split(',')))

def handle_resource_get_structured(mime_pattern, resource, request):
    if hasattr(resource, 'get_structured_body'):
        raw_body = resource.get_structured_body()
    else:
        raw_body = {}
    current_path = fp.prop('consumed_path', request)
    name = fp.last(current_path)

    offset = int_param('offset', request)
    page = int_param('page', request)
    count = int_param('count', request)
    filters = parse_filters_param('where', request)
    if offset is None and count is not None and page is not None:
        offset = (page - 1) * count

    body = hateoas(current_path, raw_body)

    if hasattr(resource, 'get_children'):
        children = resource.get_children(
            offset=offset,
            count=count,
            filters=filters)
    else:
        children = None
    if children is not None:
        children_alist = [
            (k, get_resource_digest(v)) for k, v in children
        ]

        def prepare_child(kv):
            name, value = kv
            if not isinstance(value, dict):
                value = {'_value': value}
            return fp.chain(
                    partial(fp.assoc, '_name', name),
                    partial(hateoas, fp.snoc(name, current_path))
                )(value)

        children_list = list(map(prepare_child, children_alist))
        body['_items'] = children_list
    if name is not None:
        body['_name'] = name

    response_writers = fp.concat([
        fp.prop('response_writers', request) or [],
        get_resource_response_writers(resource) or [],
        default_response_writers,
    ])
    query = fp.prop('query', request)
    for mime_type, response_writer in response_writers:
        if match_mime(mime_pattern, mime_type, ["charset"]):
            converted = response_writer(body, **query)
            return make_binary_response(mime_type, converted)

def json_writer(data, **query):
    kwargs = {}
    if query.get('pretty'):
        kwargs['indent'] = 2
    return json.dumps(data, **kwargs)

default_response_writers = [
    (parse_mime_type(k), v)
    for (k, v)
    in [
        ('text/json', json_writer),
        ('application/json', json_writer),
       ]
]

def consume_path_item(request):
    first_item = fp.head(fp.prop('remaining_path', request))
    if first_item is None:
        return None, request
    new_request = fp.chain(
        partial(
            fp.Lens.over,
            fp.prop_lens('remaining_path'),
            partial(fp.drop, 1)),
        partial(
            fp.Lens.over,
            fp.prop_lens('consumed_path'),
            partial(fp.snoc, first_item)))(request)
    return first_item, new_request

def make_json_response(
        data,
        status=200,
        headers=None):
    content_type = 'application/json'
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = json.dumps(data)
    if type(body) is str:
        body = body.encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

def make_binary_response(
        mime_type,
        data,
        status=None,
        headers=None,
        range=None,
        accepts_ranges=False):
    def_status = 200 if range is None else 206
    status = status or def_status
    content_type = mime_str(mime_type)
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    if range is not None:
        headers.append(('Content-Range', format_range(range)))
    if accepts_ranges:
        headers.append(('Accept-Ranges', 'bytes'))
    if type(data) is bytes:
        body = data
    else:
        body = str(data).encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

def make_empty_response(mime_type=None, status=204, headers=None):
    content_type = mime_str(mime_type or parse_mime_type("text/plain"))
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = b""
    return ((status, status_names.get(status, 'OK')), headers, body)

def format_range(range):
    return "bytes {0}-{1}/{2}".format(*range)

status_names = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    206: 'Partial Content',
}
