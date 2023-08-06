from __future__ import print_function

import copy
import functools

from oslo_utils import encodeutils
from oslo_utils import strutils

from gaiaclient.common import utils
from gaiaclient import exc
import gaiaclient.v1.dcs


_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


REQUIRED_FIELDS = ('auth_url', 'admin_username', 'admin_password', 'admin_tenant', 'transport_url')


@utils.arg('--sort-key', default='name',
           choices=gaiaclient.v1.dcs.SORT_KEY_VALUES,
           help='Sort dc list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=gaiaclient.v1.dcs.SORT_DIR_VALUES,
           help='Sort dc list in specified direction.')
def do_dc_list(gc, args):
    """List dcs you can access."""

    kwargs = dict()
    kwargs['sort_key'] = args.sort_key
    kwargs['sort_dir'] = args.sort_dir

    dcs = gc.dcs.list(**kwargs)
    columns = ['ID', 'Name', 'Status']
    utils.print_list(dcs, columns)


def _dc_show(dc, max_column_width=80):
    # Flatten dc properties dict for display
    info = copy.deepcopy(dc._info)
    utils.print_dict(info, max_column_width=max_column_width)


@utils.arg('dc', metavar='<DC>', help='Name or ID of dc to describe.')
@utils.arg('--max-column-width', metavar='<integer>', default=80,
           help='The max column width of the printed table.')
def do_dc_show(gc, args):
    """Describe a specific dc."""
    dc_id = utils.find_resource(gc.dcs, args.dc).id
    dc = gc.dcs.get(dc_id)
    _dc_show(dc, max_column_width=int(args.max_column_width))


@utils.arg('name', metavar='<NAME>',
           help='Name of dc.')
@utils.arg('--auth-url', metavar='<AUTH_URL>',
           help='Auth url of dc.')
@utils.arg('--admin-username', metavar='<ADMIN_USERNAME>',
           help='Admin username of dc.')
@utils.arg('--admin-password', metavar='<ADMIN_PASSWORD>',
           help='Admin password of dc.')
@utils.arg('--admin-tenant', metavar='<ADMIN_TENANT>',
           help='Admin tenant of dc.')
@utils.arg('--transport-url', metavar='<TRANSPORT_URL>',
           help='Messaging transport url.')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='Description of dc.')
@utils.require_fields(REQUIRED_FIELDS)
def do_dc_create(gc, args):
    """Create a new dc."""
    # Filter out None values
    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))

    # Filter out values we can't use
    CREATE_PARAMS = gaiaclient.v1.dcs.CREATE_PARAMS
    fields = dict(filter(lambda x: x[0] in CREATE_PARAMS, fields.items()))

    dc = gc.dcs.create(**fields)
    _dc_show(dc)


@utils.arg('dc', metavar='<DC>', help='Name or ID of dc to modify.')
@utils.arg('--name', metavar='<NAME>',
           help='Name of dc.')
@utils.arg('--auth-url', metavar='<AUTH_URL>',
           help='Auth url of dc.')
@utils.arg('--admin-username', metavar='<ADMIN_USERNAME>',
           help='Admin username of dc.')
@utils.arg('--admin-password', metavar='<ADMIN_PASSWORD>',
           help='Admin password of dc.')
@utils.arg('--admin-tenant', metavar='<ADMIN_TENANT>',
           help='Admin tenant of dc.')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='Description of dc.')
def do_dc_update(gc, args):
    """Update a specific dc."""
    # Filter out None values
    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))

    dc_arg = fields.pop('dc')
    dc = utils.find_resource(gc.dcs, dc_arg)

    # Filter out values we can't use
    UPDATE_PARAMS = gaiaclient.v1.dcs.UPDATE_PARAMS
    fields = dict(filter(lambda x: x[0] in UPDATE_PARAMS, fields.items()))

    dc = gc.dcs.update(dc, **fields)
    _dc_show(dc)


@utils.arg('dcs', metavar='<DC>', nargs='+',
           help='Name or ID of dc(s) to delete.')
def do_dc_delete(gc, args):
    """Delete specified dc(s)."""
    for args_dc in args.dcs:
        dc = utils.find_resource(gc.dcs, args_dc)
        try:
            if args.verbose:
                print('Requesting dc delete for %s ...' %
                      encodeutils.safe_decode(args_dc), end=' ')

            gc.dcs.delete(dc)

            if args.verbose:
                print('[Done]')

        except exc.HTTPException as e:
            if args.verbose:
                print('[Fail]')
            print('%s: Unable to delete dc %s' % (e, args_dc))

