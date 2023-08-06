import testtools

from gaiaclient.tests import utils
import gaiaclient.v1.versions


fixtures = {
    '/': {
        'GET': (
            {},
            {"versions": [
                {
                    "status": "EXPERIMENTAL",
                    "id": "v3.0",
                    "links": [
                        {
                            "href": "http://10.229.45.145:9292/v3/",
                            "rel": "self"
                        }
                    ]
                },
                {
                    "status": "CURRENT",
                    "id": "v2.3",
                    "links": [
                        {
                            "href": "http://10.229.45.145:9292/v2/",
                            "rel": "self"
                        }
                    ]
                },
                {
                    "status": "SUPPORTED",
                    "id": "v1.0",
                    "links": [
                        {
                            "href": "http://10.229.45.145:9292/v1/",
                            "rel": "self"
                        }
                    ]
                }
            ]}
        )
    }
}


class TestVersions(testtools.TestCase):

    def setUp(self):
        super(TestVersions, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = gaiaclient.v1.versions.VersionManager(self.api)

    def test_version_list(self):
        versions = self.mgr.list()
        expect = [('GET', '/', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(versions))
        self.assertEqual('v3.0', versions[0].id)
        self.assertEqual('EXPERIMENTAL', versions[0].status)
        self.assertEqual([{"href": "http://10.229.45.145:9292/v3/",
                           "rel": "self"}], versions[0].links)
