import json
import testtools
import os
from gaiaclient.tests import utils
from gaiaclient import shell
from gaiaclient.common import http

import mock

from gaiaclient.tests.unit.fixture_data import fixtures


class ServerShellTest(utils.TestCase):

    def setUp(self):
        super(ServerShellTest, self).setUp()
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

    def test_shell_list_server(self):
        self.run_command('server-list --sort name')
        self.assert_called('GET', '/v1/servers/?sort_dir=desc&sort_key=name')

    def test_shell_create_server(self):
        self.run_command('server-create --flavor f1 --image i1 --network n1 --ip 1.1.1.1 server1')

        self.assert_called_anytime('POST', '/v1/servers/')

    def test_shell_delete_server(self):
        self.run_command('server-delete 1')
        self.assert_called_anytime('DELETE', '/v1/servers/1')

    def test_shell_update_server(self):
        self.run_command('server-update 1 --name s1')
        self.assert_called_anytime('PUT', '/v1/servers/1')

    def test_shell_start_server(self):
        self.run_command('server-start 1')
        self.assert_called_anytime('POST', '/v1/servers/1/start')

    def test_shell_stop_server(self):
        self.run_command('server-stop 1')
        self.assert_called_anytime('POST', '/v1/servers/1/stop')

    def test_shell_reboot_server(self):
        self.run_command('server-reboot 1')
        self.assert_called_anytime('POST', '/v1/servers/1/reboot?type=SOFT')

    def test_shell_get_vnc_console(self):
        self.run_command('server-get-vnc-console 1')
        self.assert_called_anytime('POST', '/v1/servers/1/console?type=NOVNC')

    def test_shell_interface_list(self):
        self.run_command('interface-list 1')
        self.assert_called_anytime('GET', '/v1/servers/1/interfaces')

    def test_shell_interface_attach(self):
        self.run_command('interface-attach 1')
        self.assert_called_anytime('POST', '/v1/servers/1/interfaces')

    def test_shell_interface_detach(self):
        self.run_command('interface-detach 1 1')
        self.assert_called_anytime('DELETE', '/v1/servers/1/interfaces/1')

