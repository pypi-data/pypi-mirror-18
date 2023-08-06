import json
import testtools

from gaiaclient.tests import utils
from gaiaclient.v1 import flavors
from gaiaclient.tests.unit.fixture_data import fixtures


class FlavorsTest(utils.TestCase):

    def setUp(self):
        super(FlavorsTest, self).setUp()
        self.prepare_fixtures(fixtures)
        self.mgr = flavors.FlavorManager(self.api)
        self.mgr.dc = '1234'

    def test_list_flavor(self):
        list(self.mgr.list())
        self.assert_called('GET', '/v1/flavors/')

    def test_create_flavor(self):
        self.mgr.create(name='1', ram=1024, vcpus=2, disk=20)
        self.assert_called('POST', '/v1/flavors/')


