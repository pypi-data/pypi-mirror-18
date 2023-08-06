"""
Nework interface.
"""

import base64

from oslo_utils import encodeutils
import six
import six.moves.urllib.parse as urlparse

from gaiaclient.zeus.common.apiclient import base


SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('name',)

OS_REQ_ID_HDR = 'x-openstack-request-id'


class Network(base.Resource):
    HUMAN_ID = True

    def __repr__(self):
        return '<Network: %s>' % getattr(self, 'name', 'unknown-name')

    def delete(self):
        """
        Delete (i.e. shut down and delete the image) this server.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.delete(self)

    def update(self, name=None, description=None):
        """
        Update the name and the description for this server.
        :param name: Update the server's name.
        :param description: Update the server's description.
        :returns: :class:`Server`
        """
        update_kwargs = {"name": name}
        if description is not None:
            update_kwargs["description"] = description
        return self.manager.update(self, **update_kwargs)


class Subnet(base.Resource):
    HUMAN_ID = True

    def __repr__(self):
        return '<Subnet: %s>' % getattr(self, 'name', 'unknown-name')


class NetworkManager(base.ManagerWithDcId):
    resource_class = Network

    def _build_params(self, parameters):
        # params = {'limit': parameters.get('page_size', DEFAULT_PAGE_SIZE)}

        params = {}

        if 'marker' in parameters:
            params['marker'] = parameters['marker']

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

        if 'is_public' in parameters:
            params['is_public'] = parameters['is_public']

        return params


    def get(self, network):
        """
        Get a server.
        :param server: ID of the :class:`Server` to get.
        :rtype: :class:`Server`
        """
        return self._get("/v1/networks/%s" % base.getid(network), "network")

    def list(self, **kwargs):

        absolute_limit = kwargs.get('limit')

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

        url = '/v1/networks/?%s' % urlparse.urlencode(params)
        networks = self._list(url, "networks")

        if return_request_id is not None:
            return_request_id.append(networks.request_ids)

        return networks

    def create(self, name, image, flavor, meta=None, files=None,
               reservation_id=None, min_count=None,
               max_count=None, security_groups=None, userdata=None,
               key_name=None, availability_zone=None,
               block_device_mapping=None, block_device_mapping_v2=None,
               nics=None, scheduler_hints=None,
               config_drive=None, disk_config=None, admin_pass=None,
               access_ip_v4=None, access_ip_v6=None, **kwargs):
        # TODO(anthony): indicate in doc string if param is an extension
        # and/or optional
        """
        Create (boot) a new server.
        :param name: Something to name the server.
        :param image: The :class:`Image` to boot with.
        :param flavor: The :class:`Flavor` to boot onto.
        :param meta: A dict of arbitrary key/value metadata to store for this
                     server. Both keys and values must be <=255 characters.
        :param files: A dict of files to overwrite on the server upon boot.
                      Keys are file names (i.e. ``/etc/passwd``) and values
                      are the file contents (either as a string or as a
                      file-like object). A maximum of five entries is allowed,
                      and each file must be 10k or less.
        :param reservation_id: a UUID for the set of servers being requested.
        :param min_count: (optional extension) The minimum number of
                          servers to launch.
        :param max_count: (optional extension) The maximum number of
                          servers to launch.
        :param security_groups: A list of security group names
        :param userdata: user data to pass to be exposed by the metadata
                      server this can be a file type object as well or a
                      string.
        :param key_name: (optional extension) name of previously created
                      keypair to inject into the instance.
        :param availability_zone: Name of the availability zone for instance
                                  placement.
        :param block_device_mapping: (optional extension) A dict of block
                      device mappings for this server.
        :param block_device_mapping_v2: (optional extension) A dict of block
                      device mappings for this server.
        :param nics:  An ordered list of nics (dicts) to be added to this
                      server, with information about connected networks,
                      fixed IPs, port etc.
                      Beginning in microversion 2.37 this field is required and
                      also supports a single string value of 'auto' or 'none'.
                      The 'auto' value means the Compute service will
                      automatically allocate a network for the project if one
                      is not available. This is the same behavior as not
                      passing anything for nics before microversion 2.37. The
                      'none' value tells the Compute service to not allocate
                      any networking for the server.
        :param scheduler_hints: (optional extension) arbitrary key-value pairs
                            specified by the client to help boot an instance
        :param config_drive: (optional extension) value for config drive
                            either boolean, or volume-id
        :param disk_config: (optional extension) control how the disk is
                            partitioned when the server is created.  possible
                            values are 'AUTO' or 'MANUAL'.
        :param admin_pass: (optional extension) add a user supplied admin
                           password.
        :param access_ip_v4: (optional extension) add alternative access ip v4
        :param access_ip_v6: (optional extension) add alternative access ip v6
        :param description: optional description of the server (allowed since
                            microversion 2.19)
        """
        if not min_count:
            min_count = 1
        if not max_count:
            max_count = min_count
        if min_count > max_count:
            min_count = max_count

        boot_args = [name, image, flavor]

        descr_microversion = api_versions.APIVersion("2.19")
        if "description" in kwargs and self.api_version < descr_microversion:
            raise exceptions.UnsupportedAttribute("description", "2.19")

        self._validate_create_nics(nics)

        tags_microversion = api_versions.APIVersion("2.32")
        if self.api_version < tags_microversion:
            if nics:
                for nic_info in nics:
                    if nic_info.get("tag"):
                        raise ValueError("Setting interface tags is "
                                         "unsupported before microversion "
                                         "2.32")

            if block_device_mapping_v2:
                for bdm in block_device_mapping_v2:
                    if bdm.get("tag"):
                        raise ValueError("Setting block device tags is "
                                         "unsupported before microversion "
                                         "2.32")

        boot_kwargs = dict(
            meta=meta, files=files, userdata=userdata,
            reservation_id=reservation_id, min_count=min_count,
            max_count=max_count, security_groups=security_groups,
            key_name=key_name, availability_zone=availability_zone,
            scheduler_hints=scheduler_hints, config_drive=config_drive,
            disk_config=disk_config, admin_pass=admin_pass,
            access_ip_v4=access_ip_v4, access_ip_v6=access_ip_v6, **kwargs)

        if block_device_mapping:
            resource_url = "/os-volumes_boot"
            boot_kwargs['block_device_mapping'] = block_device_mapping
        elif block_device_mapping_v2:
            resource_url = "/os-volumes_boot"
            boot_kwargs['block_device_mapping_v2'] = block_device_mapping_v2
        else:
            resource_url = "/servers"
        if nics:
            boot_kwargs['nics'] = nics

        response_key = "server"
        return self._boot(resource_url, response_key, *boot_args,
                          **boot_kwargs)

    def update(self, server, name=None, description=None):
        """
        Update the name or the description for a server.
        :param server: The :class:`Server` (or its ID) to update.
        :param name: Update the server's name.
        :param description: Update the server's description. If it equals to
            empty string(i.g. ""), the server description will be removed.
        """
        if name is None and description is None:
            return

        body = {"server": {}}
        if name:
            body["server"]["name"] = name
        if description == "":
            body["server"]["description"] = None
        elif description:
            body["server"]["description"] = description

        return self._update("/v1/servers/%s" % base.getid(server), body, "server")

    def delete(self, network):
        """
        Delete (i.e. shut down and delete the image) this server.
        :param server: The :class:`Server` (or its ID) to delete
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self._delete("/v1/networks/%s" % base.getid(network))


class SubnetManager(base.ManagerWithDcId):
    resource_class = Subnet

    def _build_params(self, parameters):
        # params = {'limit': parameters.get('page_size', DEFAULT_PAGE_SIZE)}

        params = {}

        if 'marker' in parameters:
            params['marker'] = parameters['marker']

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

        if 'is_public' in parameters:
            params['is_public'] = parameters['is_public']

        return params

    def get(self, subnet):
        """
        Get a server.
        :param server: ID of the :class:`Server` to get.
        :rtype: :class:`Server`
        """
        return self._get("/v1/subnets/%s" % base.getid(subnet), "subnet")

    def list(self, **kwargs):

        absolute_limit = kwargs.get('limit')

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

        url = '/v1/subnets/?%s' % urlparse.urlencode(params)
        subnets = self._list(url, "subnets")

        if return_request_id is not None:
            return_request_id.append(subnets.request_ids)

        return subnets

