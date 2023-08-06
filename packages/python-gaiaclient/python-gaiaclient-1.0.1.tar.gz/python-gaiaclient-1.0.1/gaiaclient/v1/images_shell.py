from gaiaclient.common import utils
from gaiaclient.v1 import images


@utils.arg('--limit', metavar='<LIMIT>', default=None, type=int,
           help='Maximum number of images to get.')
@utils.arg('--visibility', metavar='<VISIBILITY>',
           help='The visibility of the images to display.')
@utils.arg('--tag', metavar='<TAG>', action='append',
           help="Filter images by a user-defined tag.")
@utils.arg('--sort-key', default=[], action='append',
           choices=images.SORT_KEY_VALUES,
           help='Sort image list by specified fields.'
                ' May be used multiple times.')
@utils.arg('--sort-dir', default=[], action='append',
           choices=images.SORT_DIR_VALUES,
           help='Sort image list in specified directions.')
@utils.arg('--sort', metavar='<key>[:<direction>]', default=None,
           help=("Comma-separated list of sort keys and directions in the "
                 "form of <key>[:<asc|desc>]. Valid keys: %s. OPTIONAL."
                 ) % ', '.join(images.SORT_KEY_VALUES))
@utils.require_dc
def do_image_list(gc, args):
    """List images you can access."""
    filter_keys = ['visibility', 'tag']
    filter_items = [(key, getattr(args, key)) for key in filter_keys]
    filters = dict([item for item in filter_items if item[1] is not None])

    kwargs = {'filters': filters}
    if args.limit is not None:
        kwargs['limit'] = args.limit

    if args.sort_key:
        kwargs['sort_key'] = args.sort_key
    if args.sort_dir:
        kwargs['sort_dir'] = args.sort_dir
    if args.sort is not None:
        kwargs['sort'] = args.sort
    elif not args.sort_dir and not args.sort_key:
        kwargs['sort_key'] = 'name'
        kwargs['sort_dir'] = 'asc'

    columns = ['ID', 'Name', 'Disk_format', 'Container_format', 'Size', 'Status']

    images = gc.images.list(**kwargs)

    def convert_size(image):
        image.size = utils.make_size_human_readable(image.size)
        return image

    images = (convert_size(image) for image in images)

    utils.print_list(images, columns)
