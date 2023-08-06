from gaiaclient.common import utils
from gaiaclient.v1 import networks


@utils.require_dc
def do_net_list(gc, args):
    """List networks you can access."""
    kwargs = {}

    columns = ['ID', 'Name', 'subnets']

    nets = gc.networks.list(**kwargs)

    utils.print_list(nets, columns)


@utils.require_dc
def do_subnet_list(gc, args):
    """List networks you can access."""
    kwargs = {}

    columns = ['ID', 'Name', 'Cidr', 'Allocation Pools']

    subnets = gc.subnets.list(**kwargs)

    utils.print_list(subnets, columns)
