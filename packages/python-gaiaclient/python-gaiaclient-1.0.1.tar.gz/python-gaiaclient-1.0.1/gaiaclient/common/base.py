"""
Base utilities to build API operation managers and objects on top of.

DEPRECATED post v.0.12.0. Use 'gaiaclient.zeus.common.apiclient.base'
instead of this module."
"""

import warnings

from gaiaclient.zeus.common.apiclient import base


warnings.warn("The 'gaiaclient.common.base' module is deprecated post "
              "v.0.12.0. Use 'gaiaclient.zeus.common.apiclient.base' "
              "instead of this one.", DeprecationWarning)


getid = base.getid
Manager = base.ManagerWithFind
Resource = base.Resource
