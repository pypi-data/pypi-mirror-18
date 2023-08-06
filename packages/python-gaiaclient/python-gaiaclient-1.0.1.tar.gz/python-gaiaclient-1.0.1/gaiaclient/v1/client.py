from gaiaclient.common import http
from gaiaclient.common import utils
from gaiaclient.v1 import dcs, versions, servers, \
    volumes, images, networks, flavors, usages


class Client(object):
    """Client for the Zeus Gaia v1 API.

    :param string endpoint: A user-supplied endpoint URL for the gaia
                            service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    :param string language_header: Set Accept-Language header to be sent in
                                   requests to gaia.
    """

    def __init__(self, endpoint=None, dc=None, **kwargs):
        """Initialize a new client for the Gaia v1 API."""
        endpoint, self.version = utils.endpoint_version_from_url(endpoint, 1.0)
        self.http_client = http.get_http_client(endpoint=endpoint, **kwargs)
        self.dcs = dcs.DCManager(self.http_client)
        self.servers = servers.ServerManager(self.http_client)
        self.volumes = volumes.VolumeManager(self.http_client)
        self.images = images.ImageManager(self.http_client)
        self.networks = networks.NetworkManager(self.http_client)
        self.subnets = networks.SubnetManager(self.http_client)
        self.versions = versions.VersionManager(self.http_client)
        self.flavors = flavors.FlavorManager(self.http_client)
        self.usages = usages.UsageManager(self.http_client)
        self.set_dc(dc)

    def set_dc(self, dc):
        self.servers.dc = dc
        self.volumes.dc = dc
        self.images.dc = dc
        self.networks.dc = dc
        self.subnets.dc = dc
        self.flavors.dc = dc
        self.usages.dc = dc
