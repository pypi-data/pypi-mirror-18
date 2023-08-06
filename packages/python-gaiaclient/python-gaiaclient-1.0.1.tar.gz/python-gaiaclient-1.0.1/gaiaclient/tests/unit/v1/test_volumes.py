import json
import testtools

from gaiaclient.tests import utils
from gaiaclient.v1 import volumes
from gaiaclient.tests.unit.fixture_data import fixtures


class VolumesTest(utils.TestCase):

    def setUp(self):
        super(VolumesTest, self).setUp()
        self.prepare_fixtures(fixtures)
        self.mgr = volumes.VolumeManager(self.api)
        self.mgr.dc = '1234'

    def test_list_volumes_with_sort_dir(self):
        list(self.mgr.list(sort_dir='asc'))
        self.assert_called('GET', '/v1/volumes/?sort_dir=asc')

    def test_create_volume(self):
        volume = self.mgr.create(
            name="My server",
            size=1024,
            volume_type='ceph'
        )

        self.assert_request_id(volume, ['req-1234'])
        self.assert_called('POST', '/v1/volumes/')
        self.assertIsInstance(volume, volumes.Volume)

    def test_delete_volume(self):
        self.mgr.delete('1')
        self.assert_called('DELETE', '/v1/volumes/1')

    def test_update_volume(self):
        volume = self.mgr.get('1')
        volume.update(name='volume2')
        self.assert_called('PUT', '/v1/volumes/1')
        self.assertIsInstance(volume, volumes.Volume)

    def test_create_server_volume(self):
        volume = self.mgr.create_server_volume('1', '1')
        self.assert_called('POST', '/v1/servers/1/volumes')
        self.assertIsInstance(volume, volumes.Volume)

    def test_delete_server_volume(self):
        self.mgr.delete_server_volume('1', '1')
        self.assert_called('DELETE', '/v1/servers/1/volumes/1')

    def test_get_server_volumes(self):
        volume = self.mgr.get_server_volumes('1')
        self.assert_called('GET', '/v1/servers/1/volumes')
        self.assertIsInstance(volume[0], volumes.Volume)




