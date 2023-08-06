import errno
import json
import testtools

import six
from six.moves.urllib import parse

from gaiaclient.tests import utils
from gaiaclient.v1 import client
from gaiaclient.v1 import dcs
from gaiaclient.v1 import dcs_shell as shell


fixtures = {
    '/v1/dcs/': {
        'POST': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'dc':
                {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            },
        ),
    },
    '/v1/dcs/?limit=20': {
        'GET': (
            {},
            {'dcs': [
                {
                    'id': 'a',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/dcs/?is_public=None&limit=20': {
        'GET': (
            {'x-openstack-request-id': 'req-1234'},
            {'images': [
                {
                    'id': 'a',
                    'owner': 'A',
                    'is_public': 'True',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b',
                    'owner': 'B',
                    'is_public': 'False',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'c',
                    'is_public': 'False',
                    'name': 'image-3',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?is_public=None&limit=5': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'a',
                    'owner': 'A',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b',
                    'owner': 'B',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b2',
                    'owner': 'B',
                    'name': 'image-3',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'c',
                    'name': 'image-3',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=5': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'a',
                    'owner': 'A',
                    'is_public': 'False',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b',
                    'owner': 'A',
                    'is_public': 'False',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b2',
                    'owner': 'B',
                    'name': 'image-3',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'c',
                    'is_public': 'True',
                    'name': 'image-3',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=20&marker=a': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'b',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'c',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=1': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'a',
                    'name': 'image-0',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=1&marker=a': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'b',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=2': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'a',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=2&marker=b': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'c',
                    'name': 'image-3',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=20&name=foo': {
        'GET': (
            {},
            {'images': [
                {
                    'id': 'a',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
                {
                    'id': 'b',
                    'name': 'image-2',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/images/?limit=20&property-ping=pong':
    {
        'GET': (
            {},
            {'images': [
                {
                    'id': '1',
                    'name': 'image-1',
                    'properties': {'arch': 'x86_64'},
                },
            ]},
        ),
    },
    '/v1/dcs/?sort_dir=desc': {
        'GET': (
            {},
            {'dcs': [
                {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                },
                {
                    'id': '2',
                    'name': 'dc-2',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                },
            ]},
        ),
    },
    '/v1/dcs/?sort_key=name': {
        'GET': (
            {},
            {'dcs': [
                {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                },
                {
                    'id': '2',
                    'name': 'dc-2',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                },
            ]},
        ),
    },
    '/v1/dcs/1': {
        'GET': (
            {},
            {
                'dc': {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at' : '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
        'PUT': (
            {},
            {
                'dc': {
                    'id': '1',
                    'name': 'dc-5',
                    'description': 'desc5',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
        'DELETE': ({}, None),
    },
    '/v1/images/2': {
        'HEAD': (
            {
                'x-image-meta-id': '2'
            },
            None,
        ),
        'GET': (
            {
                'x-image-meta-checksum': 'wrong'
            },
            'YYY',
        ),
    },
    '/v1/dcs/3': {
        'GET': (
            {},
            {
                'dc': {
                    'id': '1',
                    'name': u"ni\xf1o",
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
    },
    '/v1/dcs/4': {
        'GET': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'dc': {
                    'id': '1',
                    'name': 'dc-5',
                    'description': 'desc',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            },
        ),
        'PUT': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            {
                'dc': {
                    'id': '4',
                    'name': 'dc-3',
                    'description': 'desc-4',
                    'url': 'http://keystone:5000/v3',
                    'status': 'Active',
                    'created_at': '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            },
        ),
        'DELETE': (
            {
                'x-openstack-request-id': 'req-1234',
            },
            None),
    },
    '/v1/images/v2_created_img': {
        'PUT': (
            {},
            json.dumps({
                "image": {
                    "status": "queued",
                    "deleted": False,
                    "container_format": "bare",
                    "min_ram": 0,
                    "updated_at": "2013-12-20T01:51:45",
                    "owner": "foo",
                    "min_disk": 0,
                    "is_public": False,
                    "deleted_at": None,
                    "id": "v2_created_img",
                    "size": None,
                    "name": "bar",
                    "checksum": None,
                    "created_at": "2013-12-20T01:50:38",
                    "disk_format": "qcow2",
                    "properties": {},
                    "protected": False
                }
            })
        ),
    },
}


class DCManagerTest(testtools.TestCase):

    def setUp(self):
        super(DCManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = dcs.DCManager(self.api)

    def test_list_with_sort_dir(self):
        list(self.mgr.list(sort_dir='desc'))
        url = '/v1/dcs/?sort_dir=desc'
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)

    def test_list_with_sort_key(self):
        list(self.mgr.list(sort_key='name'))
        url = '/v1/dcs/?sort_key=name'
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)

    def test_get(self):
        dc = self.mgr.get('1')
        expect = [('GET', '/v1/dcs/1', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', dc.id)
        self.assertEqual('dc-1', dc.name)
        self.assertEqual('Active', dc.status)
        self.assertEqual('2016-06-20T10:45:59.000000', dc.created_at)

    def test_get_int(self):
        dc = self.mgr.get(1)
        expect = [('GET', '/v1/dcs/1', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', dc.id)
        self.assertEqual('dc-1', dc.name)
        self.assertEqual('Active', dc.status)
        self.assertEqual('2016-06-20T10:45:59.000000', dc.created_at)

    def test_get_encoding(self):
        dc = self.mgr.get('3')
        self.assertEqual(u"ni\xf1o", dc.name)

    def test_get_req_id(self):
        params = {'return_req_id': []}
        self.mgr.get('4', **params)
        expect_req_id = ['req-1234']
        self.assertEqual(expect_req_id, params['return_req_id'])

    def test_delete(self):
        self.mgr.delete('1')
        expect = [('DELETE', '/v1/dcs/1', {}, None)]
        self.assertEqual(expect, self.api.calls)

    def test_delete_req_id(self):
        params = {
            'return_req_id': []
        }
        self.mgr.delete('4', **params)
        expect = [('DELETE', '/v1/dcs/4', {}, None)]
        self.assertEqual(self.api.calls, expect)
        expect_req_id = ['req-1234']
        self.assertEqual(expect_req_id, params['return_req_id'])

    def test_create(self):
        params = {
            'name': 'dc-1',
            'auth_url': 'http://keystone:5000/v3',
        }
        dc = self.mgr.create(**params)
        expect_data = [('dc', {'name': 'dc-1', 'auth_url': 'http://keystone:5000/v3'})]
        expect = [('POST', '/v1/dcs/', {}, expect_data)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', dc.id)
        self.assertEqual('dc-1', dc.name)
        self.assertEqual('Active', dc.status)
        self.assertEqual('http://keystone:5000/v3', dc.url)

    def test_create_req_id(self):
        params = {
            'name': 'dc-1',
            'auth_url': 'http://keystone:5000/v3',
            'return_req_id': []
        }
        dc = self.mgr.create(**params)
        expect_data = [('dc', {'name': 'dc-1', 'auth_url': 'http://keystone:5000/v3'})]
        expect = [('POST', '/v1/dcs/', {}, expect_data)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', dc.id)
        expect_req_id = ['req-1234']
        self.assertEqual(expect_req_id, params['return_req_id'])

    def test_update(self):
        fields = {
            'name': 'dc-1',
            'auth_url': 'http://keystone:5000/v3',
        }
        dc = self.mgr.update('1', **fields)
        expect_data = [('dc', {'name': 'dc-1', 'auth_url': 'http://keystone:5000/v3'})]
        expect = [('PUT', '/v1/dcs/1', {}, expect_data)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', dc.id)
        self.assertEqual('dc-5', dc.name)
        self.assertEqual('Active', dc.status)
        self.assertEqual('http://keystone:5000/v3', dc.url)

    def test_update_req_id(self):
        fields = {
            'name': 'dc-3',
            'description': 'desc-3',
            'return_req_id': []
        }
        self.mgr.update('4', **fields)
        expect_data = [('dc', {'name': 'dc-3',
                               'description': 'desc-3'
                               })]
        expect = [('PUT', '/v1/dcs/4', {}, expect_data)]
        self.assertEqual(expect, self.api.calls)
        expect_req_id = ['req-1234']
        self.assertEqual(expect_req_id, fields['return_req_id'])


class DCTest(testtools.TestCase):
    def setUp(self):
        super(DCTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = dcs.DCManager(self.api)

    def test_delete(self):
        dc = self.mgr.get('1')
        dc.delete()
        expect = [
            ('GET', '/v1/dcs/1', {}, None),
            ('GET', '/v1/dcs/1', {}, None),
            ('DELETE', '/v1/dcs/1', {}, None),
        ]
        self.assertEqual(expect, self.api.calls)

    def test_update(self):
        dc = self.mgr.get('1')
        dc.update(name='dc-5')
        expect = [
            ('GET', '/v1/dcs/1', {}, None),
            ('GET', '/v1/dcs/1', {}, None),
            ('PUT', '/v1/dcs/1', {}, [('dc', {'name': 'dc-5'})]),
        ]
        self.assertEqual(expect, self.api.calls)


class FakeArg(object):
    def __init__(self, arg_dict):
        self.arg_dict = arg_dict
        self.fields = arg_dict.keys()

    def __getattr__(self, name):
        if name in self.arg_dict:
            return self.arg_dict[name]
        else:
            return None
