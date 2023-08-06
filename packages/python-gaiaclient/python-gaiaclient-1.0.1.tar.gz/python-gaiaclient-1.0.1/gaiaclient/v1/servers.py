"""
Server interface.
"""

import base64

from oslo_utils import encodeutils
import six
from six.moves.urllib import parse

from gaiaclient.zeus.common.apiclient import base
# from novaclient import crypto
# from novaclient import exceptions
# from novaclient.i18n import _
# from novaclient.v2 import security_groups


REBOOT_SOFT, REBOOT_HARD = 'SOFT', 'HARD'
BOOT_VOLUME, BOOT_LOCAL = 'volume', 'local'


class Server(base.Resource):
    HUMAN_ID = True

    def __repr__(self):
        return '<Server: %s>' % getattr(self, 'name', 'unknown-name')

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

    def get_vnc_console(self, console_type):
        """
        Get vnc console for a Server.
        :param console_type: Type of console ('novnc' or 'xvpvnc')
        """
        return self.manager.get_vnc_console(self, console_type)

    def add_fixed_ip(self, network_id):
        """
        Add an IP address on a network.
        :param network_id: The ID of the network the IP should be on.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.add_fixed_ip(self, network_id)

    def stop(self):
        """
        Stop -- Stop the running server.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.stop(self)

    def force_delete(self):
        """
        Force delete -- Force delete a server.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.force_delete(self)

    def start(self):
        """
        Start -- Start the paused server.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.start(self)

    def remove_fixed_ip(self, address):
        """
        Remove an IP address.
        :param address: The IP address to remove.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.remove_fixed_ip(self, address)

    def reboot(self, reboot_type=REBOOT_SOFT):
        """
        Reboot the server.
        :param reboot_type: either :data:`REBOOT_SOFT` for a software-level
                reboot, or `REBOOT_HARD` for a virtual power cycle hard reboot.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self.manager.reboot(self, reboot_type)

    def resize(self, flavor, **kwargs):
        """
        Resize the server's resources.
        :param flavor: the :class:`Flavor` (or its ID) to resize to.
        :returns: An instance of novaclient.base.TupleWithMeta
        Until a resize event is confirmed with :meth:`confirm_resize`, the old
        server will be kept around and you'll be able to roll back to the old
        flavor quickly with :meth:`revert_resize`. All resizes are
        automatically confirmed after 24 hours.
        """
        return self.manager.resize(self, flavor, **kwargs)

    def create_image(self, image_name, metadata=None):
        """
        Create an image based on this server.
        :param image_name: The name to assign the newly create image.
        :param metadata: Metadata to assign to the image.
        """
        return self.manager.create_image(self, image_name, metadata)

    @property
    def networks(self):
        """
        Generate a simplified list of addresses
        """
        networks = {}
        try:
            for network_label, address_list in self.addresses.items():
                networks[network_label] = [a['addr'] for a in address_list]
            return networks
        except Exception:
            return {}

    def interface_list(self):
        """
        List interfaces attached to an instance.
        """
        return self.manager.interface_list(self)

    def interface_attach(self, port_id, net_id, fixed_ip):
        """
        Attach a network interface to an instance.
        """
        return self.manager.interface_attach(self, port_id, net_id, fixed_ip)

    def interface_detach(self, port_id):
        """
        Detach a network interface from an instance.
        """
        return self.manager.interface_detach(self, port_id)


class NetworkInterface(base.Resource):
    @property
    def id(self):
        return self.port_id

    def __repr__(self):
        return '<NetworkInterface: %s>' % self.id


class ServerManager(base.ManagerWithDcId):
    resource_class = Server

    def _action(self, action, server, info=None, **kwargs):
        """
        Perform a server "action" -- reboot/rebuild/resize/etc.
        """
        if info:
            items = list(info.items())
            new_qparams = sorted(items, key=lambda x: x[0])
            query_string = "?%s" % parse.urlencode(new_qparams)
        else:
            query_string = ""
        url = '/v1/servers/%s/%s%s' % (base.getid(server), action, query_string)
        self._post(url)

        return

    def _action_return_resp_and_body(self, action, server, info=None,
                                     **kwargs):
        """
        Perform a server "action" and return response headers and body
        """
        # body = {action: info}
        body = {}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/v1/servers/%s/%s' % (base.getid(server), action)
        return self._post(url, body)

    def _console(self, server, info=None, **kwargs):
        """
        Retrieve a console of a particular protocol -- vnc/spice/rdp/serial
        """

        console_type = "?type=%s" % info['type'] if info else ""
        url = '/v1/servers/%s/console%s' % (base.getid(server), console_type)
        resp, body = self._post(url, return_raw=True)
        return self.convert_into_with_meta(body, resp)

    def get(self, server):
        """
        Get a server.
        :param server: ID of the :class:`Server` to get.
        :rtype: :class:`Server`
        """
        return self._get("/v1/servers/%s" % base.getid(server), "server")

    def list(self, search_opts=None, marker=None, limit=None,
             sort_keys=None, sort_dirs=None):
        """
        Get a list of servers.
        :param search_opts: Search options to filter out servers which don't
            match the search_opts (optional). The search opts format is a
            dictionary of key / value pairs that will be appended to the query
            string.  For a complete list of keys see:
            http://developer.openstack.org/api-ref-compute-v2.1.html#listServers
        :param marker: Begin returning servers that appear later in the server
                       list than that represented by this server id (optional).
        :param limit: Maximum number of servers to return (optional).
        :param sort_keys: List of sort keys
        :param sort_dirs: List of sort directions
        :rtype: list of :class:`Server`
        Examples:
        client.servers.list() - returns detailed list of servers
        client.servers.list(search_opts={'status': 'ERROR'}) -
        returns list of servers in error state.
        client.servers.list(limit=10) - returns only 10 servers
        """
        if search_opts is None:
            search_opts = {}

        qparams = {}

        for opt, val in six.iteritems(search_opts):
            if val:
                if isinstance(val, six.text_type):
                    val = val.encode('utf-8')
                qparams[opt] = val

        result = base.ListWithMeta([], None)
        while True:
            if marker:
                qparams['marker'] = marker

            if limit and limit != -1:
                qparams['limit'] = limit

            # Transform the dict to a sequence of two-element tuples in fixed
            # order, then the encoded string will be consistent in Python 2&3.
            if qparams or sort_keys or sort_dirs:
                # sort keys and directions are unique since the same parameter
                # key is repeated for each associated value
                # (ie, &sort_key=key1&sort_key=key2&sort_key=key3)
                items = list(qparams.items())
                if sort_keys:
                    items.extend(('sort_key', sort_key)
                                 for sort_key in sort_keys)
                if sort_dirs:
                    items.extend(('sort_dir', sort_dir)
                                 for sort_dir in sort_dirs)
                new_qparams = sorted(items, key=lambda x: x[0])
                query_string = "?%s" % parse.urlencode(new_qparams)
            else:
                query_string = ""

            servers = self._list("/v1/servers/%s" % query_string, "servers")

            result.extend(servers)
            result.append_request_ids(servers.request_ids)

            if not servers or limit != -1:
                break
            marker = result[-1].id
        return result

    def add_fixed_ip(self, server, network_id):
        """
        Add an IP address on a network.
        :param server: The :class:`Server` (or its ID) to add an IP to.
        :param network_id: The ID of the network the IP should be on.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self._action('addFixedIp', server, {'networkId': network_id})

    def remove_fixed_ip(self, server, address):
        """
        Remove an IP address.
        :param server: The :class:`Server` (or its ID) to add an IP to.
        :param address: The IP address to remove.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self._action('removeFixedIp', server, {'address': address})

    def get_vnc_console(self, server, console_type):
        """
        Get a vnc console for an instance
        :param server: The :class:`Server` (or its ID) to get console for.
        :param console_type: Type of vnc console to get ('novnc' or 'xvpvnc')
        :returns: An instance of novaclient.base.DictWithMeta
        """

        return self._console(server,
                             {'protocol': 'vnc', 'type': console_type})

    def stop(self, server):
        """
        Stop the server.
        :param server: The :class:`Server` (or its ID) to stop
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        self._action('stop', server, None)

        return

    def force_delete(self, server):
        """
        Force delete the server.
        :param server: The :class:`Server` (or its ID) to force delete
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        resp, body = self._action_return_resp_and_body('forceDelete', server,
                                                       None)
        return base.TupleWithMeta((resp, body), resp)

    def start(self, server):
        """
        Start the server.
        :param server: The :class:`Server` (or its ID) to start
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        self._action('start', server, None)

        return

    def ips(self, server):
        """
        Return IP Addresses associated with the server.
        Often a cheaper call then getting all the details for a server.
        :param server: The :class:`Server` (or its ID) for which
                       the IP adresses are to be returned
        :returns: An instance of novaclient.base.DictWithMeta
        """
        resp, body = self.api.client.get("/servers/%s/ips" %
                                         base.getid(server))
        return base.DictWithMeta(body['addresses'], resp)

    def create(self, name, image, flavor, networks, volume=None, boot_type=None, description=None):
        # TODO(anthony): indicate in doc string if param is an extension
        # and/or optional
        """
        Create (boot) a new server.
        :param name: Something to name the server.
        :param image: The :class:`Image` to boot with.
        :param flavor: The :class:`Flavor` to boot onto.
        :param networks: An list of nics (dicts) to be added to this
                      server, with information about connected networks
        :param volume: The :class:`Volume` to boot onto.
        :param boot_type: Where server boot from
        """

        if boot_type not in (None, BOOT_VOLUME, BOOT_LOCAL):
            raise Exception('boot_type must in None, volume, local')

        resource_url = "/v1/servers/"

        body = {"server": {
            "name": name,
            "image": str(base.getid(image)) if image else '',
            "flavor": str(base.getid(flavor)),
            "volume": str(base.getid(volume)),
            "networks": networks,
            "boot_type": boot_type
        }}

        self._post(resource_url, body)

        return

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

    def delete(self, server):
        """
        Delete (i.e. shut down and delete the image) this server.
        :param server: The :class:`Server` (or its ID) to delete
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self._delete("/v1/servers/%s" % base.getid(server))

    def reboot(self, server, reboot_type=REBOOT_HARD):
        """
        Reboot a server.
        :param server: The :class:`Server` (or its ID) to share onto.
        :param reboot_type: either :data:`REBOOT_SOFT` for a software-level
                reboot, or `REBOOT_HARD` for a virtual power cycle hard reboot.
        :returns: An instance of novaclient.base.TupleWithMeta
        """
        return self._action('reboot', server, info={'type': reboot_type})

    def interface_list(self, server):
        """
        List attached network interfaces

        :param server: The :class:`Server` (or its ID) to query.
        """
        return self._list('/v1/servers/%s/interfaces' % base.getid(server),
                          'server-interfaces', obj_class=NetworkInterface)

    def interface_attach(self, server, port_id, net_id, fixed_ip):
        """
        Attach a network_interface to an instance.

        :param server: The :class:`Server` (or its ID) to attach to.
        :param port_id: The port to attach.
        """

        body = {'server-interface': {}}
        if port_id:
            body['server-interface']['port_id'] = port_id
        if net_id:
            body['server-interface']['net_id'] = net_id
        if fixed_ip:
            body['server-interface']['fixed_ip'] = fixed_ip

        return self._create('/v1/servers/%s/interfaces' % base.getid(server),
                            body, 'server-interface')

    def interface_detach(self, server, port_id):
        """
        Detach a network_interface from an instance.

        :param server: The :class:`Server` (or its ID) to detach from.
        :param port_id: The port to detach.
        :returns: An instance of gaiaclient.common.base.TupleWithMeta
        """
        return self._delete('/v1/servers/%s/interfaces/%s' %
                            (base.getid(server), port_id))


