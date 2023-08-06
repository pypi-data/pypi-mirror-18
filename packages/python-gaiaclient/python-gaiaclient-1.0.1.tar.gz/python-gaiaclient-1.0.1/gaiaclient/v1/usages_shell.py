from gaiaclient.common import utils
import gaiaclient


@utils.require_dc
def do_usage_list(gc, args):
    """List usages."""
    usages = gc.usages.list()
    columns = ["Name", "Quota", "Used", "Available"]

    utils.print_list(usages, columns)
