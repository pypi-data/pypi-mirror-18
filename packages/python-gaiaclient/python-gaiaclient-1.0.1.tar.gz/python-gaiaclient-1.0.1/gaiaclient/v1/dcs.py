import copy

from oslo_utils import encodeutils
from oslo_utils import strutils
import six
import six.moves.urllib.parse as urlparse

from gaiaclient.common import utils
from gaiaclient.zeus.common.apiclient import base

UPDATE_PARAMS = ('name', 'auth_url', 'description', 'admin_username',
                 'admin_password', 'admin_tenant', 'transport_url')

CREATE_PARAMS = UPDATE_PARAMS

DEFAULT_PAGE_SIZE = 20

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('name', 'id', 'status')

OS_REQ_ID_HDR = 'x-openstack-request-id'


class DC(base.Resource):
    def __repr__(self):
        return "<DC %s>" % self._info

    def update(self, **fields):
        self.manager.update(self, **fields)

    def delete(self, **kwargs):
        return self.manager.delete(self)


class DCManager(base.ManagerWithFind):
    resource_class = DC

    def _list(self, url, response_key, obj_class=None, data=None):
        resp, body = self.client.get(url)

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key]
        return ([obj_class(self, res, loaded=True) for res in data if res],
                resp)

    def get(self, dc, **kwargs):
        """Get the metadata for a specific dc.

        :param dc: dc object or id to look up
        :rtype: :class:`DC`
        """
        dc_id = base.getid(dc)
        resp, body = self.client.get('/v1/dcs/%s'
                                      % urlparse.quote(str(dc_id)))

        return_request_id = kwargs.get('return_req_id', None)
        if return_request_id is not None:
            return_request_id.append(resp.headers.get(OS_REQ_ID_HDR, None))
        return DC(self, body['dc'])

    def _build_params(self, parameters):

        params = {}
        sort_key = parameters.get('sort_key')
        if sort_key is not None:
            if sort_key in SORT_KEY_VALUES:
                params['sort_key'] = sort_key
            else:
                raise ValueError('sort_key must be one of the following: %s.'
                                 % ', '.join(SORT_KEY_VALUES))

        sort_dir = parameters.get('sort_dir')
        if sort_dir is not None:
            if sort_dir in SORT_DIR_VALUES:
                params['sort_dir'] = sort_dir
            else:
                raise ValueError('sort_dir must be one of the following: %s.'
                                 % ', '.join(SORT_DIR_VALUES))
        # filters = parameters.get('filters')
        # if filters is not None:
        #     params['filters'] = filters

        return params

    def filter_name_or_id(self, name_or_id, dc):
        if name_or_id is None:
            return False

        return dc.id == name_or_id or dc.name == name_or_id

    def list(self, **kwargs):
        """Get a list of dcs.

        :param return_req_id: If an empty list is provided, populate this
                              list with the request ID value from the header
                              x-openstack-request-id
        :rtype: list of :class:`DC`        """

        return_request_id = kwargs.get('return_req_id', None)

        params = self._build_params(kwargs)

        for param, value in six.iteritems(params):
            if isinstance(value, six.string_types):
                # Note(flaper87) Url encoding should
                # be moved inside http utils, at least
                # shouldn't be here.
                #
                # Making sure all params are str before
                # trying to encode them
                params[param] = encodeutils.safe_decode(value)

        url = '/v1/dcs/?%s' % urlparse.urlencode(params)
        dcs, resp = self._list(url, "dcs")

        if return_request_id is not None:
            return_request_id.append(resp.headers.get(OS_REQ_ID_HDR, None))

        filters = kwargs.get('filters', None)

        if filters:
            name_or_id = filters.get('name')
            dcs = [dc for dc in dcs if self.filter_name_or_id(name_or_id, dc)]
            return dcs

        return dcs

    def delete(self, dc, **kwargs):
        """Delete a dc."""
        url = "/v1/dcs/%s" % base.getid(dc)
        resp, body = self.client.delete(url)
        return_request_id = kwargs.get('return_req_id', None)
        if return_request_id is not None:
            return_request_id.append(resp.headers.get(OS_REQ_ID_HDR, None))

    def create(self, **kwargs):
        """Create a dc.

        TODO(bcwaldon): document accepted params
        """

        fields = {}
        for field in kwargs:
            if field in CREATE_PARAMS:
                fields[field] = kwargs[field]
            elif field == 'return_req_id':
                continue
            else:
                msg = 'create() got an unexpected keyword argument \'%s\''
                raise TypeError(msg % field)

        dc_data = {'dc': fields}

        resp, body = self.client.post('/v1/dcs/',
                                      data=dc_data)
        return_request_id = kwargs.get('return_req_id', None)
        if return_request_id is not None:
            return_request_id.append(resp.headers.get(OS_REQ_ID_HDR, None))

        return DC(self, body['dc'])

    def update(self, dc, **kwargs):
        """Update an dc.

        TODO(bcwaldon): document accepted params
        """
        fields = {}
        for field in kwargs:
            if field in UPDATE_PARAMS:
                fields[field] = kwargs[field]
            elif field == 'return_req_id':
                continue
            else:
                msg = 'update() got an unexpected keyword argument \'%s\''
                raise TypeError(msg % field)

        dc_data = {'dc': fields}

        url = '/v1/dcs/%s' % base.getid(dc)
        resp, body = self.client.put(url, data=dc_data)
        return_request_id = kwargs.get('return_req_id', None)
        if return_request_id is not None:
            return_request_id.append(resp.headers.get(OS_REQ_ID_HDR, None))

        return DC(self, body['dc'])
