import json
import testtools

from gaiaclient.tests import utils
from gaiaclient.v1 import servers
from gaiaclient.tests.unit.fixture_data import fixtures


class ServersTest(utils.TestCase):

    def setUp(self):
        super(ServersTest, self).setUp()
        self.prepare_fixtures(fixtures)
        self.mgr = servers.ServerManager(self.api)
        self.mgr.dc = '1234'

    def test_list_with_sort_dir(self):
        list(self.mgr.list(sort_dirs=['asc']))
        url = '/v1/servers/?sort_dir=asc'
        expect = [('GET', url, {'X-Dc-Id': '1234'}, None)]
        self.assertEqual(expect, self.api.calls)

    def test_create_server(self):

        self.mgr.create(
            name="My server",
            image=1,
            flavor=1,
            networks=[
                {
                    'id': '1234',
                    'ip': '1.1.1.1'
                }
            ]
        )

        self.assert_called('POST', '/v1/servers/')
        # self.assertIsInstance(server, servers.Server)

    def test_start_server(self):
        s = self.mgr.get(1)
        s.start()
        self.assert_called('POST', '/v1/servers/1/start')
        self.mgr.start(s)
        self.assert_called('POST', '/v1/servers/1/start')

    def test_stop_server(self):
        s = self.mgr.get(1)
        s.stop()
        self.assert_called('POST', '/v1/servers/1/stop')
        self.mgr.stop(s)
        self.assert_called('POST', '/v1/servers/1/stop')

    def test_reboot_server(self):
        s = self.mgr.get(1)
        s.reboot()
        self.assert_called('POST', '/v1/servers/1/reboot?type=SOFT')
        self.mgr.reboot(s, reboot_type='HARD')
        self.assert_called('POST', '/v1/servers/1/reboot?type=HARD')

    def test_delete_server(self):
        dc = self.mgr.get('1')
        dc.delete()
        expect = [
            ('GET', '/v1/servers/1', {'X-Dc-Id': '1234'}, None),
            ('DELETE', '/v1/servers/1', {'X-Dc-Id': '1234'}, None),
        ]
        self.assertEqual(expect, self.api.calls)

    def test_update_server(self):
        dc = self.mgr.get('1')
        dc.update(name='server5')
        expect = [
            ('GET', '/v1/servers/1', {'X-Dc-Id': '1234'}, None),
            ('PUT', '/v1/servers/1', {'X-Dc-Id': '1234'}, [('server', {'name': 'server5'})]),
        ]
        self.assertEqual(expect, self.api.calls)

    def test_get_vnc_console(self):
        s = self.mgr.get(1)
        vnc = s.get_vnc_console('NOVNC')
        self.assert_called('POST', '/v1/servers/1/console?type=NOVNC')

    def test_server_list_interfaces(self):
        s = self.mgr.get(1)
        s.interface_list()
        self.assert_called('GET', '/v1/servers/1/interfaces')

    def test_server_attach_interface(self):
        s = self.mgr.get(1)
        s.interface_attach(None, '1', '1.1.1.1')
        self.assert_called('POST', '/v1/servers/1/interfaces')

    def test_server_detach_interface(self):
        s = self.mgr.get(1)
        s.interface_detach('1')
        self.assert_called('DELETE', '/v1/servers/1/interfaces/1')


