import argparse

from gaiaclient.common import utils
from gaiaclient.zeus.common.apiclient import base
from gaiaclient import exc

from servers_shell import _find_server


def _print_volume(volume):
    utils.print_dict(volume._info)


def _translate_volume_keys(collection):
    convert = [('volumeType', 'volume_type'),
               ('os-vol-tenant-attr:tenant_id', 'tenant_id')]
    _translate_keys(collection, convert)


def _translate_volume_attachments_keys(collection):
    _translate_keys(collection,
                    [('serverId', 'server_id'),
                     ('volumeId', 'volume_id')])


def _translate_keys(collection, convert):
    for item in collection:
        keys = item.__dict__
        for from_key, to_key in convert:
            if from_key in keys and to_key not in keys:
                setattr(item, to_key, item._info[from_key])


class CheckSizeArgForCreate(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if (args.snapshot_id is None and values is None):
            parser.error('Size is a required parameter if snapshot '
                         'or source volume is not specified.')
        setattr(args, self.dest, values)


@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Filters results by a name. Default=None.')
@utils.arg('--status',
           metavar='<status>',
           default=None,
           help='Filters results by a status. Default=None.')
@utils.arg('--bootable',
           metavar='<True|true|False|false>',
           const=True,
           nargs='?',
           choices=['True', 'true', 'False', 'false'],
           help='Filters results by bootable status. Default=None.')
@utils.arg('--marker',
           metavar='<marker>',
           default=None,
           help='Begin returning volumes that appear later in the volume '
                'list than that represented by this volume id. '
                'Default=None.')
@utils.arg('--limit',
           metavar='<limit>',
           default=None,
           help='Maximum number of volumes to return. Default=None.')
@utils.arg('--sort_key',
           metavar='<sort_key>',
           default=None,
           help=argparse.SUPPRESS)
@utils.arg('--sort_dir',
           metavar='<sort_dir>',
           default=None,
           help=argparse.SUPPRESS)
@utils.require_dc
def do_volume_list(gc, args):
    """Lists all volumes."""

    search_opts = {
        'name': args.name,
        'status': args.status,
        'bootable': args.bootable
    }

    volumes = gc.volumes.list(search_opts=search_opts, marker=args.marker,
                              limit=args.limit, sort_key=args.sort_key,
                              sort_dir=args.sort_dir)

    _translate_volume_keys(volumes)

    # Create a list of servers to which the volume is attached
    for vol in volumes:
        servers = [base.getid(s) for s in vol.attachments]
        setattr(vol, 'attached_to', ','.join(map(str, servers)))

    key_list = ['ID', 'Status', 'Name', 'Size', 'Volume Type', 'Bootable', 'Attached to']

    utils.print_list(volumes, key_list)


@utils.arg('size',
           metavar='<size>',
           nargs='?',
           type=int,
           action=CheckSizeArgForCreate,
           help='Size of volume, in GiBs. (Required unless '
                'snapshot-id/source-volid is specified).')
@utils.arg('--snapshot-id',
           metavar='<snapshot-id>',
           default=None,
           help='Creates volume from snapshot ID. Default=None.')
@utils.arg('--snapshot_id',
           help=argparse.SUPPRESS)
@utils.arg('--image-id',
           metavar='<image-id>',
           default=None,
           help='Creates volume from image ID. Default=None.')
@utils.arg('--image',
           metavar='<image>',
           default=None,
           help='Creates a volume from image (ID or name). Default=None.')
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Volume name. Default=None.')
@utils.arg('--description',
           metavar='<description>',
           default=None,
           help='Volume description. Default=None.')
@utils.arg('--volume-type',
           metavar='<volume-type>',
           default=None,
           help='Volume type. Default=None.')
@utils.require_dc
def do_volume_create(gc, args):
    """Creates a volume."""

    image_ref = args.image_id or args.image

    volume = gc.volumes.create(args.size,
                               snapshot_id=args.snapshot_id,
                               name=args.name,
                               description=args.description,
                               volume_type=args.volume_type,
                               imageRef=image_ref,
                               )
    info = dict()
    volume = gc.volumes.get(volume.id)
    info.update(volume._info)

    if 'readonly' in info['metadata']:
        info['readonly'] = info['metadata']['readonly']

    info.pop('links', None)
    utils.print_dict(info)


@utils.arg('--cascade',
           action='store_true',
           default=False,
           help='Remove any snapshots along with volume. Default=False.')
@utils.arg('volume',
           metavar='<volume>', nargs='+',
           help='Name or ID of volume or volumes to delete.')
@utils.require_dc
def do_volume_delete(gc, args):
    """Removes one or more volumes."""
    failure_count = 0
    for volume in args.volume:
        try:
            utils.find_volume(gc, volume).delete(cascade=args.cascade)
            print("Request to delete volume %s has been accepted." % (volume))
        except Exception as e:
            failure_count += 1
            print("Delete for volume %s failed: %s" % (volume, e))
    if failure_count == len(args.volume):
        raise exc.CommandError("Unable to delete any of the specified volumes.")


@utils.arg('volume',
           metavar='<volume>',
           help='Old name or ID of volume to update.')
@utils.arg('--name',
           metavar='<name>',
           default=None,
           help='Volume new name.')
@utils.arg('--description',
           metavar='<description>',
           default=None,
           help='Volume description.')
@utils.require_dc
def do_volume_update(gc, args):
    """Updates volume."""
    volume = utils.find_volume(gc, args.volume)

    kwargs = {}
    if args.name:
        kwargs['name'] = args.name
    if args.description:
        kwargs['description'] = args.description

    volume.update(**kwargs)


@utils.arg(
    'server',
    metavar='<server>',
    help='Name or ID of server.')
@utils.arg(
    'volume',
    metavar='<volume>',
    help='ID of the volume to attach.')
@utils.arg(
    'device', metavar='<device>', default=None, nargs='?',
    help='Name of the device e.g. /dev/vdb.')
@utils.require_dc
def do_volume_attach(gc, args):
    """Attach a volume to a server."""
    if args.device == 'auto':
        args.device = None

    volume = gc.volumes.create_server_volume(_find_server(gc, args.server).id,
                                             args.volume,
                                             args.device)
    _print_volume(volume)


@utils.arg(
    'server',
    metavar='<server>',
    help='Name or ID of server.')
@utils.arg(
    'attachment_id',
    metavar='<volume>',
    help='ID of the volume to detach.')
@utils.require_dc
def do_volume_detach(gc, args):
    """Detach a volume from a server."""
    gc.volumes.delete_server_volume(_find_server(gc, args.server).id,
                                    args.attachment_id)


@utils.arg(
    'server',
    metavar='<server>',
    help='Name or ID of server.')
@utils.require_dc
def do_server_volumes(gc, args):
    """List all the volumes attached to a server."""
    volumes = gc.volumes.get_server_volumes(_find_server(gc, args.server).id)
    _translate_volume_attachments_keys(volumes)
    utils.print_list(volumes, ['ID', 'DEVICE', 'SERVER ID', 'VOLUME ID'])
