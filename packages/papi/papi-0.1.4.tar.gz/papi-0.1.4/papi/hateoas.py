import papi.fp as fp
import urllib.parse
from functools import partial

def quote_path_elem(e):
    return urllib.parse.quote(e, safe='', encoding='utf-8')

def quote_query_name(n):
    return urllib.parse.quote(str(n), safe=';/?$,:', encoding='utf-8')

def quote_query_value(n):
    return urllib.parse.quote(str(n), safe=';/?$,:=', encoding='utf-8')

def join_path(path):
    return '/' + '/'.join(fp.fmap(quote_path_elem, fp.flatten(path)))

def join_query(query):
    return '?' + '&'.join(( \
        "{0}={1}".format(quote_query_name(name), quote_query_value(value)) \
        for name, value in sorted(query.items())))

def join_url(protocol=None, domain=None, path=None, query=None):
    result = ""
    if domain is not None:
        if protocol is not None:
            result += protocol
            result += ":"
        result += "//"
        result += domain
    if path is not None:
        result += join_path(path)
    if query is not None and query != {}:
        result += join_query(query)
    return result

def hateoas(path, item, page=None, offset=None, count=None):
    if item is None:
        item = {}
    elif item == '':
        item = {'_value': item}
    try:
        item = dict(item)
    except TypeError:
        item = {'_value': item}
    except ValueError:
        item = {'_value': item}

    query = {
        'page': page,
        'offset': offset,
        'count': count,
    }
    query = dict([ (k,v) for (k,v) in query.items() if v is not None ])

    top_link = ("_top",
        join_url(
            path=path,
            query=fp.chain(
                partial(fp.dissoc, 'page'),
                partial(fp.dissoc, 'offset')
            )(query)
        ))
    next_page_link = None
    prev_page_link = None
    next_offset_link = None
    prev_offset_link = None

    count = 20 if count is None else count

    if page is None and offset is None:
        page = 1
    if offset is not None:
        next_offset_link = ("_next", join_url(
            path=path,
            query=fp.assoc('offset', offset+count, query)))
        if offset > count:
            prev_offset_link = ("_prev", join_url(
                path=path,
                query=fp.assoc('offset', offset-count, query)))
    else:
        next_page_link = ("_next", join_url(
            path=path,
            query=fp.assoc('page', page+1, query)))
        if page > 1:
            prev_page_link = ("_prev", join_url(
                path=path,
                query=fp.assoc('page', page-1, query)))

    meta = [ (k, {'href': x}) \
            for (k, x) in \
                fp.cat_maybes([
                    ('_self', join_url(path=path, query=query)),
                    ('_parent', join_path(fp.drop_end(1, path))),
                    top_link,
                    next_page_link,
                    prev_page_link,
                    next_offset_link,
                    prev_offset_link
                ])]
    return fp.assocs(meta, item)
