from gaiaclient.common import utils
import gaiaclient


def do_version_list(gc, args):
    """List all API versions."""
    versions = gc.versions.list()
    columns = ["Id", "Status", "Min Version", "Max Version", "Release Version"]

    print("Client supported API versions:")
    print("Minimum version %(v)s" %
          {'v': gaiaclient.API_MIN_VERSION})
    print("Maximum version %(v)s" %
          {'v': gaiaclient.API_MAX_VERSION})

    print("\nServer supported API versions:")
    utils.print_list(versions, columns)
