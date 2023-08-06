import json
import testtools

from gaiaclient.tests import utils
from gaiaclient.v1 import networks
from gaiaclient.tests.unit.fixture_data import fixtures


class NetworksTest(utils.TestCase):

    def setUp(self):
        super(NetworksTest, self).setUp()
        self.prepare_fixtures(fixtures)
        self.mgr = networks.NetworkManager(self.api)
        self.submgr = networks.SubnetManager(self.api)
        self.mgr.dc = '1234'
        self.submgr.dc = '1234'

    def test_list_network_with_sort_dir(self):
        list(self.mgr.list(sort_dir='asc'))
        self.assert_called('GET', '/v1/networks/?sort_dir=asc')

    def test_list_subnets(self):
        list(self.submgr.list())
        self.assert_called('GET', '/v1/subnets/')



