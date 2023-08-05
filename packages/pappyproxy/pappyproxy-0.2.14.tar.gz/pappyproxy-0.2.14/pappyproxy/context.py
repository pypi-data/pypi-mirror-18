import crochet
import re
import shlex
import json

from .http import Request, Response, RepeatableDict
from twisted.internet import defer
from util import PappyException

"""
context.py

Functions and classes involved with managing the current context and filters
"""

scope = []
_BARE_COMPARERS = ('ex','nex')

class Context(object):
    """
    A class representing a set of requests that pass a set of filters

    :ivar active_filters: Filters that are currently applied to the context
    :vartype active_filters: List of functions that takes one :class:`pappyproxy.http.Request` and returns either true or false.
    :ivar active_requests: Requests which pass all the filters applied to the context
    :type active_requests: Request
    :ivar inactive_requests: Requests which do not pass all the filters applied to the context
    :type inactive_requests: Request
    """

    def __init__(self):
        self.active_filters = []
        self.complete = True
        self.active_requests = []

    @staticmethod
    def get_memid():
        i = 'm%d' % Context._next_in_mem_id
        Context._next_in_mem_id += 1
        return i

    def cache_reset(self):
        self.active_requests = []
        self.complete = False
        
    def add_filter(self, filt):
        """
        Add a filter to the context. This will remove any requests that do not pass
        the filter from the ``active_requests`` set.

        :param filt: The filter to add
        :type filt: Function that takes one :class:`pappyproxy.http.Request` and returns either true or false. (or a :class:`pappyproxy.context.Filter`)
        """
        self.active_filters.append(filt)
        self.cache_reset()

    @defer.inlineCallbacks
    def add_filter_string(self, filtstr):
        """
        Add a filter to the context by filter string
        """
        f = Filter(filtstr)
        yield f.generate()
        self.add_filter(f)

    def filter_up(self):
        """
        Removes the last filter that was applied to the context.
        """
        # Deletes the last filter of the context
        if self.active_filters:
            self.active_filters = self.active_filters[:-1]
        self.cache_reset()

    def set_filters(self, filters):
        """
        Set the list of filters for the context.
        """
        self.active_filters = filters[:]
        self.cache_reset()

    @defer.inlineCallbacks
    def get_reqs(self, n=-1):
        # This is inefficient but I want it to work for now, and as long as we
        # don't put the full requests in memory I don't care.
        ids = self.active_requests
        if (len(ids) >= n and n != -1) or self.complete == True:
            if n == -1:
                defer.returnValue(ids)
            else:
                defer.returnValue(ids[:n])
        ids = []
        for req_d in Request.cache.req_it():
            r = yield req_d
            passed = True
            for filt in self.active_filters:
                if not filt(r):
                    passed = False
                    break
            if passed:
                self.active_requests.append(r.reqid)
                ids.append(r.reqid)
            if len(ids) >= n and n != -1:
                defer.returnValue(ids[:n])
        self.complete = True
        defer.returnValue(ids)

class FilterParseError(PappyException):
    pass


def cmp_is(a, b):
    if a is None or b is None:
        return False
    return str(a) == str(b)

def cmp_contains(a, b):
    if a is None or b is None:
        return False
    return (b.lower() in a.lower())

def cmp_exists(a, b=None):
    if a is None or b is None:
        return False
    return (a is not None and a != [])

def cmp_len_eq(a, b):
    if a is None or b is None:
        return False
    return (len(a) == int(b))

def cmp_len_gt(a, b):
    if a is None or b is None:
        return False
    return (len(a) > int(b))

def cmp_len_lt(a, b):
    if a is None or b is None:
        return False
    return (len(a) < int(b))

def cmp_eq(a, b):
    if a is None or b is None:
        return False
    return (int(a) == int(b))

def cmp_gt(a, b):
    if a is None or b is None:
        return False
    return (int(a) > int(b))

def cmp_lt(a, b):
    if a is None or b is None:
        return False
    return (int(a) < int(b))

def cmp_containsr(a, b):
    if a is None or b is None:
        return False
    try:
        if re.search(b, a):
            return True
        return False
    except re.error as e:
        raise PappyException('Invalid regexp: %s' % e)

def relation_from_text(s, val=''):
    # Gets the relation function associated with the string
    # Returns none if not found

    def negate_func(func):
        def f(*args, **kwargs):
            return not func(*args, **kwargs)
        return f

    negate = False
    if s[0] == 'n':
        negate = True
        s = s[1:]

    if s in ("is",):
        retfunc = cmp_is
    elif s in ("contains", "ct"):
        retfunc = cmp_contains
    elif s in ("containsr", "ctr"):
        validate_regexp(val)
        retfunc = cmp_containsr
    elif s in ("exists", "ex"):
        retfunc = cmp_exists
    elif s in ("Leq",):
        retfunc = cmp_len_eq
    elif s in ("Lgt",):
        retfunc = cmp_len_gt
    elif s in ("Llt",):
        retfunc = cmp_len_lt
    elif s in ("eq",):
        retfunc = cmp_eq
    elif s in ("gt",):
        retfunc = cmp_gt
    elif s in ("lt",):
        retfunc = cmp_lt
    else:
        raise FilterParseError("Invalid relation: %s" % s)

    if negate:
        return negate_func(retfunc)
    else:
        return retfunc
    
def compval_from_args(args):
    """
    NOINDEX
    returns a function that compares to a value from text.
    ie compval_from_text('ct foo') will return a function that returns true
    if the passed in string contains foo.
    """
    if len(args) == 0:
        raise PappyException('Invalid number of arguments')
    if args[0] in _BARE_COMPARERS:
        if len(args) != 1:
            raise PappyException('Invalid number of arguments')
        comparer = relation_from_text(args[0], None)
        value = None
    else:
        if len(args) != 2:
            raise PappyException('Invalid number of arguments')
        comparer = relation_from_text(args[0], args[1])
        value = args[1]

    def retfunc(s):
        return comparer(s, value)

    return retfunc

def compval_from_args_repdict(args):
    """
    NOINDEX
    Similar to compval_from_args but checks a repeatable dict with up to 2
    comparers and values.
    """
    if len(args) == 0:
        raise PappyException('Invalid number of arguments')
    nextargs = args[:]
    value = None
    if args[0] in _BARE_COMPARERS:
        comparer = relation_from_text(args[0], None)
        if len(args) > 1:
            nextargs = args[1:]
    else:
        if len(args) == 1:
            raise PappyException('Invalid number of arguments')
        comparer = relation_from_text(args[0], args[1])
        value = args[1]
        nextargs = args[2:]

    comparer2 = None
    value2 = None
    if nextargs:
        if nextargs[0] in _BARE_COMPARERS:
            comparer2 = relation_from_text(nextargs[0], None)
        else:
            if len(nextargs) == 1:
                raise PappyException('Invalid number of arguments')
            comparer2 = relation_from_text(nextargs[0], nextargs[1])
            value2 = nextargs[1]

    def retfunc(d):
        for k, v in d.all_pairs():
            if comparer2 is None:
                if comparer(k, value) or comparer(v, value):
                    return True
            else:
                if comparer(k, value) and comparer2(v, value2):
                    return True
        return False

    return retfunc

def gen_filter_by_all(args):
    compval = compval_from_args(args)
    def f(req):
        if args[0][0] == 'n':
            return compval(req.full_message) and ((not req.response) or compval(req.response.full_message))
        else:
            return compval(req.full_message) or (req.response and compval(req.response.full_message))
    return f

def gen_filter_by_host(args):
    compval = compval_from_args(args)
    def f(req):
        return compval(req.host)
    return f

def gen_filter_by_body(args):
    compval = compval_from_args(args)
    def f(req):
        if args[0][0] == 'n':
            return compval(req.body) and ((not req.response) or compval(req.response.body))
        else:
            return compval(req.body) or (req.response and compval(req.response.body))
    return f

def gen_filter_by_req_body(args):
    compval = compval_from_args(args)
    def f(req):
        return compval(req.body)
    return f

def gen_filter_by_rsp_body(args):
    compval = compval_from_args(args)
    def f(req):
        if args[0][0] == 'n':
            return (not req.response) or compval(req.response.body)
        else:
            return req.response and compval(req.response.body)
    return f

def gen_filter_by_raw_headers(args):
    compval = compval_from_args(args)
    def f(req):
        if args[0][0] == 'n':
            # compval already negates comparison
            return compval(req.headers_section) and ((not req.response) or compval(req.response.headers_section))
        else:
            return compval(req.headers_section) or (req.response and compval(req.response.headers_section))
    return f

def gen_filter_by_response_code(args):
    compval_from_args(args) # try and throw an error
    def f(req):
        if not req.response:
            return False
        compval = compval_from_args(args)
        return compval(req.response.response_code)
    return f
        
def gen_filter_by_path(args):
    compval = compval_from_args(args)
    def f(req):
        return compval(req.path)
    return f

def gen_filter_by_responsetime(args):
    compval = compval_from_args(args)
    def f(req):
        return compval(req.rsptime)
    return f

def gen_filter_by_verb(args):
    compval = compval_from_args(args)
    def f(req):
        return compval(req.verb)
    return f

def gen_filter_by_tag(args):
    compval = compval_from_args(args)
    def f(req):
        for tag in req.tags:
            if compval(tag):
                return True
        return False
    return f

def gen_filter_by_saved(args):
    if len(args) != 0:
        raise PappyException('Invalid number of arguments')
    def f(req):
        if req.saved:
            return True
        else:
            return False
    return f
                
@defer.inlineCallbacks
def gen_filter_by_before(args):
    if len(args) != 1:
        raise PappyException('Invalid number of arguments')
    r = yield Request.load_request(args[0])
    def f(req):
        if req.time_start is None:
            return False
        if r.time_start is None:
            return False
        return req.time_start <= r.time_start
    defer.returnValue(f)

@defer.inlineCallbacks
def gen_filter_by_after(args, negate=False):
    if len(args) != 1:
        raise PappyException('Invalid number of arguments')
    r = yield Request.load_request(args[0])
    def f(req):
        if req.time_start is None:
            return False
        if r.time_start is None:
            return False
        return req.time_start >= r.time_start
    defer.returnValue(f)

def gen_filter_by_headers(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        if args[0][0] == 'n':
            return comparer(req.headers) and ((not req.response) or comparer(req.response.headers))
        else:
            return comparer(req.headers) or (req.response and comparer(req.response.headers))
    return f

def gen_filter_by_request_headers(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        return comparer(req.headers)
    return f

def gen_filter_by_response_headers(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        if args[0][0] == 'n':
            return (not req.response) or comparer(req.response.headers)
        else:
            return req.response and comparer(req.response.headers)
    return f

def gen_filter_by_submitted_cookies(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        return comparer(req.cookies)
    return f
    
def gen_filter_by_set_cookies(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        if not req.response:
            return False
        checkdict = RepeatableDict()
        for k, v in req.response.cookies.all_pairs():
            checkdict[k] = v.cookie_str
        return comparer(checkdict)
    return f

def gen_filter_by_url_params(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        return comparer(req.url_params)
    return f

def gen_filter_by_post_params(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        return comparer(req.post_params)
    return f

def gen_filter_by_params(args):
    comparer = compval_from_args_repdict(args)
    def f(req):
        return comparer(req.url_params) or comparer(req.post_params)
    return f

@defer.inlineCallbacks
def gen_filter_by_inverse(args):
    filt = yield Filter.from_filter_string(parsed_args=args)
    def f(req):
        return not filt(req)
    defer.returnValue(f)
    
def gen_filter_by_websocket(args):
    def f(req):
        if not req.response:
            return False
        if Response.is_ws_upgrade(req.response):
            return True
        return False
    return f

@defer.inlineCallbacks
def filter_reqs(reqids, filters):
    to_delete = set()
    # Could definitely be more efficient, but it stays like this until
    # it impacts performance
    requests = []
    for reqid in reqids:
        r = yield Request.load_request(reqid)
        requests.append(r)
    for req in requests:
        for filt in filters:
            if not filt(req):
                to_delete.add(req)
    retreqs = []
    retdel = []
    for r in requests:
        if r in to_delete:
            retdel.append(r.reqid)
        else:
            retreqs.append(r.reqid)
    defer.returnValue((retreqs, retdel))

def passes_filters(request, filters):
    for filt in filters:
        if not filt(request):
            return False
    return True

def in_scope(request):
    global scope
    passes = passes_filters(request, scope)
    return passes
    
def set_scope(filters):
    global scope
    scope = filters
    
def save_scope(context):
    global scope
    scope = context.active_filters[:]

def reset_to_scope(context):
    global scope
    context.active_filters = scope[:]
    context.cache_reset()
    
def print_scope():
    global scope
    for f in scope:
        print f.filter_string

@defer.inlineCallbacks
def store_scope(dbpool):
    # Delete the old scope
    yield dbpool.runQuery(
        """
        DELETE FROM scope
        """
    );

    # Insert the new scope
    i = 0
    for f in scope:
        yield dbpool.runQuery(
            """
            INSERT INTO scope (filter_order, filter_string) VALUES (?, ?);
            """,
            (i, f.filter_string)
        );
        i += 1
        
@defer.inlineCallbacks
def load_scope(dbpool):
    global scope
    rows = yield dbpool.runQuery(
            """
            SELECT filter_order, filter_string FROM scope;
            """,
        )
    rows = sorted(rows, key=lambda r: int(r[0]))
    new_scope = []
    for row in rows:
        new_filter = Filter(row[1])
        yield new_filter.generate()
        new_scope.append(new_filter)
    scope = new_scope

@defer.inlineCallbacks
def clear_tag(tag):
    # Remove a tag from every request
    reqs = yield Request.cache.load_by_tag(tag)
    for req in reqs:
        req.tags.discard(tag)
        if req.saved:
            yield req.async_save()
    reset_context_caches()

@defer.inlineCallbacks
def async_set_tag(tag, reqs):
    """
    async_set_tag(tag, reqs)
    Remove the tag from every request then add the given requests to memory and
    give them the tag. The async version.

    :param tag: The tag to set
    :type tag: String
    :param reqs: The requests to assign to the tag
    :type reqs: List of Requests
    """
    yield clear_tag(tag)
    for req in reqs:
        req.tags.add(tag)
        Request.cache.add(req)
    reset_context_caches()

@defer.inlineCallbacks
def save_context(name, filter_strings, dbpool):
    """
    Saves the filter strings to the datafile using their name
    """
    rows = yield dbpool.runQuery(
        """
        SELECT id FROM saved_contexts WHERE context_name=?;
        """, (name,)
    )
    list_str = json.dumps(filter_strings)
    if len(rows) > 0:
        yield dbpool.runQuery(
            """
            UPDATE saved_contexts SET filter_strings=?
            WHERE context_name=?;
            """, (list_str, name)
        )
    else:
        yield dbpool.runQuery(
            """
            INSERT INTO saved_contexts (context_name, filter_strings)
            VALUES (?,?);
            """, (name, list_str)
        )
        
@defer.inlineCallbacks
def delete_saved_context(name, dbpool):
    yield dbpool.runQuery(
        """
        DELETE FROM saved_contexts WHERE context_name=?;
        """, (name,)
    )
    
@defer.inlineCallbacks
def get_saved_context(name, dbpool):
    rows = yield dbpool.runQuery(
        """
        SELECT filter_strings FROM saved_contexts WHERE context_name=?;
        """, (name,)
    )
    if len(rows) == 0:
        raise PappyException("Saved context with name %s does not exist" % name)
    filter_strs = json.loads(rows[0][0])
    defer.returnValue(filter_strs)

@defer.inlineCallbacks
def get_all_saved_contexts(dbpool):
    rows = yield dbpool.runQuery(
        """
        SELECT context_name, filter_strings FROM saved_contexts;
        """,
    )
    all_strs = {}
    for row in rows:
        all_strs[row[0]] = json.loads(row[1])
    defer.returnValue(all_strs)

@crochet.wait_for(timeout=180.0)
@defer.inlineCallbacks
def set_tag(tag, reqs):
    """
    set_tag(tag, reqs)
    Remove the tag from every request then add the given requests to memory and
    give them the tag. The non-async version.

    :param tag: The tag to set
    :type tag: String
    :param reqs: The requests to assign to the tag
    :type reqs: List of Requests
    """
    yield async_set_tag(tag, reqs)

def validate_regexp(r):
    try:
        re.compile(r)
    except re.error as e:
        raise PappyException('Invalid regexp: %s' % e)

def reset_context_caches():
    import pappyproxy.pappy
    for c in pappyproxy.pappy.all_contexts:
        c.cache_reset()

class Filter(object):
    """
    A class representing a filter. Its claim to fame is that you can use
    :func:`pappyproxy.context.Filter.from_filter_string` to generate a
    filter from a filter string.
    """
    
    _filter_functions = {
        "all": gen_filter_by_all,

        "host": gen_filter_by_host,
        "domain": gen_filter_by_host,
        "hs": gen_filter_by_host,
        "dm": gen_filter_by_host,

        "path": gen_filter_by_path,
        "pt": gen_filter_by_path,
        
        "body": gen_filter_by_body,
        "bd": gen_filter_by_body,
        "data": gen_filter_by_body,
        "dt": gen_filter_by_body,
        
        "reqbody": gen_filter_by_req_body,
        "qbd": gen_filter_by_req_body,
        "reqdata": gen_filter_by_req_body,
        "qdt": gen_filter_by_req_body,
        
        "rspbody": gen_filter_by_rsp_body,
        "sbd": gen_filter_by_rsp_body,
        "qspdata": gen_filter_by_rsp_body,
        "sdt": gen_filter_by_rsp_body,
        
        "verb": gen_filter_by_verb,
        "vb": gen_filter_by_verb,
        
        "param": gen_filter_by_params,
        "pm": gen_filter_by_params,
        
        "header": gen_filter_by_headers,
        "hd": gen_filter_by_headers,
        
        "reqheader": gen_filter_by_request_headers,
        "qhd": gen_filter_by_request_headers,
        
        "rspheader": gen_filter_by_response_headers,
        "shd": gen_filter_by_response_headers,
        
        "rawheaders": gen_filter_by_raw_headers,
        "rh": gen_filter_by_raw_headers,
        
        "sentcookie": gen_filter_by_submitted_cookies,
        "sck": gen_filter_by_submitted_cookies,
        
        "setcookie": gen_filter_by_set_cookies,
        "stck": gen_filter_by_set_cookies,
        
        "statuscode": gen_filter_by_response_code,
        "sc": gen_filter_by_response_code,
        "responsecode": gen_filter_by_response_code,
        
        "tag": gen_filter_by_tag,
        "tg": gen_filter_by_tag,
        
        "saved": gen_filter_by_saved,
        "svd": gen_filter_by_saved,

        "websocket": gen_filter_by_websocket,
        "ws": gen_filter_by_websocket,
    }

    _async_filter_functions = {
        "before": gen_filter_by_before,
        "b4": gen_filter_by_before,
        "bf": gen_filter_by_before,
        
        "after": gen_filter_by_after,
        "af": gen_filter_by_after,
        
        "inv": gen_filter_by_inverse,
    }

    def __init__(self, filter_string):
        self.filter_string = filter_string

    def __call__(self, *args, **kwargs):
        return self.filter_func(*args, **kwargs)

    def __repr__(self):
        return '<Filter "%s">' % self.filter_string

    @defer.inlineCallbacks
    def generate(self):
        self.filter_func = yield self.from_filter_string(self.filter_string)

    @staticmethod
    @defer.inlineCallbacks
    def from_filter_string(filter_string=None, parsed_args=None):
        """
        from_filter_string(filter_string)

        Create a filter from a filter string. If passed a list of arguments, they
        will be used instead of parsing the string.

        :rtype: Deferred that returns a :class:`pappyproxy.context.Filter`
        """
        if parsed_args is not None:
            args = parsed_args
        else:
            args = shlex.split(filter_string)
        if len(args) == 0:
            raise PappyException('Field is required')
        field = args[0]
        new_filter = None

        field_args = args[1:]
        if field in Filter._filter_functions:
            new_filter = Filter._filter_functions[field](field_args)
        elif field in Filter._async_filter_functions:
            new_filter = yield Filter._async_filter_functions[field](field_args)
        else:
            raise FilterParseError("%s is not a valid field" % field)

        if new_filter is None:
            raise FilterParseError("Error creating filter")
        defer.returnValue(new_filter)
