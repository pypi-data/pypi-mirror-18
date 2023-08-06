import pbr.version

try:
    import gaiaclient.client
    Client = gaiaclient.client.Client
except ImportError:
    import warnings
    warnings.warn("Could not import gaiaclient.client", ImportWarning)


version_info = pbr.version.VersionInfo('python-gaiaclient')

__version__ = version_info.version_string()

API_MIN_VERSION = '1.0'

API_MAX_VERSION = '1.0'

