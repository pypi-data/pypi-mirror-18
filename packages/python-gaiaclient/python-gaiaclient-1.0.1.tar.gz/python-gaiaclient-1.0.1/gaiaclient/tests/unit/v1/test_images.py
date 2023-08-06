import json
import testtools

from gaiaclient.tests import utils
from gaiaclient.v1 import images


fixtures = {
    '/v1/images': {
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
    '/v1/images/?sort_dir=asc': {
        'GET': (
            {'X-Dc-Id': '1234'},
            {'images': [
                {
                    'id': '1',
                    'name': 'image1',
                },
                {
                    'id': '2',
                    'name': 'image2',
                },
            ]},
        ),
    },
    '/v1/images/1': {
        'GET': (
            {},
            {
                'image': {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'status': 'Active',
                    'created_at' : '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
        'PUT': (
            {},
            {
                'image': {
                    'id': '1',
                    'name': 'dc-1',
                    'description': 'desc',
                    'status': 'Active',
                    'created_at' : '2016-06-20T10:45:59.000000',
                    'updated_at': '2016-06-20T10:45:59.000000'
                }
            }
        ),
        'DELETE': ({}, None),
    },
}


class ImageManagerTest(testtools.TestCase):

    def setUp(self):
        super(ImageManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = images.ImageManager(self.api)
        self.mgr.dc = '1234'

    def test_list_with_sort_dir(self):
        list(self.mgr.list(sort_dir='asc'))
        url = '/v1/images/?sort_dir=asc'
        expect = [('GET', url, {'X-Dc-Id': '1234'}, None)]
        self.assertEqual(expect, self.api.calls)


class ImageTest(testtools.TestCase):
    def setUp(self):
        super(ImageTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = images.ImageManager(self.api)
        self.mgr.dc = '1234'

    def test_delete(self):
        dc = self.mgr.get('1')
        dc.delete()
        expect = [
            ('GET', '/v1/images/1', {'X-Dc-Id': '1234'}, None),
            ('DELETE', '/v1/images/1', {'X-Dc-Id': '1234'}, None),
        ]
        self.assertEqual(expect, self.api.calls)

    # def test_update(self):
    #     dc = self.mgr.get('1')
    #     dc.update(name='image1')
    #     expect = [
    #         ('GET', '/v1/images/1', {'X-Dc-Id': '1234'}, None),
    #         ('PUT', '/v1/images/1', {'X-Dc-Id': '1234'}, [('image', {'name': 'image1'})]),
    #     ]
    #     self.assertEqual(expect, self.api.calls)
