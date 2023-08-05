import sys
import base64
import json

from twisted.protocols.basic import LineReceiver
from twisted.internet import defer
from util import PappyException

"""
comm.py
Handles creating a listening server bound to localhost that other processes can
use to interact with the proxy.
"""

debug = False

class CommServer(LineReceiver):
    MAX_LENGTH=sys.maxint

    def __init__(self):
        self.delimiter = '\n'
        self.action_handlers = {
            'ping': self.action_ping,
            'get_request': self.action_get_request,
            'get_response': self.action_get_response,
            'submit': self.action_submit_request,
        }

    def lineReceived(self, line):
        line = line.strip()

        if line == '':
            return
        #try:
        command_data = json.loads(line)
        command = command_data['action']
        valid = False
        if command in self.action_handlers:
            valid = True
            result = {'success': True}
            func_defer = self.action_handlers[command](command_data)
            func_defer.addCallback(self.action_result_handler, result)
            func_defer.addErrback(self.action_error_handler, result)
        if not valid:
            raise PappyException('%s is an invalid command' % command_data['action'])
        # except PappyException as e:
        #     return_data = {'success': False, 'message': str(e)}
        #     self.sendLine(json.dumps(return_data))

    def action_result_handler(self, data, result):
        result.update(data)
        self.sendLine(json.dumps(result))

    def action_error_handler(self, error, result):
        if debug:
            print error.getTraceback()
        return_data = {'success': False, 'message': str(error.getTraceback())}
        result.update(result)
        error.trap(Exception)
        self.sendLine(json.dumps(return_data))
        return True

    def action_ping(self, data):
        return defer.succeed({'ping': 'pong'})

    @defer.inlineCallbacks
    def action_get_request(self, data):
        from .http import Request
        try:
            reqid = data['reqid']
            req = yield Request.load_request(reqid)
        except KeyError:
            raise PappyException("Request with given ID does not exist")

        dat = json.loads(req.to_json())
        defer.returnValue(dat)

    @defer.inlineCallbacks
    def action_get_response(self, data):
        from .http import Request, Response
        try:
            reqid = data['reqid']
            req = yield Request.load_request(reqid)
        except KeyError:
            raise PappyException("Request with given ID does not exist, cannot fetch associated response.")

        if req.response:
            rsp = req.response
            dat = json.loads(rsp.to_json())
        else:
            dat = {}
        defer.returnValue(dat)

    @defer.inlineCallbacks
    def action_submit_request(self, data):
        from .http import Request
        from .plugin import active_intercepting_macros
        message = base64.b64decode(data['full_message'])
        req = Request(message)
        req.host = data['host'].encode('utf-8')
        req.port = data['port']
        req.is_ssl = data['is_ssl']
        yield req.async_submit(mangle=True)
        if 'tags' in data:
            req.tags = set(data['tags'])
        yield req.async_deep_save()

        retdata = {}
        retdata['request'] = json.loads(req.to_json())
        if req.response:
            retdata['response'] = json.loads(req.response.to_json())
        defer.returnValue(retdata)
