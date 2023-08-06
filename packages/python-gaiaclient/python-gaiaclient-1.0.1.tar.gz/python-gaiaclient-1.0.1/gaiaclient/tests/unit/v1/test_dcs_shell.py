import argparse
import json
import os
import six
import subprocess
import tempfile
import testtools

import mock

from gaiaclient import exc
from gaiaclient import shell

import gaiaclient.v1.client as client
import gaiaclient.v1.dcs
import gaiaclient.v1.dcs_shell as v1shell

from gaiaclient.tests import utils

if six.PY3:
    import io
    file_type = io.IOBase
else:
    file_type = file

fixtures = {
    '/v1/images/96d2c7e1-de4e-4612-8aa2-ba26610c804e': {
        'PUT': (
            {
                'Location': 'http://fakeaddress.com:9292/v1/images/'
                            '96d2c7e1-de4e-4612-8aa2-ba26610c804e',
                'Etag': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                'X-Openstack-Request-Id':
                        'req-b645039d-e1c7-43e5-b27b-2d18a173c42b',
                'Date': 'Mon, 29 Apr 2013 10:24:32 GMT'
            },
            json.dumps({
                'image': {
                    'status': 'active', 'name': 'testimagerename',
                    'deleted': False,
                    'container_format': 'ami',
                    'created_at': '2013-04-25T15:47:43',
                    'disk_format': 'ami',
                    'updated_at': '2013-04-29T10:24:32',
                    'id': '96d2c7e1-de4e-4612-8aa2-ba26610c804e',
                    'min_disk': 0,
                    'protected': False,
                    'min_ram': 0,
                    'checksum': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                    'owner': '1310db0cce8f40b0987a5acbe139765a',
                    'is_public': True,
                    'deleted_at': None,
                    'properties': {
                        'kernel_id': '1b108400-65d8-4762-9ea4-1bf6c7be7568',
                        'ramdisk_id': 'b759bee9-0669-4394-a05c-fa2529b1c114'
                    },
                    'size': 25165824
                }
            })
        ),
        'HEAD': (
            {
                'x-image-meta-id': '96d2c7e1-de4e-4612-8aa2-ba26610c804e',
                'x-image-meta-status': 'active'
            },
            None
        ),
        'GET': (
            {
                'x-image-meta-status': 'active',
                'x-image-meta-owner': '1310db0cce8f40b0987a5acbe139765a',
                'x-image-meta-name': 'cirros-0.3.1-x86_64-uec',
                'x-image-meta-container_format': 'ami',
                'x-image-meta-created_at': '2013-04-25T15:47:43',
                'etag': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                'location': 'http://fakeaddress.com:9292/v1/images/'
                            '96d2c7e1-de4e-4612-8aa2-ba26610c804e',
                'x-image-meta-min_ram': '0',
                'x-image-meta-updated_at': '2013-04-25T15:47:43',
                'x-image-meta-id': '96d2c7e1-de4e-4612-8aa2-ba26610c804e',
                'x-image-meta-property-ramdisk_id':
                        'b759bee9-0669-4394-a05c-fa2529b1c114',
                'date': 'Mon, 29 Apr 2013 09:25:17 GMT',
                'x-image-meta-property-kernel_id':
                        '1b108400-65d8-4762-9ea4-1bf6c7be7568',
                'x-openstack-request-id':
                        'req-842735bf-77e8-44a7-bfd1-7d95c52cec7f',
                'x-image-meta-deleted': 'False',
                'x-image-meta-checksum': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                'x-image-meta-protected': 'False',
                'x-image-meta-min_disk': '0',
                'x-image-meta-size': '25165824',
                'x-image-meta-is_public': 'True',
                'content-type': 'text/html; charset=UTF-8',
                'x-image-meta-disk_format': 'ami',
            },
            None
        )
    },
    '/v1/images/44d2c7e1-de4e-4612-8aa2-ba26610c444f': {
        'PUT': (
            {
                'Location': 'http://fakeaddress.com:9292/v1/images/'
                            '44d2c7e1-de4e-4612-8aa2-ba26610c444f',
                'Etag': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                'X-Openstack-Request-Id':
                        'req-b645039d-e1c7-43e5-b27b-2d18a173c42b',
                'Date': 'Mon, 29 Apr 2013 10:24:32 GMT'
            },
            json.dumps({
                'image': {
                    'status': 'queued', 'name': 'testimagerename',
                    'deleted': False,
                    'container_format': 'ami',
                    'created_at': '2013-04-25T15:47:43',
                    'disk_format': 'ami',
                    'updated_at': '2013-04-29T10:24:32',
                    'id': '44d2c7e1-de4e-4612-8aa2-ba26610c444f',
                    'min_disk': 0,
                    'protected': False,
                    'min_ram': 0,
                    'checksum': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                    'owner': '1310db0cce8f40b0987a5acbe139765a',
                    'is_public': True,
                    'deleted_at': None,
                    'properties': {
                        'kernel_id':
                                '1b108400-65d8-4762-9ea4-1bf6c7be7568',
                        'ramdisk_id':
                                'b759bee9-0669-4394-a05c-fa2529b1c114'
                    },
                    'size': 25165824
                }
            })
        ),
        'HEAD': (
            {
                'x-image-meta-id': '44d2c7e1-de4e-4612-8aa2-ba26610c444f',
                'x-image-meta-status': 'queued'
            },
            None
        ),
        'GET': (
            {
                'x-image-meta-status': 'queued',
                'x-image-meta-owner': '1310db0cce8f40b0987a5acbe139765a',
                'x-image-meta-name': 'cirros-0.3.1-x86_64-uec',
                'x-image-meta-container_format': 'ami',
                'x-image-meta-created_at': '2013-04-25T15:47:43',
                'etag': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                'location': 'http://fakeaddress.com:9292/v1/images/'
                            '44d2c7e1-de4e-4612-8aa2-ba26610c444f',
                'x-image-meta-min_ram': '0',
                'x-image-meta-updated_at': '2013-04-25T15:47:43',
                'x-image-meta-id': '44d2c7e1-de4e-4612-8aa2-ba26610c444f',
                'x-image-meta-property-ramdisk_id':
                        'b759bee9-0669-4394-a05c-fa2529b1c114',
                'date': 'Mon, 29 Apr 2013 09:25:17 GMT',
                'x-image-meta-property-kernel_id':
                        '1b108400-65d8-4762-9ea4-1bf6c7be7568',
                'x-openstack-request-id':
                        'req-842735bf-77e8-44a7-bfd1-7d95c52cec7f',
                'x-image-meta-deleted': 'False',
                'x-image-meta-checksum': 'f8a2eeee2dc65b3d9b6e63678955bd83',
                'x-image-meta-protected': 'False',
                'x-image-meta-min_disk': '0',
                'x-image-meta-size': '25165824',
                'x-image-meta-is_public': 'True',
                'content-type': 'text/html; charset=UTF-8',
                'x-image-meta-disk_format': 'ami',
            },
            None
        )
    },
    '/v1/images/detail?limit=20&name=70aa106f-3750-4d7c-a5ce-0a535ac08d0a': {
        'GET': (
            {},
            {'images': [
                {
                    'id': '70aa106f-3750-4d7c-a5ce-0a535ac08d0a',
                    'name': 'imagedeleted',
                    'deleted': True,
                    'status': 'deleted',
                },
            ]},
        ),
    },
    '/v1/images/70aa106f-3750-4d7c-a5ce-0a535ac08d0a': {
        'HEAD': (
            {
                'x-image-meta-id': '70aa106f-3750-4d7c-a5ce-0a535ac08d0a',
                'x-image-meta-status': 'deleted'
            },
            None
        )
    }
}


class ShellInvalidEndpointandTest(utils.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        """Run before each test."""
        super(ShellInvalidEndpointandTest, self).setUp()
        self.old_environment = os.environ.copy()
        os.environ = {
            'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
            'OS_TENANT_ID': 'tenant_id',
            'OS_TOKEN_ID': 'test',
            'OS_AUTH_URL': 'http://127.0.0.1:5000/v2.0/',
            'OS_AUTH_TOKEN': 'pass',
            'OS_GAIA_API_VERSION': '1',
            'OS_REGION_NAME': 'test',
            'OS_GAIA_URL': 'http://is.invalid'}

        self.shell = shell.ZeusGaiaShell()
        self.patched = mock.patch('gaiaclient.common.utils.get_data_file',
                                  autospec=True, return_value=None)
        self.mock_get_data_file = self.patched.start()

        self.gc = self._mock_gaia_client()

    def _make_args(self, args):
        # NOTE(venkatesh): this conversion from a dict to an object
        # is required because the test_shell.do_xxx(gc, args) methods
        # expects the args to be attributes of an object. If passed as
        # dict directly, it throws an AttributeError.
        class Args(object):
            def __init__(self, entries):
                self.__dict__.update(entries)

        return Args(args)

    def _mock_gaia_client(self):
        my_mocked_gc = mock.Mock()
        my_mocked_gc.get.return_value = {}
        return my_mocked_gc

    def tearDown(self):
        super(ShellInvalidEndpointandTest, self).tearDown()
        os.environ = self.old_environment
        self.patched.stop()

    def run_command(self, cmd):
        self.shell.main(cmd.split())

    def assert_called(self, method, url, body=None, **kwargs):
        return self.shell.cs.assert_called(method, url, body, **kwargs)

    def assert_called_anytime(self, method, url, body=None):
        return self.shell.cs.assert_called_anytime(method, url, body)

    def test_dc_list_invalid_endpoint(self):
        self.assertRaises(
            exc.CommunicationError, self.run_command, 'dc-list')

    def test_dc_create_invalid_endpoint(self):
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'dc-create dc1 --auth-url http://1.1.1.1/v3 --admin-username admin '
                              '--admin-password keystone --admin-tenant admin '
                              '--transport-url rabbit://guest:guest@10.47.235.201:5672/')

    def test_dc_delete_invalid_endpoint(self):
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'dc-delete <fake>')

    def test_dc_show_invalid_endpoint(self):
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'dc-show <DC_ID>')
