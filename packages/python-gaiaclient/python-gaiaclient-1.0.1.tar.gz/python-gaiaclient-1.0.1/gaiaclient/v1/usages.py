from gaiaclient.zeus.common.apiclient import base
import six

USAGE_KEYS = ('volumes', 'instances', 'gigabytes', 'ram', 'instances', 'cores')


class Usage(base.Resource):
    """A Usage object."""
    def __repr__(self):
        return "<Usage %s: quota %s, used %s, available %s>" % \
               (self.name, self.quota, self.used, self.available)


class UsageManager(base.ManagerWithDcId):
    resource_class = Usage

    def _list(self, url, response_key, obj_class=None, data=None):
        resp, body = self._get(url)

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key]

        result = []

        for (k, v) in six.iteritems(data):
            if k in USAGE_KEYS:
                info = {'name': k,
                        'quota': v.get('quota', None),
                        'used': v.get('used', None),
                        'available': v.get('available', None)
                        }
                result.append(obj_class(self, info, loaded=True))

        return (result, resp)

    def list(self):
        """List all versions."""
        url = '/v1/usages/'
        usages, resp = self._list(url, 'usages')
        return usages
