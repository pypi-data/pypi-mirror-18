import argparse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import hashlib
import logging
import os
import sys
import traceback
import uuid

import fixtures
from keystoneauth1 import exceptions as ks_exc
from keystoneauth1 import fixture as ks_fixture
import mock
from requests_mock.contrib import fixture as rm_fixture
import six

from gaiaclient.common import utils
from gaiaclient import exc
from gaiaclient import shell as zeus_shell
from gaiaclient.tests import utils as testutils

import json


DEFAULT_GAIA_URL = 'http://127.0.0.1:9292/'
DEFAULT_GAIA_URL_INTERNAL = 'http://127.0.0.1:9191/'
DEFAULT_USERNAME = 'username'
DEFAULT_PASSWORD = 'password'
DEFAULT_TENANT_ID = 'tenant_id'
DEFAULT_TENANT_NAME = 'tenant_name'
DEFAULT_PROJECT_ID = '0123456789'
DEFAULT_USER_DOMAIN_NAME = 'user_domain_name'
DEFAULT_UNVERSIONED_AUTH_URL = 'http://127.0.0.1:5000/'
DEFAULT_V2_AUTH_URL = '%sv2.0' % DEFAULT_UNVERSIONED_AUTH_URL
DEFAULT_V3_AUTH_URL = '%sv3' % DEFAULT_UNVERSIONED_AUTH_URL
DEFAULT_AUTH_TOKEN = ' 3bcc3d3a03f44e3d8377f9247b0ad155'
TEST_SERVICE_URL = 'http://127.0.0.1:5000/'
DEFAULT_SERVICE_TYPE = 'gaia'
DEFAULT_ENDPOINT_TYPE = 'public'

FAKE_V2_ENV = {'OS_USERNAME': DEFAULT_USERNAME,
               'OS_PASSWORD': DEFAULT_PASSWORD,
               'OS_TENANT_NAME': DEFAULT_TENANT_NAME,
               'OS_AUTH_URL': DEFAULT_V2_AUTH_URL,
               'OS_GAIA_URL': DEFAULT_GAIA_URL}

FAKE_V3_ENV = {'OS_USERNAME': DEFAULT_USERNAME,
               'OS_PASSWORD': DEFAULT_PASSWORD,
               'OS_PROJECT_ID': DEFAULT_PROJECT_ID,
               'OS_USER_DOMAIN_NAME': DEFAULT_USER_DOMAIN_NAME,
               'OS_AUTH_URL': DEFAULT_V3_AUTH_URL,
               'OS_GAIA_URL': DEFAULT_GAIA_URL}

FAKE_V4_ENV = {'OS_USERNAME': DEFAULT_USERNAME,
               'OS_PASSWORD': DEFAULT_PASSWORD,
               'OS_PROJECT_ID': DEFAULT_PROJECT_ID,
               'OS_USER_DOMAIN_NAME': DEFAULT_USER_DOMAIN_NAME,
               'OS_AUTH_URL': DEFAULT_V3_AUTH_URL,
               'OS_SERVICE_TYPE': DEFAULT_SERVICE_TYPE,
               'OS_ENDPOINT_TYPE': DEFAULT_ENDPOINT_TYPE,
               'OS_AUTH_TOKEN': DEFAULT_AUTH_TOKEN}

TOKEN_ID = uuid.uuid4().hex

V2_TOKEN = ks_fixture.V2Token(token_id=TOKEN_ID)
V2_TOKEN.set_scope()
_s = V2_TOKEN.add_service('gaia', name='gaia')
_s.add_endpoint(DEFAULT_GAIA_URL)

V3_TOKEN = ks_fixture.V3Token()
V3_TOKEN.set_project_scope()
_s = V3_TOKEN.add_service('gaia', name='gaia')
_s.add_standard_endpoints(public=DEFAULT_GAIA_URL,
                          internal=DEFAULT_GAIA_URL_INTERNAL)


class ShellTest(testutils.TestCase):
    # auth environment to use
    auth_env = FAKE_V2_ENV.copy()
    # expected auth plugin to invoke
    token_url = DEFAULT_V2_AUTH_URL + '/tokens'

    # Patch os.environ to avoid required auth info
    def make_env(self, exclude=None):
        env = dict((k, v) for k, v in self.auth_env.items() if k != exclude)
        self.useFixture(fixtures.MonkeyPatch('os.environ', env))

    def setUp(self):
        super(ShellTest, self).setUp()
        global _old_env
        _old_env, os.environ = os.environ, self.auth_env

        self.requests = self.useFixture(rm_fixture.Fixture())

        json_list = ks_fixture.DiscoveryList(DEFAULT_UNVERSIONED_AUTH_URL)
        self.requests.get(DEFAULT_UNVERSIONED_AUTH_URL,
                          json=json_list,
                          status_code=300)

        json_v2 = {'version': ks_fixture.V2Discovery(DEFAULT_V2_AUTH_URL)}
        self.requests.get(DEFAULT_V2_AUTH_URL, json=json_v2)

        json_v3 = {'version': ks_fixture.V3Discovery(DEFAULT_V3_AUTH_URL)}
        self.requests.get(DEFAULT_V3_AUTH_URL, json=json_v3)

        self.v2_auth = self.requests.post(DEFAULT_V2_AUTH_URL + '/tokens',
                                          json=V2_TOKEN)

        headers = {'X-Subject-Token': TOKEN_ID}
        self.v3_auth = self.requests.post(DEFAULT_V3_AUTH_URL + '/auth/tokens',
                                          headers=headers,
                                          json=V3_TOKEN)

        global shell, _shell, assert_called, assert_called_anytime
        _shell = zeus_shell.ZeusGaiaShell()
        shell = lambda cmd: _shell.main(cmd.split())

    def tearDown(self):
        super(ShellTest, self).tearDown()
        global _old_env
        os.environ = _old_env

    def shell(self, argstr, exitcodes=(0,)):
        orig = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdout = six.StringIO()
            sys.stderr = six.StringIO()
            _shell = zeus_shell.ZeusGaiaShell()
            _shell.main(argstr.split())
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertIn(exc_value.code, exitcodes)
        finally:
            stdout = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig
            stderr = sys.stderr.getvalue()
            sys.stderr.close()
            sys.stderr = orig_stderr
        return (stdout, stderr)

    def test_help_unknown_command(self):
        shell = zeus_shell.ZeusGaiaShell()
        argstr = 'help foofoo'
        self.assertRaises(exc.CommandError, shell.main, argstr.split())

    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    @mock.patch('sys.argv', ['gaia', 'help', 'foofoo'])
    def test_no_stacktrace_when_debug_disabled(self):
        with mock.patch.object(traceback, 'print_exc') as mock_print_exc:
            try:
                zeus_shell.main()
            except SystemExit:
                pass
            self.assertFalse(mock_print_exc.called)

    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    @mock.patch('sys.argv', ['gaia', 'help', 'foofoo'])
    def test_stacktrace_when_debug_enabled_by_env(self):
        old_environment = os.environ.copy()
        os.environ = {'GAIACLIENT_DEBUG': '1'}
        try:
            with mock.patch.object(traceback, 'print_exc') as mock_print_exc:
                try:
                    zeus_shell.main()
                except SystemExit:
                    pass
                self.assertTrue(mock_print_exc.called)
        finally:
            os.environ = old_environment

    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    @mock.patch('sys.argv', ['gaia', '--debug', 'help', 'foofoo'])
    def test_stacktrace_when_debug_enabled(self):
        with mock.patch.object(traceback, 'print_exc') as mock_print_exc:
            try:
                zeus_shell.main()
            except SystemExit:
                pass
            self.assertTrue(mock_print_exc.called)

    def test_help(self):
        shell = zeus_shell.ZeusGaiaShell()
        argstr = 'help'
        with mock.patch.object(shell, '_get_keystone_auth_plugin') as et_mock:
            actual = shell.main(argstr.split())
            self.assertEqual(0, actual)
            self.assertFalse(et_mock.called)

    def test_blank_call(self):
        shell = zeus_shell.ZeusGaiaShell()
        with mock.patch.object(shell, '_get_keystone_auth_plugin') as et_mock:
            actual = shell.main('')
            self.assertEqual(0, actual)
            self.assertFalse(et_mock.called)

    def test_help_on_subcommand_error(self):
        self.assertRaises(exc.CommandError, shell,
                          'help bad')

    def test_get_base_parser(self):
        test_shell = zeus_shell.ZeusGaiaShell()
        # NOTE(stevemar): Use the current sys.argv for base_parser since it
        # doesn't matter for this test, it just needs to initialize the CLI
        actual_parser = test_shell.get_base_parser(sys.argv)
        description = 'Command-line interface to the Zeus Gaia API.'
        expected = argparse.ArgumentParser(
            prog='gaia', usage=None,
            description=description,
            conflict_handler='error',
            add_help=False,
            formatter_class=zeus_shell.HelpFormatter,)
        # NOTE(guochbo): Can't compare ArgumentParser instances directly
        # Convert ArgumentPaser to string first.
        self.assertEqual(str(expected), str(actual_parser))

    @mock.patch.object(zeus_shell.ZeusGaiaShell,
                       '_get_versioned_client')
    def test_cert_and_key_args(self,  mock_versioned_client):
        # make sure --os-cert and --os-key are passed correctly
        args = ('--os-cert mycert '
                '--os-key mykey dc-list')
        shell(args)
        assert mock_versioned_client.called
        ((api_version, args), kwargs) = mock_versioned_client.call_args
        self.assertEqual('mycert', args.os_cert)
        self.assertEqual('mykey', args.os_key)

    @mock.patch('gaiaclient.v1.client.Client')
    def test_no_auth_with_token_and_gaia_url(self, v1_client):
        # test no authentication is required if both token and endpoint url
        # are specified
        args = ('--os-auth-token mytoken'
                ' --os-gaia-url https://gaia:1234/v1 dc-list')
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        assert v1_client.called
        (args, kwargs) = v1_client.call_args
        self.assertEqual('mytoken', kwargs['token'])
        self.assertEqual('https://gaia:1234', args[0])

    def _assert_auth_plugin_args(self):
        # make sure our auth plugin is invoked with the correct args
        self.assertFalse(self.v3_auth.called)

        body = json.loads(self.v2_auth.last_request.body)

        self.assertEqual(self.auth_env['OS_TENANT_NAME'],
                         body['auth']['tenantName'])
        self.assertEqual(self.auth_env['OS_USERNAME'],
                         body['auth']['passwordCredentials']['username'])
        self.assertEqual(self.auth_env['OS_PASSWORD'],
                         body['auth']['passwordCredentials']['password'])

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation(self, v1_client):
        args = 'dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        self.assertEqual(0, self.v2_auth.call_count)

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation_with_unversioned_auth_url(
            self, v1_client):
        args = ('--os-auth-url %s dc-list' %
                DEFAULT_UNVERSIONED_AUTH_URL)
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())

    @mock.patch('gaiaclient.Client')
    def test_endpoint_token_no_auth_req(self, mock_client):

        def verify_input(version=None, endpoint=None, *args, **kwargs):
            self.assertIn('token', kwargs)
            self.assertEqual(TOKEN_ID, kwargs['token'])
            self.assertEqual(DEFAULT_GAIA_URL, endpoint)
            return mock.MagicMock()

        mock_client.side_effect = verify_input
        gaia_shell = zeus_shell.ZeusGaiaShell()
        args = ['--os-gaia-api-version', '1',
                '--os-auth-token', TOKEN_ID,
                '--os-gaia-url', DEFAULT_GAIA_URL,
                'dc-list']

        gaia_shell.main(args)
        self.assertEqual(1, mock_client.call_count)

    @mock.patch('sys.stdin', side_effect=mock.MagicMock)
    @mock.patch('getpass.getpass', side_effect=EOFError)
    @mock.patch('gaiaclient.v1.client.Client')
    def test_password_prompted_ctrlD(self, v1_client,
                                             mock_getpass, mock_stdin):
        cli1 = mock.MagicMock()
        v1_client.return_value = cli1
        cli1.http_client.get.return_value = (None, {'versions': []})

        gaia_shell = zeus_shell.ZeusGaiaShell()
        self.make_env(exclude='OS_PASSWORD')
        # We should get Command Error because we mock Ctl-D.
        self.assertRaises(exc.CommandError, gaia_shell.main, ['dc-list'])
        # Make sure we are actually prompted.
        mock_getpass.assert_called_with('OS Password: ')

    @mock.patch(
        'gaiaclient.shell.ZeusGaiaShell._get_keystone_auth_plugin')
    def test_no_auth_with_proj_name(self, session):
        with mock.patch('gaiaclient.v1.client.Client'):
            args = ('--os-project-name myname '
                    '--os-project-domain-name mydomain '
                    '--os-project-domain-id myid '
                    'dc-list')
            gaia_shell = zeus_shell.ZeusGaiaShell()
            gaia_shell.main(args.split())
            ((args), kwargs) = session.call_args
            self.assertEqual('myname', kwargs['project_name'])
            self.assertEqual('mydomain', kwargs['project_domain_name'])
            self.assertEqual('myid', kwargs['project_domain_id'])

    @mock.patch.object(zeus_shell.ZeusGaiaShell, 'main')
    def test_shell_keyboard_interrupt(self, mock_gaia_shell):
        # Ensure that exit code is 130 for KeyboardInterrupt
        try:
            mock_gaia_shell.side_effect = KeyboardInterrupt()
            zeus_shell.main()
        except SystemExit as ex:
            self.assertEqual(130, ex.code)

    @mock.patch('gaiaclient.common.utils.exit', side_effect=utils.exit)
    def test_shell_illegal_version(self, mock_exit):
        # Only int versions are allowed on cli
        shell = zeus_shell.ZeusGaiaShell()
        argstr = '--os-gaia-api-version 1.1 dc-list'
        try:
            shell.main(argstr.split())
        except SystemExit as ex:
            self.assertEqual(1, ex.code)
        msg = ("Invalid API version parameter. "
               "Supported values are %s" % zeus_shell.SUPPORTED_VERSIONS)
        mock_exit.assert_called_with(msg=msg)

    @mock.patch('gaiaclient.common.utils.exit', side_effect=utils.exit)
    def test_shell_unsupported_version(self, mock_exit):
        # Test an integer version which is not supported (-1)
        shell = zeus_shell.ZeusGaiaShell()
        argstr = '--os-gaia-api-version -1 dc-list'
        try:
            shell.main(argstr.split())
        except SystemExit as ex:
            self.assertEqual(1, ex.code)
        msg = ("Invalid API version parameter. "
               "Supported values are %s" % zeus_shell.SUPPORTED_VERSIONS)
        mock_exit.assert_called_with(msg=msg)

    @mock.patch.object(zeus_shell.ZeusGaiaShell,
                       'get_subcommand_parser')
    def test_shell_import_error_with_mesage(self, mock_parser):
        msg = 'Unable to import module xxx'
        mock_parser.side_effect = ImportError('%s' % msg)
        shell = zeus_shell.ZeusGaiaShell()
        argstr = 'dc-list'
        try:
            shell.main(argstr.split())
            self.fail('No import error returned')
        except ImportError as e:
            self.assertEqual(msg, str(e))

    @mock.patch.object(zeus_shell.ZeusGaiaShell,
                       'get_subcommand_parser')
    def test_shell_import_error_default_message(self, mock_parser):
        mock_parser.side_effect = ImportError
        shell = zeus_shell.ZeusGaiaShell()
        argstr = 'dc-list'
        try:
            shell.main(argstr.split())
            self.fail('No import error returned')
        except ImportError as e:
            msg = 'Unable to import module. Re-run with --debug for more info.'
            self.assertEqual(msg, str(e))

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation_without_username(self, v1_client):
        self.make_env(exclude='OS_USERNAME')
        args = 'dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        self.assertRaises(exc.CommandError, gaia_shell.main, args.split())

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation_without_auth_url(self, v1_client):
        self.make_env(exclude='OS_AUTH_URL')
        args = 'dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        self.assertRaises(exc.CommandError, gaia_shell.main, args.split())

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation_without_tenant(self, v1_client):
        if 'OS_TENANT_NAME' in os.environ:
            self.make_env(exclude='OS_TENANT_NAME')
        if 'OS_PROJECT_ID' in os.environ:
            self.make_env(exclude='OS_PROJECT_ID')
        args = 'dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        self.assertRaises(exc.CommandError, gaia_shell.main, args.split())

    @mock.patch('sys.argv', ['gaia'])
    @mock.patch('sys.stdout', six.StringIO())
    @mock.patch('sys.stderr', six.StringIO())
    def test_main_noargs(self):
        # Ensure that main works with no command-line arguments
        try:
            zeus_shell.main()
        except SystemExit:
            self.fail('Unexpected SystemExit')

        # We expect the normal v1 usage as a result
        expected = ['Command-line interface to the Zeus Gaia API',
                    'dc-list']
        for output in expected:
            self.assertIn(output,
                          sys.stdout.getvalue())

    @mock.patch('gaiaclient.v1.client.Client')
    @mock.patch('gaiaclient.shell.logging.basicConfig')
    def test_setup_debug(self, conf, v1_client):
        cli1 = mock.MagicMock()
        v1_client.return_value = cli1
        cli1.http_client.get.return_value = (None, {'versions': []})
        args = '--debug dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        gaia_logger = logging.getLogger('gaiaclient')
        self.assertEqual(gaia_logger.getEffectiveLevel(), logging.DEBUG)
        conf.assert_called_with(level=logging.DEBUG)


class ShellTestWithKeystoneV3Auth(ShellTest):
    # auth environment to use
    auth_env = FAKE_V3_ENV.copy()
    token_url = DEFAULT_V3_AUTH_URL + '/auth/tokens'

    def _assert_auth_plugin_args(self):
        self.assertFalse(self.v2_auth.called)

        body = json.loads(self.v3_auth.last_request.body)
        user = body['auth']['identity']['password']['user']

        self.assertEqual(self.auth_env['OS_USERNAME'], user['name'])
        self.assertEqual(self.auth_env['OS_PASSWORD'], user['password'])
        self.assertEqual(self.auth_env['OS_USER_DOMAIN_NAME'],
                         user['domain']['name'])
        self.assertEqual(self.auth_env['OS_PROJECT_ID'],
                         body['auth']['scope']['project']['id'])

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation(self, v1_client):
        args = 'dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        self.assertEqual(0, self.v3_auth.call_count)

    @mock.patch('keystoneauth1.discover.Discover',
                side_effect=ks_exc.ClientException())
    def test_api_discovery_failed_with_unversioned_auth_url(self,
                                                            discover):
        args = ('--os-auth-url %s dc-list'
                % DEFAULT_UNVERSIONED_AUTH_URL)
        gaia_shell = zeus_shell.ZeusGaiaShell()
        self.assertRaises(exc.CommandError, gaia_shell.main, args.split())

    def test_bash_completion(self):
        stdout, stderr = self.shell('bash_completion')
        # just check we have some output
        required = [
            '--description',
            'dc-create',
            'help',
            '--auth-url']
        for r in required:
            self.assertIn(r, stdout.split())
        avoided = [
            'bash_completion',
            'bash-completion']
        for r in avoided:
            self.assertNotIn(r, stdout.split())


class ShellTestWithNoZSGaiaURLPublic(ShellTestWithKeystoneV3Auth):
    # auth environment to use
    # default uses public
    auth_env = FAKE_V4_ENV.copy()

    def setUp(self):
        super(ShellTestWithNoZSGaiaURLPublic, self).setUp()
        self.gaia_url = DEFAULT_GAIA_URL
        self.requests.get(DEFAULT_GAIA_URL + 'v1/dcs/',
                          text='{"dcs": []}')

    @mock.patch('gaiaclient.v1.client.Client')
    def test_auth_plugin_invocation(self, v1_client):
        args = 'dc-list'
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        self.assertEqual(1, self.v3_auth.call_count)
        self._assert_auth_plugin_args()

    @mock.patch('gaiaclient.v1.client.Client')
    def test_endpoint_from_interface(self, v1_client):
        args = ('dc-list')
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        assert v1_client.called
        (args, kwargs) = v1_client.call_args
        self.assertEqual(self.gaia_url, kwargs['endpoint_override'])

    def test_endpoint_real_from_interface(self):
        args = ('dc-list')
        gaia_shell = zeus_shell.ZeusGaiaShell()
        gaia_shell.main(args.split())
        self.assertIn(self.gaia_url + "v1/dcs/",
                      self.requests.request_history[2].url)


class ShellTestWithNoZSGaiaURLInternal(ShellTestWithNoZSGaiaURLPublic):
    # auth environment to use
    # this uses internal
    FAKE_V5_ENV = FAKE_V4_ENV.copy()
    FAKE_V5_ENV['OS_ENDPOINT_TYPE'] = 'internal'
    auth_env = FAKE_V5_ENV.copy()

    def setUp(self):
        super(ShellTestWithNoZSGaiaURLPublic, self).setUp()
        self.gaia_url = DEFAULT_GAIA_URL_INTERNAL
        self.requests.get(DEFAULT_GAIA_URL_INTERNAL + 'v1/dcs/',
                          text='{"dcs": []}')


