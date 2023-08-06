from gaiaclient.zeus.common.apiclient import base


class Version(base.Resource):
    """A version object."""
    def __repr__(self):
        return "<Version: %s>" % self.release_version


class VersionManager(base.ManagerWithFind):
    resource_class = Version

    def _list(self, url, response_key, obj_class=None, data=None):
        resp, body = self.client.get(url)

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key]
        return ([obj_class(self, res, loaded=True) for res in data if res],
                resp)

    def list(self):
        """List all versions."""
        url = '/'
        versions, resp = self._list(url, 'versions')
        return versions
