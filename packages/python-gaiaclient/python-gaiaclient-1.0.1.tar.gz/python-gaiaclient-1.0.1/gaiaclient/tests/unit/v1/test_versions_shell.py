import json
import testtools
import os
from gaiaclient.tests import utils
from gaiaclient import shell
from gaiaclient.common import http

import mock

from gaiaclient.tests.unit.fixture_data import fixtures


class VersionShellTest(utils.TestCase):

    def setUp(self):
        super(VersionShellTest, self).setUp()
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

    def test_shell_list_version(self):
        self.run_command('version-list')
        self.assert_called('GET', '/')

