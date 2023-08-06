"""
Flavor interface.
"""

from oslo_utils import strutils
from six.moves.urllib import parse

from gaiaclient.zeus.common.apiclient import base
from gaiaclient.common import exceptions
from gaiaclient.common import utils


class Flavor(base.Resource):
    """A flavor is an available hardware configuration for a server."""
    HUMAN_ID = True

    def __repr__(self):
        return "<Flavor: %s>" % self.name

    @property
    def ephemeral(self):
        """Provide a user-friendly accessor to OS-FLV-EXT-DATA:ephemeral."""
        return self._info.get("OS-FLV-EXT-DATA:ephemeral", 'N/A')

    @property
    def is_public(self):
        """Provide a user-friendly accessor to os-flavor-access:is_public."""
        return self._info.get("os-flavor-access:is_public", 'N/A')


class FlavorManager(base.ManagerWithDcId):
    """Manage :class:`Flavor` resources."""
    resource_class = Flavor

    def _build_body(self, name, ram, vcpus, disk, id, swap,
                    ephemeral, rxtx_factor, is_public):

        return {
            "flavor": {
                "name": name,
                "ram": ram,
                "vcpus": vcpus,
                "disk": disk,
                "id": id,
                "swap": swap,
                "OS-FLV-EXT-DATA:ephemeral": ephemeral,
                "rxtx_factor": rxtx_factor,
                "os-flavor-access:is_public": is_public,
            }
        }

    def list(self, is_public=True, marker=None, limit=None,
             sort_key=None, sort_dir=None, **kwargs):
        """Get a list of all flavors.

        :param is_public: Filter flavors with provided access type (optional).
                          None means give all flavors and only admin has query
                          access to all flavor types.
        :param marker: Begin returning flavors that appear later in the flavor
                       list than that represented by this flavor id (optional).
        :param limit: maximum number of flavors to return (optional).
        :param sort_key: Flavors list sort key (optional).
        :param sort_dir: Flavors list sort direction (optional).
        :returns: list of :class:`Flavor`.
        """
        qparams = {}
        # is_public is ternary - None means give all flavors.
        # By default Nova assumes True and gives admins public flavors
        # and flavors from their own projects only.
        if marker:
            qparams['marker'] = str(marker)
        if limit:
            qparams['limit'] = int(limit)
        if sort_key:
            qparams['sort_key'] = str(sort_key)
        if sort_dir:
            qparams['sort_dir'] = str(sort_dir)
        if not is_public:
            qparams['is_public'] = is_public
        qparams = sorted(qparams.items(), key=lambda x: x[0])
        query_string = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list("/v1/flavors/%s" % query_string, "flavors")

    def get(self, flavor):
        """Get a specific flavor.

        :param flavor: The ID of the :class:`Flavor` to get.
        :returns: :class:`Flavor`
        """
        return self._get("/v1/flavors/%s" % base.getid(flavor), "flavor")

    def create(self, name, ram, vcpus, disk, flavorid="auto",
               ephemeral=0, swap=0, rxtx_factor=1.0, is_public=True):
        """Create a flavor.

        :param name: Descriptive name of the flavor
        :param ram: Memory in MB for the flavor
        :param vcpus: Number of VCPUs for the flavor
        :param disk: Size of local disk in GB
        :param flavorid: ID for the flavor (optional). You can use the reserved
                         value ``"auto"`` to have Nova generate a UUID for the
                         flavor in cases where you cannot simply pass ``None``.
        :param swap: Swap space in MB
        :param rxtx_factor: RX/TX factor
        :returns: :class:`Flavor`
        """

        try:
            ram = int(ram)
        except (TypeError, ValueError):
            raise exceptions.CommandError("Ram must be an integer.")
        try:
            vcpus = int(vcpus)
        except (TypeError, ValueError):
            raise exceptions.CommandError("VCPUs must be an integer.")
        try:
            disk = int(disk)
        except (TypeError, ValueError):
            raise exceptions.CommandError("Disk must be an integer.")

        if flavorid == "auto":
            flavorid = None

        try:
            swap = int(swap)
        except (TypeError, ValueError):
            raise exceptions.CommandError(_("Swap must be an integer."))
        try:
            ephemeral = int(ephemeral)
        except (TypeError, ValueError):
            raise exceptions.CommandError(_("Ephemeral must be an integer."))
        try:
            rxtx_factor = float(rxtx_factor)
        except (TypeError, ValueError):
            raise exceptions.CommandError(_("rxtx_factor must be a float."))

        try:
            is_public = strutils.bool_from_string(is_public, True)
        except Exception:
            raise exceptions.CommandError(_("is_public must be a boolean."))

        body = self._build_body(name, ram, vcpus, disk, flavorid, swap,
                                ephemeral, rxtx_factor, is_public)

        return self._create("/v1/flavors/", body, "flavor")
