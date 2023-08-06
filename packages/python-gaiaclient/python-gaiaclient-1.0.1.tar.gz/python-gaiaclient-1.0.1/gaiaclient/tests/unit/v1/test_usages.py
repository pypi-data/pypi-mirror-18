from gaiaclient.tests import utils
from gaiaclient.v1 import usages
from gaiaclient.tests.unit.fixture_data import fixtures


class UsagesTest(utils.TestCase):

    def setUp(self):
        super(UsagesTest, self).setUp()
        self.prepare_fixtures(fixtures)
        self.mgr = usages.UsageManager(self.api)
        self.mgr.dc = '1234'

    def test_list_usages(self):
        list(self.mgr.list())
        self.assert_called('GET', '/v1/usages/')
