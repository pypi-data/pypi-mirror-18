import glob
import json
import os
import shutil

class PappyConfig(object):
    """
    The configuration settings for the proxy. To access the config object for the
    current session (eg from plugins) use ``pappyproxy.pappy.session.config``.
    
    .. data:: cert_dir
    
    The location of the CA certs that Pappy will use. This can be configured in the
    ``config.json`` file for a project.
    
    :Default: ``{DATADIR}/certs``
    
    .. data:: pappy_dir
    
    The file where pappy's scripts are located. Don't write anything here, and you
    probably don't need to write anything here. Use DATA_DIR instead.
    
    :Default: Wherever the scripts are installed
    
    .. data:: data_dir
    
    The data directory. This is where files that have to be read by Pappy every time
    it's run are put. For example, plugins are stored in ``{DATADIR}/plugins`` and
    certs are by default stored in ``{DATADIR}/certs``. This defaults to ``~/.pappy``
    and isn't configurable right now.
    
    :Default: ``~/.pappy``
    
    .. data:: datafile
    
    The location of the CA certs that Pappy will use. This can be configured in the
    ``config.json`` file for a project.
    
    :Default: ``data.db``
    
    .. data:: debug_dir
    
    The directory to write debug output to. Don't put this outside the project folder
    since it writes all the request data to this directory. You probably won't need
    to use this. Configured in the ``config.json`` file for the project.
    
    :Default: None
    
    .. data:: listeners
    
    The list of active listeners. It is a list of dictionaries of the form `{"port": 8000, "interface": "127.0.0.1"}`
    Not modifiable after startup. Configured in the ``config.json`` file for the project.
    
    :Default: ``[]``
    
    .. data:: socks_proxy
    
    Details for a SOCKS proxy. It is a dict with the following key/values::
    
      host: The SOCKS proxy host
      port: The proxy port
      username: Username (optional)
      password: Password (optional)
    
    If null, no proxy will be used.
    
    :Default: ``null``
    
    .. data:: http_proxy

    Details for an upstream HTTP proxy. It is a dict with the following key/values::
    
      host: The proxy host
      port: The proxy port
      username: Username (optional)
      password: Password (optional)
    
    If null, no proxy will be used.

    .. data:: plugin_dirs
    
    List of directories that plugins are loaded from. Not modifiable.
    
    :Default: ``['{DATA_DIR}/plugins', '{PAPPY_DIR}/plugins']``
    
    .. data:: save_history
    
    Whether command history should be saved to a file/loaded at startup.
    
    :Default: True
    
    .. data:: config_dict
    
    The dictionary read from config.json. When writing plugins, use this to load
    configuration options for your plugin.
    
    .. data:: global_config_dict
    
    The dictionary from ~/.pappy/global_config.json. It contains settings for
    Pappy that are specific to the current computer. Avoid putting settings here,
    especially if it involves specific projects.
     
    .. data:: archive 

    Project archive compressed as a ``tar.bz2`` archive if libraries available on the system, 
    otherwise falls back to zip archive.

    :Default: ``project.archive``

    .. data:: crypt_dir 

    Temporary working directory to unpack an encrypted project archive. Directory
    will contain copies of normal startup files, e.g. conifg.json, cmdhistory, etc.
    On exiting pappy, entire directory will be compressed into an archive and encrypted.
    Compressed as a tar.bz2 archive if libraries available on the system, 
    otherwise falls back to zip.

    :Default: ``crypt``

    .. data:: crypt_file

    Encrypted archive of the temporary working directory ``crypt_dir``. Compressed as a
    tar.bz2 archive if libraries available on the system, otherwise falls back to zip.

    :Default: ``project.crypt``
     
    .. data:: crypt_session
    
    Boolean variable to determine whether pappy started in crypto mode
    
    :Default: False

    .. data:: salt_len

    Length of the nonce-salt value appended to the end of `crypt_file`

    :Default: 16
    """

    def __init__(self):
        self.pappy_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = os.path.join(os.path.expanduser('~'), '.pappy')

        self.cert_dir = os.path.join(self.data_dir, 'certs')

        self.datafile = 'data.db'

        self.debug_dir = None
        self.debug_to_file = False
        self.debug_verbosity = 0

        self.listeners = []
        self.socks_proxy = None
        self.http_proxy = None

        self.ssl_ca_file  = 'certificate.crt'
        self.ssl_pkey_file = 'private.key'

        self.histsize = 1000

        self.plugin_dirs = [os.path.join(self.data_dir, 'plugins'), os.path.join(self.pappy_dir, 'plugins')]

        self.config_dict = {}
        self.global_config_dict = {}

        self.archive = 'project.archive' 
        self.debug = False
        self.crypt_dir = 'crypt'
        self.crypt_file = 'project.crypt'
        self.crypt_session = False
        self.salt_len = 16
    
    def get_default_config(self):
        default_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                           'default_user_config.json')
        with open(default_config_file) as f:
            settings = json.load(f)
        return settings

    def get_project_files(self):
        file_glob = glob.glob('*')
        pp = os.getcwd() + os.sep 
        project_files = [pp+f for f in file_glob if os.path.isfile(pp+f)]
        
        if self.crypt_file in project_files:
            project_files.remove(self.crypt_file)
        
        return project_files 
        

    @staticmethod
    def _parse_proxy_login(conf):
        proxy = {}
        if 'host' in conf and 'port' in conf:
            proxy = {}
            proxy['host'] = conf['host'].encode('utf-8')
            proxy['port'] = conf['port']
            if 'username' in conf:
                if 'password' in conf:
                    proxy['username'] = conf['username'].encode('utf-8')
                    proxy['password'] = conf['password'].encode('utf-8')
                else:
                    print 'Proxy has a username but no password. Ignoring creds.'
        else:
            print 'Host is missing host/port.'
            return None
        return proxy
    
    def load_settings(self, proj_config):
        # Substitution dictionary
        subs = {}
        subs['PAPPYDIR'] = self.pappy_dir
        subs['DATADIR'] = self.data_dir
    
        # Data file settings
        if 'data_file' in proj_config:
            self.datafile = proj_config["data_file"].format(**subs)
    
        # Debug settings
        if 'debug_dir' in proj_config:
            if proj_config['debug_dir']:
                self.debug_to_file = True
                self.debug_dir = proj_config["debug_dir"].format(**subs)
    
        # Cert directory settings
        if 'cert_dir' in proj_config:
            self.cert_dir = proj_config["cert_dir"].format(**subs)
    
        # Listener settings
        if "proxy_listeners" in proj_config:
            self.listeners = []
            for l in proj_config["proxy_listeners"]:
                if 'forward_host_ssl' in l:
                    l['forward_host_ssl'] = l['forward_host_ssl'].encode('utf-8')
                if 'forward_host' in l:
                    l['forward_host'] = l['forward_host'].encode('utf-8')
                self.listeners.append(l)
    
        # SOCKS proxy settings
        self.socks_proxy = None
        if "socks_proxy" in proj_config:
            if proj_config['socks_proxy'] is not None:
                self.socks_proxy = PappyConfig._parse_proxy_login(proj_config['socks_proxy'])

        # HTTP proxy settings
        self.http_proxy = None
        if "http_proxy" in proj_config:
            if proj_config['http_proxy'] is not None:
                self.http_proxy = PappyConfig._parse_proxy_login(proj_config['http_proxy'])
    
        # History saving settings
        if "history_size" in proj_config:
            self.histsize = proj_config['history_size']
    
    def load_global_settings(self, global_config):
        from .http import Request
    
        if "cache_size" in global_config:
            self.cache_size = global_config['cache_size']
        else:
            self.cache_size = 2000
        Request.cache.resize(self.cache_size)
    
    def load_from_file(self, fname):
        # Make sure we have a config file
        if not os.path.isfile(fname):
            print "Copying default config to %s" % fname
            default_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            'default_user_config.json')
            shutil.copyfile(default_config_file, fname)
    
        # Load local project config
        with open(fname, 'r') as f:
            self.config_dict = json.load(f)
        self.load_settings(self.config_dict)
    
    def global_load_from_file(self):
        # Make sure we have a config file
        fname = os.path.join(self.data_dir, 'global_config.json')
        if not os.path.isfile(fname):
            print "Copying default global config to %s" % fname
            default_global_config_file = os.path.join(self.pappy_dir,
                                                      'default_global_config.json')
            shutil.copyfile(default_global_config_file, fname)
    
        # Load local project config
        with open(fname, 'r') as f:
            self.global_config_dict = json.load(f)
        self.load_global_settings(self.global_config_dict) 
