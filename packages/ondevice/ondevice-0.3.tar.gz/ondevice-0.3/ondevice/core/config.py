try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from ondevice.core import exception

import os


# default config directory:
#   ~/.config/ondevice/
# This works well on macOS and Linux
# TODO add support for further OSs
configDir = os.path.join(os.path.expanduser('~'), '.config/ondevice')

class Overrides:
    def __init__(self):
        self.data = {}

    def __contains__(self, key):
        return key in self.data

    def clear(self):
        self.data = {}

    def get(self, section, key, default=None):
        if not (section,key) in self.data:
            return default
        return self.data[(section,key)]

    def items(self):
        for key, value in self.data.items():
            yield key[0], key[1], value

    def put(self, section, key, value):
        self.data[(section,key)] = value

    def remove(self, section, key):
        if (section, key) in self.data:
            del(self.data[(section,key)])

_config = None
overrides = Overrides()

def addSection(name):
    return _getConfig(True).add_section(name)

def getClientAuth(tgtUser=None):
    """ Returns a (username, password) client access token tuple.
    If you specify a tgtUser and your ondevice.conf contains matching credentials, those will be returned instead.
    """

    clientUser = getClientUser()
    if tgtUser != None:
        if tgtUser != clientUser:
            userKey = 'auth_{0}'.format(tgtUser)
            if hasValue('client', userKey):
                return tgtUser, getValue('client', userKey)
    clientKey = getValue('client', 'auth')
    if clientUser != None and clientKey != None:
        return clientUser, clientKey
    else: return None

def getClientUser():
    return getValue('client', 'user')

def getDeviceAuth():
    envAuth = os.getenv("ONDEVICE_AUTH")
    if envAuth != None:
        # allow the credentials to be provided using environment variables
        return envAuth
    else:
        return getValue('device', 'auth')


def getDeviceKey():
    return getValue('device', 'key')

def getDeviceId():
    # remove old device 'name' config value if present
    if hasValue('device', 'name'):
        remove('device', 'name')
    return getValue('device', 'dev-id')

def getDeviceUser():
    envUser = os.getenv("ONDEVICE_USER")
    if envUser != None:
        # allow the credentials to be provided using environment variables
        return envUser
    else:
        return getValue('device', 'user')

def hasSection(name):
    return _getConfig().has_section(name)

def hasValue(section, name):
    return _getConfig().has_option(section, name)

def listKeys(section):
    return _getConfig().options(section)

def setClientAuth(auth): setValue('client', 'auth', auth)
def setClientUser(name): setValue('client', 'user', name)
def setDeviceAuth(auth): setValue('device', 'auth', auth)
def setDeviceKey(key): setValue('device', 'key', key)
def setDeviceId(slug): setValue('device', 'dev-id', slug)
def setDeviceUser(name): setValue('device', 'user', name)

def invalidateCache():
    """ Invalidate the in-memory cache of the configuration
    (forcing a re-read the next time any getter or setter is called) """
    global _config
    _config = None

def _getConfig(reread=False):
    global _config
    if reread == True or _config == None:
        configFile = _getConfigPath('ondevice.conf')
        _config = ConfigParser()
        _config.read(configFile)

        # init sections
        for s in ['client', 'device']:
            if not _config.has_section(s):
                _config.add_section(s)
        if not _config.has_section('services'):
            _config.add_section('services')
            _config.set('services', 'ssh', '{"protocol": "ssh"}')

    return _config

def _getConfigPath(filename):
    global configDir

    if not os.path.isdir(configDir):
        try:
            os.makedirs(configDir)
        except OSError:
            raise exception.ConfigurationError("Couldn't create config directory: {0}".format(configDir)) 

    return os.path.join(configDir, filename)

def getValue(section, key, default=None):
    if (section,key) in overrides:
        return overrides.get(section, key, default)

    cfg = _getConfig()
    if cfg.has_option(section, key):
        return cfg.get(section, key)
    else:
        return default

def remove(section, key):
    cfg = _getConfig(True)
    if not cfg.remove_option(section, key):
        raise KeyError("No such value: {0}/{1}".format(section, key))

    _saveConfig()

def setValue(section, key, value):
    cfg = _getConfig(True)
    overrides.remove(section, key)
    cfg.set(section, key, value)
    _saveConfig()

def _saveConfig():
    cfg = _getConfig()
    cfgPath = _getConfigPath('ondevice.conf')
    tmpPath = os.path.join(os.path.dirname(cfgPath), '.{0}.tmp'.format(os.path.basename(cfgPath)))
    with open(tmpPath, 'w') as f:
        cfg.write(f)
    os.rename(tmpPath, cfgPath)
