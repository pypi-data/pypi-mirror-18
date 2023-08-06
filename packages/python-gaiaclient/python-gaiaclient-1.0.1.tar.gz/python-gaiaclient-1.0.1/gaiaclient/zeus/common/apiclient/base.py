"""
Base utilities to build API operation managers and objects on top of.
"""
import abc
import copy

from oslo_utils import strutils
import six
from six.moves.urllib import parse
from requests import Response

from gaiaclient._i18n import _
from gaiaclient.zeus.common.apiclient import exceptions


def getid(obj):
    """Return id if argument is a Resource.

    Abstracts the common pattern of allowing both an object or an object's ID
    (UUID) as a parameter when dealing with relationships.
    """
    try:
        if obj.uuid:
            return obj.uuid
    except AttributeError:
        pass
    try:
        return obj.id
    except AttributeError:
        return obj


# TODO(aababilov): call run_hooks() in HookableMixin's child classes
class HookableMixin(object):
    """Mixin so classes can register and run hooks."""
    _hooks_map = {}

    @classmethod
    def add_hook(cls, hook_type, hook_func):
        """Add a new hook of specified type.

        :param cls: class that registers hooks
        :param hook_type: hook type, e.g., '__pre_parse_args__'
        :param hook_func: hook function
        """
        if hook_type not in cls._hooks_map:
            cls._hooks_map[hook_type] = []

        cls._hooks_map[hook_type].append(hook_func)

    @classmethod
    def run_hooks(cls, hook_type, *args, **kwargs):
        """Run all hooks of specified type.

        :param cls: class that registers hooks
        :param hook_type: hook type, e.g., '__pre_parse_args__'
        :param args: args to be passed to every hook function
        :param kwargs: kwargs to be passed to every hook function
        """
        hook_funcs = cls._hooks_map.get(hook_type) or []
        for hook_func in hook_funcs:
            hook_func(*args, **kwargs)


class BaseManager(HookableMixin):
    """Basic manager type providing common operations.

    Managers interact with a particular type of API (servers, flavors, images,
    etc.) and provide CRUD operations for them.
    """
    resource_class = None

    def __init__(self, client):
        """Initializes BaseManager with `client`.

        :param client: instance of BaseClient descendant for HTTP requests
        """
        super(BaseManager, self).__init__()
        self.client = client

    def _list(self, url, response_key=None, obj_class=None, json=None):
        """List the collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'. If response_key is None - all response body
            will be used.
        :param obj_class: class for constructing the returned objects
            (self.resource_class will be used by default)
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        """
        if json:
            body = self.client.post(url, json=json).json()
        else:
            body = self.client.get(url).json()

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key] if response_key is not None else body
        # NOTE(ja): keystone returns values as list as {'values': [ ... ]}
        #           unlike other services which just return the list...
        try:
            data = data['values']
        except (KeyError, TypeError):
            pass

        return [obj_class(self, res, loaded=True) for res in data if res]

    def _get(self, url, response_key=None):
        """Get an object from collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'server'. If response_key is None - all response body
            will be used.
        """
        body = self.client.get(url).json()
        data = body[response_key] if response_key is not None else body
        return self.resource_class(self, data, loaded=True)

    def _head(self, url):
        """Retrieve request headers for an object.

        :param url: a partial URL, e.g., '/servers'
        """
        resp = self.client.head(url)
        return resp.status_code == 204

    def _post(self, url, json, response_key=None, return_raw=False):
        """Create an object.

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'server'. If response_key is None - all response body
            will be used.
        :param return_raw: flag to force returning raw JSON instead of
            Python object of self.resource_class
        """
        body = self.client.post(url, json=json).json()
        data = body[response_key] if response_key is not None else body
        if return_raw:
            return data
        return self.resource_class(self, data)

    def _put(self, url, json=None, response_key=None):
        """Update an object with PUT method.

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'. If response_key is None - all response body
            will be used.
        """
        resp = self.client.put(url, json=json)
        # PUT requests may not return a body
        if resp.content:
            body = resp.json()
            if response_key is not None:
                return self.resource_class(self, body[response_key])
            else:
                return self.resource_class(self, body)

    def _patch(self, url, json=None, response_key=None):
        """Update an object with PATCH method.

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'. If response_key is None - all response body
            will be used.
        """
        body = self.client.patch(url, json=json).json()
        if response_key is not None:
            return self.resource_class(self, body[response_key])
        else:
            return self.resource_class(self, body)

    def _delete(self, url):
        """Delete an object.

        :param url: a partial URL, e.g., '/servers/my-server'
        """
        return self.client.delete(url)


@six.add_metaclass(abc.ABCMeta)
class ManagerWithFind(BaseManager):
    """Manager with additional `find()`/`findall()` methods."""

    @abc.abstractmethod
    def list(self):
        pass

    def find(self, **kwargs):
        """Find a single item with attributes matching ``**kwargs``.

        This isn't very efficient: it loads the entire list then filters on
        the Python side.
        """
        matches = self.findall(**kwargs)
        num_matches = len(matches)
        if num_matches == 0:
            msg = _("No %(name)s matching %(args)s.") % {
                'name': self.resource_class.__name__,
                'args': kwargs
            }
            raise exceptions.NotFound(msg)
        elif num_matches > 1:
            raise exceptions.NoUniqueMatch()
        else:
            return matches[0]

    def findall(self, **kwargs):
        """Find all items with attributes matching ``**kwargs``.

        This isn't very efficient: it loads the entire list then filters on
        the Python side.
        """
        found = []
        searches = kwargs.items()

        for obj in self.list():
            try:
                if all(getattr(obj, attr) == value
                       for (attr, value) in searches):
                    found.append(obj)
            except AttributeError:
                continue

        return found


class ManagerWithDcId(ManagerWithFind):
    dc_id = None

    @property
    def dc(self):
        return self.dc_id

    @dc.setter
    def dc(self, value):
        self.dc_id = value

    def _build_headers(self):
        if self.dc is None:
            raise exceptions.HeaderRequiredError('X-Dc-Id')

        hdrs = {}
        hdrs['X-Dc-Id'] = self.dc
        return hdrs

    def _list(self, url, response_key, obj_class=None, body=None):
        resp, body = self.client.get(url, headers=self._build_headers())

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key]
        return ListWithMeta([obj_class(self, res, loaded=True) for res in data if res], resp)

    def _get(self, url, response_key=None):
        resp, body = self.client.get(url, headers=self._build_headers())
        if response_key is not None:
            content = body[response_key]
        else:
            return resp, body
        return self.resource_class(self, content, loaded=True,
                                   resp=resp)

    def _delete(self, url):
        resp, body = self.client.delete(url, headers=self._build_headers())
        return self.convert_into_with_meta(body, resp)

    def _update(self, url, body, response_key=None, **kwargs):
        self.run_hooks('modify_body_for_update', body, **kwargs)
        resp, body = self.client.put(url, headers=self._build_headers(), data=body)
        if body:
            if response_key:
                return self.resource_class(self, body[response_key], resp=resp)
            else:
                return self.resource_class(self, body, resp=resp)
        else:
            return StrWithMeta(body, resp)

    def _post(self, url, data=None, response_key=None, return_raw=False):
        """Create an object.

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'server'. If response_key is None - all response body
            will be used.
        :param return_raw: flag to force returning raw JSON instead of
            Python object of self.resource_class
        """
        resp, body = self.client.post(url, headers=self._build_headers(), data=data)
        data = body[response_key] if response_key is not None else body
        if return_raw:
            return resp, data
        return self.resource_class(self, data)

    def convert_into_with_meta(self, item, resp):
        if isinstance(item, six.string_types):
            if six.PY2 and isinstance(item, six.text_type):
                return UnicodeWithMeta(item, resp)
            else:
                return StrWithMeta(item, resp)
        elif isinstance(item, six.binary_type):
            return BytesWithMeta(item, resp)
        elif isinstance(item, list):
            return ListWithMeta(item, resp)
        elif isinstance(item, tuple):
            return TupleWithMeta(item, resp)
        elif item is None:
            return TupleWithMeta((), resp)
        else:
            return DictWithMeta(item, resp)

    def _create(self, url, body, response_key, return_raw=False, **kwargs):
        self.run_hooks('modify_body_for_create', body, **kwargs)
        resp, body = self.client.post(url, headers=self._build_headers(), data=body)
        if return_raw:
            return self.convert_into_with_meta(body[response_key], resp)

        return self.resource_class(self, body[response_key], resp=resp)


class CrudManager(BaseManager):
    """Base manager class for manipulating entities.

    Children of this class are expected to define a `collection_key` and `key`.

    - `collection_key`: Usually a plural noun by convention (e.g. `entities`);
      used to refer collections in both URL's (e.g.  `/v3/entities`) and JSON
      objects containing a list of member resources (e.g. `{'entities': [{},
      {}, {}]}`).
    - `key`: Usually a singular noun by convention (e.g. `entity`); used to
      refer to an individual member of the collection.

    """
    collection_key = None
    key = None

    def build_url(self, base_url=None, **kwargs):
        """Builds a resource URL for the given kwargs.

        Given an example collection where `collection_key = 'entities'` and
        `key = 'entity'`, the following URL's could be generated.

        By default, the URL will represent a collection of entities, e.g.::

            /entities

        If kwargs contains an `entity_id`, then the URL will represent a
        specific member, e.g.::

            /entities/{entity_id}

        :param base_url: if provided, the generated URL will be appended to it
        """
        url = base_url if base_url is not None else ''

        url += '/%s' % self.collection_key

        # do we have a specific entity?
        entity_id = kwargs.get('%s_id' % self.key)
        if entity_id is not None:
            url += '/%s' % entity_id

        return url

    def _filter_kwargs(self, kwargs):
        """Drop null values and handle ids."""
        for key, ref in six.iteritems(kwargs.copy()):
            if ref is None:
                kwargs.pop(key)
            else:
                if isinstance(ref, Resource):
                    kwargs.pop(key)
                    kwargs['%s_id' % key] = getid(ref)
        return kwargs

    def create(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._post(
            self.build_url(**kwargs),
            {self.key: kwargs},
            self.key)

    def get(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._get(
            self.build_url(**kwargs),
            self.key)

    def head(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        return self._head(self.build_url(**kwargs))

    def list(self, base_url=None, **kwargs):
        """List the collection.

        :param base_url: if provided, the generated URL will be appended to it
        """
        kwargs = self._filter_kwargs(kwargs)

        return self._list(
            '%(base_url)s%(query)s' % {
                'base_url': self.build_url(base_url=base_url, **kwargs),
                'query': '?%s' % parse.urlencode(kwargs) if kwargs else '',
            },
            self.collection_key)

    def put(self, base_url=None, **kwargs):
        """Update an element.

        :param base_url: if provided, the generated URL will be appended to it
        """
        kwargs = self._filter_kwargs(kwargs)

        return self._put(self.build_url(base_url=base_url, **kwargs))

    def update(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)
        params = kwargs.copy()
        params.pop('%s_id' % self.key)

        return self._patch(
            self.build_url(**kwargs),
            {self.key: params},
            self.key)

    def delete(self, **kwargs):
        kwargs = self._filter_kwargs(kwargs)

        return self._delete(
            self.build_url(**kwargs))

    def find(self, base_url=None, **kwargs):
        """Find a single item with attributes matching ``**kwargs``.

        :param base_url: if provided, the generated URL will be appended to it
        """
        kwargs = self._filter_kwargs(kwargs)

        rl = self._list(
            '%(base_url)s%(query)s' % {
                'base_url': self.build_url(base_url=base_url, **kwargs),
                'query': '?%s' % parse.urlencode(kwargs) if kwargs else '',
            },
            self.collection_key)
        num = len(rl)

        if num == 0:
            msg = _("No %(name)s matching %(args)s.") % {
                'name': self.resource_class.__name__,
                'args': kwargs
            }
            raise exceptions.NotFound(msg)
        elif num > 1:
            raise exceptions.NoUniqueMatch
        else:
            return rl[0]


class Extension(HookableMixin):
    """Extension descriptor."""

    SUPPORTED_HOOKS = ('__pre_parse_args__', '__post_parse_args__')
    manager_class = None

    def __init__(self, name, module):
        super(Extension, self).__init__()
        self.name = name
        self.module = module
        self._parse_extension_module()

    def _parse_extension_module(self):
        self.manager_class = None
        for attr_name, attr_value in self.module.__dict__.items():
            if attr_name in self.SUPPORTED_HOOKS:
                self.add_hook(attr_name, attr_value)
            else:
                try:
                    if issubclass(attr_value, BaseManager):
                        self.manager_class = attr_value
                except TypeError:
                    pass

    def __repr__(self):
        return "<Extension '%s'>" % self.name


class RequestIdMixin(object):
    """Wrapper class to expose x-openstack-request-id to the caller.
    """
    def request_ids_setup(self):
        self.x_openstack_request_ids = []

    @property
    def request_ids(self):
        return self.x_openstack_request_ids

    def append_request_ids(self, resp):
        """Add request_ids as an attribute to the object
        :param resp: Response object or list of Response objects
        """
        if isinstance(resp, list):
            # Add list of request_ids if response is of type list.
            for resp_obj in resp:
                self._append_request_id(resp_obj)
        elif resp is not None:
            # Add request_ids if response contains single object.
            self._append_request_id(resp)

    def _append_request_id(self, resp):
        if isinstance(resp, Response):
            # Extract 'x-openstack-request-id' from headers if
            # response is a Response object.
            request_id = (resp.headers.get('x-openstack-request-id') or
                          resp.headers.get('x-compute-request-id'))
        else:
            # If resp is of type string or None.
            request_id = resp
        if request_id not in self.x_openstack_request_ids:
            self.x_openstack_request_ids.append(request_id)


class Resource(RequestIdMixin):
    """Base class for Zeus resources (tenant, user, etc.).

    This is pretty much just a bag for attributes.
    """

    HUMAN_ID = False
    NAME_ATTR = 'name'

    def __init__(self, manager, info, loaded=False, resp=None):
        """Populate and bind to a manager.

        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        :param loaded: prevent lazy-loading if set to True
        :param resp: Response or list of Response objects
        """
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded
        self.request_ids_setup()
        self.append_request_ids(resp)

    def __repr__(self):
        reprkeys = sorted(k
                          for k in self.__dict__.keys()
                          if k[0] != '_' and
                          k not in ['manager', 'x_openstack_request_ids'])
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    @property
    def human_id(self):
        """Human-readable ID which can be used for bash completion."""
        if self.HUMAN_ID:
            name = getattr(self, self.NAME_ATTR, None)
            if name is not None:
                return strutils.to_slug(name)
        return None

    def _add_details(self, info):
        for (k, v) in six.iteritems(info):
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass

    def __getattr__(self, k):
        if k not in self.__dict__:
            # NOTE(bcwaldon): disallow lazy-loading if already loaded once
            if not self.is_loaded():
                self.get()
                return self.__getattr__(k)

            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def get(self):
        """Support for lazy loading details.

        Some clients, such as novaclient have the option to lazy load the
        details, details which can be loaded with this function.
        """
        # set_loaded() first ... so if we have to bail, we know we tried.
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.id)
        if new:
            self._add_details(new._info)
            self.append_request_ids(new.request_ids)

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented
        # two resources of different types are not equal
        if not isinstance(other, self.__class__):
            return False
        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id
        return self._info == other._info

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_loaded(self):
        return self._loaded

    def set_loaded(self, val):
        self._loaded = val

    def to_dict(self):
        return copy.deepcopy(self._info)


class ListWithMeta(list, RequestIdMixin):
    def __init__(self, values, resp):
        super(ListWithMeta, self).__init__(values)
        self.request_ids_setup()
        self.append_request_ids(resp)


class DictWithMeta(dict, RequestIdMixin):
    def __init__(self, values, resp):
        super(DictWithMeta, self).__init__(values)
        self.request_ids_setup()
        self.append_request_ids(resp)


class TupleWithMeta(tuple, RequestIdMixin):
    def __new__(cls, values, resp):
        return super(TupleWithMeta, cls).__new__(cls, values)

    def __init__(self, values, resp):
        self.request_ids_setup()
        self.append_request_ids(resp)


class StrWithMeta(str, RequestIdMixin):
    def __new__(cls, value, resp):
        return super(StrWithMeta, cls).__new__(cls, value)

    def __init__(self, values, resp):
        self.request_ids_setup()
        self.append_request_ids(resp)


class BytesWithMeta(six.binary_type, RequestIdMixin):
    def __new__(cls, value, resp):
        return super(BytesWithMeta, cls).__new__(cls, value)

    def __init__(self, values, resp):
        self.request_ids_setup()
        self.append_request_ids(resp)


if six.PY2:
    class UnicodeWithMeta(six.text_type, RequestIdMixin):
        def __new__(cls, value, resp):
            return super(UnicodeWithMeta, cls).__new__(cls, value)

        def __init__(self, values, resp):
            self.request_ids_setup()
            self.append_request_ids(resp)

