from gaiaclient.common import utils
from gaiaclient import exc as exceptions

from oslo_utils import strutils


def _print_flavor_list(flavors, show_extra_specs=False):
    _translate_flavor_keys(flavors)

    headers = [
        'ID',
        'Name',
        'Memory_MB',
        'Disk',
        'Ephemeral',
        'Swap',
        'VCPUs',
        'RXTX_Factor',
        'Is_Public',
    ]

    if show_extra_specs:
        formatters = {'extra_specs': _print_flavor_extra_specs}
        headers.append('extra_specs')
    else:
        formatters = {}

    utils.print_list(flavors, headers, formatters)


def _translate_flavor_keys(collection):
    _translate_keys(collection, [('ram', 'memory_mb')])


def _translate_keys(collection, convert):
    for item in collection:
        keys = item.__dict__.keys()
        for from_key, to_key in convert:
            if from_key in keys and to_key not in keys:
                setattr(item, to_key, item._info[from_key])


def _print_flavor_extra_specs(flavor):
    try:
        return flavor.get_keys()
    except exceptions.NotFound:
        return "N/A"


@utils.require_dc
def do_flavor_list(gc, args):
    """Print a list of available 'flavors' (sizes of servers)."""

    flavors = gc.flavors.list()

    _print_flavor_list(flavors)


@utils.arg(
    'name',
    metavar='<name>',
    help="Unique name of the new flavor.")
@utils.arg(
    'id',
    metavar='<id>',
    help="Unique ID of the new flavor."
         " Specifying 'auto' will generated a UUID for the ID.")
@utils.arg(
    'ram',
    metavar='<ram>',
    help="Memory size in MB.")
@utils.arg(
    'disk',
    metavar='<disk>',
    help="Disk size in GB.")
@utils.arg(
    '--ephemeral',
    metavar='<ephemeral>',
    help="Ephemeral space size in GB (default 0).",
    default=0)
@utils.arg(
    'vcpus',
    metavar='<vcpus>',
    help="Number of vcpus")
@utils.arg(
    '--swap',
    metavar='<swap>',
    help="Swap space size in MB (default 0).",
    default=0)
@utils.arg(
    '--rxtx-factor',
    metavar='<factor>',
    help="RX/TX factor (default 1).",
    default=1.0)
@utils.arg(
    '--is-public',
    metavar='<is-public>',
    help="Make flavor accessible to the public (default true).",
    type=lambda v: strutils.bool_from_string(v, True),
    default=True)
@utils.require_dc
def do_flavor_create(gc, args):
    """Create a new flavor."""
    f = gc.flavors.create(args.name, args.ram, args.vcpus, args.disk, args.id,
                          args.ephemeral, args.swap, args.rxtx_factor,
                          args.is_public)
    _print_flavor_list([f])
