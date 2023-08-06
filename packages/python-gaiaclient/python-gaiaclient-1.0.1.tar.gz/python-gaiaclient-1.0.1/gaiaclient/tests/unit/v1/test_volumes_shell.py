import json
import testtools
import os
from gaiaclient.tests import utils
from gaiaclient import shell
from gaiaclient.common import http

import mock

from gaiaclient.tests.unit.fixture_data import fixtures


class VolumeShellTest(utils.TestCase):

    def setUp(self):
        super(VolumeShellTest, self).setUp()
        self.prepare_fixtures(fixtures)
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
            'OS_GAIA_URL': 'http://127.0.0.1:6666',
            'DC_NAME': 'dc1'
        }

        self.shell = shell.ZeusGaiaShell()

        http.get_http_client = self.fake_http_client

    def fake_http_client(self, endpoint=None, **kwargs):
        return self.api

    def run_command(self, cmd):
        self.shell.main(cmd.split())

    def test_shell_list_volume(self):
        self.run_command('volume-list --sort_key name')
        self.assert_called('GET', '/v1/volumes/?sort_key=name')

    def test_shell_create_volume(self):
        self.run_command('volume-create 100 --name volume1 --volume-type ceph')
        self.assert_called_anytime('POST', '/v1/volumes/')

    def test_shell_delete_volume(self):
        self.run_command('volume-delete 1')
        self.assert_called('DELETE', '/v1/volumes/1')

    def test_shell_update_volume(self):
        self.run_command('volume-update 1 --name volume2')
        self.assert_called('PUT', '/v1/volumes/1')

    def test_shell_volume_attach(self):
        self.run_command('volume-attach 1 1')
        self.assert_called_anytime('POST', '/v1/servers/1/volumes')

    def test_shell_volume_detach(self):
        self.run_command('volume-detach 1 1')
        self.assert_called_anytime('DELETE', '/v1/servers/1/volumes/1')

    def test_shell_server_volumes(self):
        self.run_command('server-volumes 1')
        self.assert_called_anytime('GET', '/v1/servers/1/volumes')

