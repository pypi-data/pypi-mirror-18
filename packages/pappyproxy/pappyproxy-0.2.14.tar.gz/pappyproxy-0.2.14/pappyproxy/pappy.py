#!/usr/bin/env python2

"""
Handles the main Pappy session.

.. data:: session

The :class:`pappyproxy.pappy.PappySession` object for the current session. Mainly
used for accessing the session's config information.
"""

import crochet
import txaio

crochet.no_setup()
txaio.use_twisted()

import argparse
import datetime
import os
import schema.update
import shutil
import sys
import tempfile
import signal

from . import comm
from . import config
from . import compress
from . import context
from . import crypto
from . import http
from .console import ProxyCmd
from .util import PappyException
from twisted.enterprise import adbapi
from twisted.internet import reactor, defer
from twisted.internet.error import CannotListenError
from twisted.internet.protocol import ServerFactory
from twisted.internet.threads import deferToThread

main_context = context.Context()
all_contexts = [main_context]

session = None
quit_confirm_time = None

try:
    from guppy import hpy
    heapstats = hpy()
    heapstats.setref()
except ImportError:
    heapstats = None
    
class PappySession(object):
    """
    An object representing a pappy session. Mainly you'll only use this to get to
    the session config.

    :ivar config: The configuration settings for the session
    :vartype config: :class:`pappyproxy.config.PappyConfig`
    """

    def __init__(self, sessconfig):
        self.config = sessconfig
        self.complete_defer = defer.Deferred()
        self.server_factories = []
        self.plugin_loader = None
        self.cons = None
        self.dbpool = None
        self.delete_data_on_quit = False
        self.ports = None
        self.crypto = crypto.Crypto(sessconfig)

    @defer.inlineCallbacks
    def start(self):
        from . import proxy, plugin

        if self.config.crypt_session:
            if self.decrypt():
                self.config.load_from_file('./config.json')
                self.config.global_load_from_file()
                self.delete_data_on_quit = False
            else:
                self.complete_defer.callback(None)
                return
        
        # If the data file doesn't exist, create it with restricted permissions
        if not os.path.isfile(self.config.datafile):
            with os.fdopen(os.open(self.config.datafile, os.O_CREAT, 0o0600), 'r'):
                pass

        self.dbpool = adbapi.ConnectionPool("sqlite3", self.config.datafile,
                                            check_same_thread=False,
                                            cp_openfun=set_text_factory,
                                            cp_max=1)
        try:
            yield schema.update.update_schema(self.dbpool, self.config.datafile)
        except Exception as e:
            print 'Error updating schema: %s' % e
            print 'Exiting...'
            self.complete_defer.callback(None)
            return
        http.init(self.dbpool)
        yield http.Request.cache.load_ids()
        context.reset_context_caches()

        # Run the proxy
        if self.config.debug_dir and os.path.exists(self.config.debug_dir):
            shutil.rmtree(self.config.debug_dir)
            print 'Removing old debugging output'
        listen_strs = []
        self.ports = []
        for listener in self.config.listeners:
            #server_factory = proxy.ProxyServerFactory(save_all=True)
            server_factory = proxy.ProxyProtocolFactory()
            try:
                if 'forward_host_ssl' in listener and listener['forward_host_ssl']:
                    server_factory.force_ssl = True
                    server_factory.forward_host = listener['forward_host_ssl']
                elif 'forward_host' in listener and listener['forward_host']:
                    server_factory.force_ssl = False
                    server_factory.forward_host = listener['forward_host']
                port = reactor.listenTCP(listener['port'], server_factory, interface=listener['interface'])
                listener_str = 'port %d' % listener['port']
                if listener['interface'] not in ('127.0.0.1', 'localhost'):
                    listener_str += ' (bound to %s)' % listener['interface']
                listen_strs.append(listener_str)
                self.ports.append(port)
                self.server_factories.append(server_factory)
            except CannotListenError as e:
                print repr(e)
        if listen_strs:
            print 'Proxy is listening on %s' % (', '.join(listen_strs))
        else:
            print 'No listeners opened'

        com_factory = ServerFactory()
        com_factory.protocol = comm.CommServer
        # Make the port different for every instance of pappy, then pass it to
        # anything we run. Otherwise we can only have it running once on a machine
        self.comm_port = reactor.listenTCP(0, com_factory, interface='127.0.0.1')
        self.comm_port = self.comm_port.getHost().port

        # Load the scope
        yield context.load_scope(self.dbpool)
        context.reset_to_scope(main_context)

        sys.argv = [sys.argv[0]] # cmd2 tries to parse args
        self.cons = ProxyCmd(session=session)
        self.plugin_loader = plugin.PluginLoader(self.cons)
        for d in self.config.plugin_dirs:
            if not os.path.exists(d):
                os.makedirs(d)
            self.plugin_loader.load_directory(d)

        # Add cleanup to defer
        self.complete_defer = deferToThread(self.cons.cmdloop)
        self.complete_defer.addCallback(self.cleanup)

    def encrypt(self):
        if self.crypto.encrypt_project():
            return True
        else:
            return False

    def decrypt(self):
        # Attempt to decrypt project archive
        if self.crypto.decrypt_project():
            return True
        # Quit pappy on failure
        else:
            return False

    @defer.inlineCallbacks
    def cleanup(self, ignored=None):
        for port in self.ports:
            yield port.stopListening()
    
        if self.delete_data_on_quit:
            print 'Deleting temporary datafile'
            os.remove(self.config.datafile)

        # Encrypt the project when in crypto mode 
        if self.config.crypt_session:
            self.encrypt()
    
def parse_args():
    # parses sys.argv and returns a settings dictionary

    parser = argparse.ArgumentParser(description='An intercepting proxy for testing web applications.')
    parser.add_argument('-l', '--lite', help='Run the proxy in "lite" mode', action='store_true')
    parser.add_argument('-d', '--debug', help='Run the proxy in "debug" mode', action='store_true')
    try:
        hlpmsg = ''.join(['Start pappy in "crypto" mode,',
                 'must supply a name for the encrypted',
                 'project archive [CRYPT]'])
        parser.add_argument('-c', '--crypt', type=str, nargs=1, help=hlpmsg)
    except:
        print 'Must supply a project name: pappy -c <project_name>'
        reactor.stop()
        defer.returnValue(None)

    args = parser.parse_args(sys.argv[1:])
    settings = {}

    if args.lite:
        settings['lite'] = True
    else:
        settings['lite'] = False

    if args.crypt:
        # Convert from single-item list produced by argparse `nargs=1`
        settings['crypt'] = args.crypt[0].encode('utf-8')
    else:
        settings['crypt'] = None

    if args.debug:
        settings['debug'] = True
    else:
        settings['debug'] = False
    return settings

def set_text_factory(conn):
    conn.text_factory = str
    
def custom_int_handler(signum, frame):
    # sorry
    print "Sorry, we can't kill things partway through otherwise the data file might be left in a corrupt state"
    
@defer.inlineCallbacks
def main():
    global session
    try:
        settings = parse_args()
    except SystemExit:
        print 'Did you mean to just start the console? If so, just run `pappy` without any arguments then enter commands into the prompt that appears.'
        reactor.stop()
        defer.returnValue(None)

    pappy_config = config.PappyConfig()

    if not os.path.exists(pappy_config.data_dir):
        os.makedirs(pappy_config.data_dir)

    session = PappySession(pappy_config)
    signal.signal(signal.SIGINT, inturrupt_handler)

    if settings['crypt']:
        pappy_config.crypt_file = settings['crypt']
        pappy_config.crypt_session = True
    elif settings['lite']:
        conf_settings = pappy_config.get_default_config()
        conf_settings['debug_dir'] = None
        conf_settings['debug_to_file'] = False
        conf_settings['history_size'] = 0
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            conf_settings['data_file'] = tf.name
            print 'Temporary datafile is %s' % tf.name
        session.delete_data_on_quit = True
        pappy_config.load_settings(conf_settings)
    else:
        # Initialize config
        pappy_config.load_from_file('./config.json')
        pappy_config.global_load_from_file()
        session.delete_data_on_quit = False

    if settings['debug']:
        pappy_config.debug = True

    yield session.start()

    session.complete_defer.addCallback(lambda ignored: reactor.stop())


def start():
    reactor.callWhenRunning(main)
    reactor.run()
    
def inturrupt_handler(signal, frame):
    global session
    global quit_confirm_time
    if not quit_confirm_time or datetime.datetime.now() > quit_confirm_time:
        print ''
        print ('Interrupting will cause Pappy to quit completely. This will '
               'cause any in-memory only requests to be lost, but all other '
               'data will be saved.')
        print ('Interrupt a second time to confirm.')
        print ''
        quit_confirm_time = datetime.datetime.now() + datetime.timedelta(0, 10)
    else:
        d = session.cleanup()
        d.addBoth(lambda _: reactor.stop())
        d.addBoth(lambda _: os._exit(1)) # Sorry blocking threads :(
    
if __name__ == '__main__':
    start()
