import os

from gaiaclient.common import utils
from gaiaclient.common import exceptions
from gaiaclient.zeus.common.apiclient import base
from gaiaclient.v1 import servers

from oslo_utils import strutils
from oslo_utils import timeutils
import six

REQUIRED_FIELDS = ('dc_name',)


def _print_interfaces(interfaces):
    columns = ['Port State', 'Port ID', 'Net ID', 'IP addresses',
               'MAC Addr']

    class FormattedInterface(object):
        def __init__(self, interface):
            for col in columns:
                key = col.lower().replace(" ", "_")
                if hasattr(interface, key):
                    setattr(self, key, getattr(interface, key))
            self.ip_addresses = ",".join([fip['ip_address']
                                          for fip in interface.fixed_ips])
    utils.print_list([FormattedInterface(i) for i in interfaces], columns)


def _translate_keys(collection, convert):
    for item in collection:
        keys = item.__dict__.keys()
        for from_key, to_key in convert:
            if from_key in keys and to_key not in keys:
                setattr(item, to_key, item._info[from_key])


def _translate_extended_states(collection):
    power_states = [
        'NOSTATE',      # 0x00
        'Running',      # 0x01
        '',             # 0x02
        'Paused',       # 0x03
        'Shutdown',     # 0x04
        '',             # 0x05
        'Crashed',      # 0x06
        'Suspended'     # 0x07
    ]

    for item in collection:
        try:
            setattr(item, 'power_state',
                    power_states[getattr(item, 'power_state')])
        except AttributeError:
            setattr(item, 'power_state', "N/A")
        try:
            getattr(item, 'task_state')
        except AttributeError:
            setattr(item, 'task_state', "N/A")


def _get_list_table_columns_and_formatters(fields, objs, exclude_fields=(), filters=None):

    """Check and add fields to output columns.
    If there is any value in fields that not an attribute of obj,
    CommandError will be raised.
    If fields has duplicate values (case sensitive), we will make them unique
    and ignore duplicate ones.
    If exclude_fields is specified, any field both in fields and
    exclude_fields will be ignored.
    :param fields: A list of string contains the fields to be printed.
    :param objs: An list of object which will be used to check if field is
                 valid or not. Note, we don't check fields if obj is None or
                 empty.
    :param exclude_fields: A tuple of string which contains the fields to be
                           excluded.
    :param filters: A dictionary defines how to get value from fields, this
                    is useful when field's value is a complex object such as
                    dictionary.
    :return: columns, formatters.
             columns is a list of string which will be used as table header.
             formatters is a dictionary specifies how to display the value
             of the field.
             They can be [], {}.
    :raise: novaclient.exceptions.CommandError
    """
    if not fields:
        return [], {}

    if not objs:
        obj = None
    elif isinstance(objs, list):
        obj = objs[0]
    else:
        obj = objs

    columns = []
    formatters = {}

    non_existent_fields = []
    exclude_fields = set(exclude_fields)

    for field in fields.split(','):
        if not hasattr(obj, field):
            non_existent_fields.append(field)
            continue
        if field in exclude_fields:
            continue
        field_title, formatter = utils.make_field_formatter(field,
                                                            filters)
        columns.append(field_title)
        formatters[field_title] = formatter
        exclude_fields.add(field)

    if non_existent_fields:
        raise exceptions.CommandError(
            _("Non-existent fields are specified: %s") % non_existent_fields)

    return columns, formatters


def _find_image(gc, image):
    """Get an image by name or ID."""
    try:
        return utils.find_resource(gc.images, image)
    except (exceptions.NotFound, exceptions.NoUniqueMatch) as e:
        raise exceptions.CommandError(six.text_type(e))


def _find_flavor(gc, flavor):
    """Get a flavor by name, ID, or RAM size."""
    try:
        return utils.find_resource(gc.flavors, flavor)
    except exceptions.NotFound:
        return gc.flavors.find(ram=flavor)


def _find_server(gc, server, raise_if_notfound=True):
    """Get a server by name or ID.

    :param gc: GaiaClient's instance
    :param server: identifier of server
    :param raise_if_notfound: raise an exception if server is not found
    :param find_args: argument to search server
    """
    if raise_if_notfound:
        return utils.find_resource(gc.servers, server)
    else:
        try:
            return utils.find_resource(gc.servers, server)
        except exceptions.NoUniqueMatch as e:
            raise exceptions.CommandError(six.text_type(e))
        except exceptions.NotFound:
            # The server can be deleted
            return server


def _print_server(gc, args, server=None):
    if not server:
        server = _find_server(gc, args.server)

    minimal = getattr(args, "minimal", False)

    networks = server.networks
    info = server._info.copy()
    for network_label, address_list in networks.items():
        info['%s network' % network_label] = ', '.join(address_list)

    flavor = info.get('flavor', {})
    flavor_id = flavor.get('id', '')
    if minimal:
        info['flavor'] = flavor_id
    else:
        try:
            info['flavor'] = '%s (%s)' % (_find_flavor(gc, flavor_id).name,
                                          flavor_id)
        except Exception:
            info['flavor'] = '%s (%s)' % ("Flavor not found", flavor_id)

    if 'security_groups' in info:
        # when we have multiple nics the info will include the
        # security groups N times where N == number of nics. Be nice
        # and only display it once.
        info['security_groups'] = ', '.join(
            sorted(set(group['name'] for group in info['security_groups'])))

    image = info.get('image', {})
    if image:
        image_id = image.get('id', '')
        if minimal:
            info['image'] = image_id
        else:
            try:
                info['image'] = '%s (%s)' % (_find_image(gc, image_id).name,
                                             image_id)
            except Exception:
                info['image'] = '%s (%s)' % ("Image not found", image_id)
    else:  # Booted from volume
        info['image'] = "Attempt to boot from volume - no image supplied"

    info.pop('links', None)
    info.pop('addresses', None)

    utils.print_dict(info)


def _boot(gc, args):
    """Boot a new server."""
    if not args.flavor:
        raise exceptions.CommandError("you need to specify a Flavor ID.")

    if args.image:
        image = _find_image(gc, args.image)
    else:
        image = None

    flavor = _find_flavor(gc, args.flavor)

    n_boot_args = len(list(filter(
        bool, (image, args.boot_volume))))

    # Fail if more than one boot devices are present
    # or if there is no device to boot from.
    if n_boot_args > 1 or n_boot_args == 0:
        raise exceptions.CommandError(
            "you need to specify at least one source ID (Image, Volume)")

    networks = _parse_networks(gc, args)

    boot_args = [args.name, image, flavor, networks]

    boot_kwargs = dict(
        volume=args.boot_volume)

    if 'description' in args:
        boot_kwargs["description"] = args.description

    if args.boot_local:
        boot_kwargs['boot_type'] = servers.BOOT_LOCAL

    return boot_args, boot_kwargs


def _parse_networks(gc, args):
    networks = []

    if len(args.networks) == 0:
        raise exceptions.CommandError(
            "you need to specify at least one network")

    i = 0
    for net in args.networks:
        network = {
            'id': base.getid(net),
            'ip': args.ips[i] if len(args.ips) > i else ''
        }
        networks.append(network)
        i = i + 1

    return networks


def print_console(gc, data):
    utils.print_list([Console(console_dict_accessor(gc, data))],
                     ['Type', 'Url'])


def console_dict_accessor(gc, data):
    return data['console']


class Console(object):
    def __init__(self, console_dict):
        self.type = console_dict['type']
        self.url = console_dict['url']


@utils.arg(
    '--ip',
    dest='ip',
    metavar='<ip-regexp>',
    default=None,
    help='Search with regular expression match by IP address.')
@utils.arg(
    '--name',
    dest='name',
    metavar='<name-regexp>',
    default=None,
    help='Search with regular expression match by name.')
@utils.arg(
    '--instance-name',
    dest='instance_name',
    metavar='<name-regexp>',
    default=None,
    help='Search with regular expression match by server name.')
@utils.arg(
    '--status',
    dest='status',
    metavar='<status>',
    default=None,
    help='Search by server status.')
@utils.arg(
    '--flavor',
    dest='flavor',
    metavar='<flavor>',
    default=None,
    help='Search by flavor name or ID.')
@utils.arg(
    '--image',
    dest='image',
    metavar='<image>',
    default=None,
    help='Search by image name or ID.')
@utils.arg(
    '--host',
    dest='host',
    metavar='<hostname>',
    default=None,
    help='Search servers by hostname to which they are assigned (Admin '
           'only).')
@utils.arg(
    '--all-tenants',
    dest='all_tenants',
    metavar='<0|1>',
    nargs='?',
    type=int,
    const=1,
    default=int(strutils.bool_from_string(
        os.environ.get("ALL_TENANTS", 'false'), True)),
    help='Display information from all tenants (Admin only).')
@utils.arg(
    '--tenant',
    # nova db searches by project_id
    dest='tenant',
    metavar='<tenant>',
    nargs='?',
    help='Display information from single tenant (Admin only).')
@utils.arg(
    '--user',
    dest='user',
    metavar='<user>',
    nargs='?',
    help='Display information from single user (Admin only).')
@utils.arg(
    '--deleted',
    dest='deleted',
    action="store_true",
    default=False,
    help='Only display deleted servers (Admin only).')
@utils.arg(
    '--fields',
    default=None,
    metavar='<fields>',
    help='Comma-separated list of fields to display. '
           'Use the show command to see which fields are available.')
@utils.arg(
    '--minimal',
    dest='minimal',
    action="store_true",
    default=False,
    help='Get only UUID and name.')
@utils.arg(
    '--sort',
    dest='sort',
    metavar='<key>[:<direction>]',
    help='Comma-separated list of sort keys and directions in the form '
           'of <key>[:<asc|desc>]. The direction defaults to descending if '
           'not specified.')
@utils.arg(
    '--marker',
    dest='marker',
    metavar='<marker>',
    default=None,
    help='The last server UUID of the previous page; displays list of '
           'servers after "marker".')
@utils.arg(
    '--limit',
    dest='limit',
    metavar='<limit>',
    type=int,
    default=None,
    help="Maximum number of servers to display. If limit == -1, all servers "
           "will be displayed. ")
@utils.arg(
    '--changes-since',
    dest='changes_since',
    metavar='<changes_since>',
    default=None,
    help="List only servers changed after a certain point of time."
           "The provided time should be an ISO 8061 formatted time."
           "ex 2016-03-04T06:27:59Z .")
@utils.require_dc
def do_server_list(gc, args):
    """List active servers."""
    imageid = None
    flavorid = None

    if args.image:
        imageid = _find_image(gc, args.image).id
    if args.flavor:
        flavorid = _find_flavor(gc, args.flavor).id
    # search by tenant or user only works with all_tenants
    if args.tenant or args.user:
        args.all_tenants = 1
    search_opts = {
        'all_tenants': args.all_tenants,
        'ip': args.ip,
        'name': args.name,
        'image': imageid,
        'flavor': flavorid,
        'status': args.status,
        'tenant_id': args.tenant,
        'user_id': args.user,
        'host': args.host,
        'deleted': args.deleted,
        'instance_name': args.instance_name,
        'changes-since': args.changes_since}

    # for arg in ('tags', "tags-any", 'not-tags', 'not-tags-any'):
    #     if arg in args:
    #         search_opts[arg] = getattr(args, arg)

    filters = {'flavor': lambda f: f['id'],
               'security_groups': utils.format_security_groups}

    id_col = 'ID'

    detailed = not args.minimal

    sort_keys = []
    sort_dirs = []
    if args.sort:
        for sort in args.sort.split(','):
            sort_key, _sep, sort_dir = sort.partition(':')
            if not sort_dir:
                sort_dir = 'desc'
            elif sort_dir not in ('asc', 'desc'):
                raise exceptions.CommandError(
                    'Unknown sort direction: %s' % sort_dir)
            sort_keys.append(sort_key)
            sort_dirs.append(sort_dir)

    if search_opts['changes-since']:
        try:
            timeutils.parse_isotime(search_opts['changes-since'])
        except ValueError:
            raise exceptions.CommandError('Invalid changes-since value: %s'
                                          % search_opts['changes-since'])

    servers = gc.servers.list(search_opts=search_opts,
                              sort_keys=sort_keys,
                              sort_dirs=sort_dirs,
                              marker=args.marker,
                              limit=args.limit)
    convert = [('OS-EXT-SRV-ATTR:host', 'host'),
               ('OS-EXT-STS:task_state', 'task_state'),
               ('OS-EXT-SRV-ATTR:instance_name', 'instance_name'),
               ('OS-EXT-STS:power_state', 'power_state'),
               ('hostId', 'host_id')]
    _translate_keys(servers, convert)
    _translate_extended_states(servers)

    formatters = {}

    cols, fmts = _get_list_table_columns_and_formatters(
        args.fields, servers, exclude_fields=('id',), filters=filters)

    if args.minimal:
        columns = [
            id_col,
            'Name']
    elif cols:
        columns = [id_col] + cols
        formatters.update(fmts)
    else:
        columns = [
            id_col,
            'Name',
            'Status',
            'Task State',
            'Power State',
            'Networks'
        ]
        # If getting the data for all tenants, print
        # Tenant ID as well
        if search_opts['all_tenants']:
            columns.insert(2, 'Tenant ID')
        if search_opts['changes-since']:
            columns.append('Updated')
    formatters['Networks'] = utils.format_servers_list_networks
    utils.print_list(servers, columns, formatters)


@utils.arg('name', metavar='<NAME>',
           help='Name of server.')
@utils.arg(
    '--flavor',
    default=None,
    metavar='<flavor>',
    help="Name or ID of flavor (see 'gaia flavor-list').")
@utils.arg(
    '--image',
    default=None,
    metavar='<image>',
    help="Name or ID of image (see 'gaia image-list'). ")
@utils.arg(
    '--boot-volume',
    default=None,
    metavar="<volume_id>",
    help="Volume ID to boot from.")
@utils.arg(
    '--network',
    metavar="<net-id>",
    action='append',
    dest='networks',
    default=[],
    help="Network ID to boot")
@utils.arg(
    '--ip',
    metavar="<ip-address>",
    action='append',
    dest='ips',
    default=[],
    help="IP address of server.")
@utils.arg('--boot-local',
           action='store_true',
           default=False,
           help='boot from image locally or boot from a new volume. Default=False.')
@utils.arg(
    '--description',
    metavar='<description>',
    dest='description',
    default=None,
    help='Description for the server.')
@utils.require_dc
def do_server_create(gc, args):
    """Boot a new server."""
    boot_args, boot_kwargs = _boot(gc, args)

    gc.servers.create(*boot_args, **boot_kwargs)


@utils.arg(
    'server', metavar='<server>', nargs='+',
    help='Name or ID of server(s).')
@utils.require_dc
def do_server_delete(gc, args):
    """Immediately shut down and delete specified server(s)."""
    utils.do_action_on_many(
        lambda s: _find_server(gc, s).delete(),
        args.server,
        "Request to delete server %s has been accepted.",
        "Unable to delete the specified server(s).")


@utils.arg(
    'server', metavar='<server>',
    help='Name (old name) or ID of server.')
@utils.arg(
    '--name',
    metavar='<name>',
    dest='name',
    default=None,
    help='New name for the server.')
@utils.arg(
    '--description',
    metavar='<description>',
    dest='description',
    default=None,
    help='New description for the server. If it equals to empty string '
         '(i.g. ""), the server description will be removed.')
@utils.require_dc
def do_server_update(gc, args):
    """Update the name or the description for a server."""
    update_kwargs = {}
    if args.name:
        update_kwargs["name"] = args.name
    # NOTE(andreykurilin): `do_update` method is used by `do_rename` method,
    # which do not have description argument at all. When `do_rename` will be
    # removed after deprecation period, feel free to change the check below to:
    #     `if args.description:`
    if "description" in args and args.description is not None:
        update_kwargs["description"] = args.description
    _find_server(gc, args.server).update(**update_kwargs)


@utils.arg(
    'server',
    metavar='<server>', nargs='+',
    help='Name or ID of server(s).')
@utils.require_dc
def do_server_start(gc, args):
    """Start the server(s)."""
    utils.do_action_on_many(
        lambda s: _find_server(gc, s).start(),
        args.server,
        "Request to start server %s has been accepted.",
        "Unable to start the specified server(s).")


@utils.arg(
    'server',
    metavar='<server>', nargs='+',
    help='Name or ID of server(s).')
@utils.require_dc
def do_server_stop(gc, args):
    """Stop the server(s)."""
    utils.do_action_on_many(
        lambda s: _find_server(gc, s).stop(),
        args.server,
        "Request to stop server %s has been accepted.",
        "Unable to stop the specified server(s).")


@utils.arg(
    '--hard',
    dest='reboot_type',
    action='store_const',
    const=servers.REBOOT_HARD,
    default=servers.REBOOT_SOFT,
    help='Perform a hard reboot (instead of a soft one). '
           'Note: Ironic does not currently support soft reboot; '
           'consequently, bare metal nodes will always do a hard '
           'reboot, regardless of the use of this option.')
@utils.arg(
    'server',
    metavar='<server>', nargs='+',
    help='Name or ID of server(s).')
@utils.require_dc
def do_server_reboot(gc, args):
    """Reboot a server."""
    servers = [_find_server(gc, s) for s in args.server]
    utils.do_action_on_many(
        lambda s: s.reboot(args.reboot_type),
        servers,
        "Request to reboot server %s has been accepted.",
        "Unable to reboot the specified server(s).")


@utils.arg('server', metavar='<server>', help='Name or ID of server.')
@utils.require_dc
def do_server_get_vnc_console(gc, args):
    """Get a vnc console to a server."""
    server = _find_server(gc, args.server)
    data = server.get_vnc_console('NOVNC')

    print_console(gc, data)


@utils.arg('server', metavar='<server>', help='Name or ID of server.')
@utils.require_dc
def do_server_show(gc, args):
    """Show details about the given server."""
    _print_server(gc, args)


@utils.arg('server', metavar='<server>', help='Name or ID of server.')
@utils.require_dc
def do_interface_list(gc, args):
    """List interfaces attached to a server."""
    server = _find_server(gc, args.server)

    res = server.interface_list()
    if isinstance(res, list):
        _print_interfaces(res)


@utils.arg('server', metavar='<server>', help='Name or ID of server.')
@utils.arg(
    '--port-id',
    metavar='<port_id>',
    help='Port ID.',
    dest="port_id")
@utils.arg(
    '--net-id',
    metavar='<net_id>',
    help='Network ID',
    default=None, dest="net_id")
@utils.arg(
    '--fixed-ip',
    metavar='<fixed_ip>',
    help='Requested fixed IP.',
    default=None, dest="fixed_ip")
@utils.require_dc
def do_interface_attach(gc, args):
    """Attach a network interface to a server."""
    server = _find_server(gc, args.server)

    res = server.interface_attach(args.port_id, args.net_id, args.fixed_ip)
    if isinstance(res, dict):
        utils.print_dict(res)


@utils.arg('server', metavar='<server>', help='Name or ID of server.')
@utils.arg('port_id', metavar='<port_id>', help='Port ID.')
@utils.require_dc
def do_interface_detach(gc, args):
    """Detach a network interface from a server."""
    server = _find_server(gc, args.server)

    res = server.interface_detach(args.port_id)
    if isinstance(res, dict):
        utils.print_dict(res)


