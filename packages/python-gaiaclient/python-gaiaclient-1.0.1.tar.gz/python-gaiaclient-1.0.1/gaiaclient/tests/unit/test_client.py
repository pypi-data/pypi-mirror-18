import testtools

from gaiaclient import client
from gaiaclient import v1


class ClientTest(testtools.TestCase):

    def test_no_endpoint_error(self):
        self.assertRaises(ValueError, client.Client, None)

    def test_endpoint(self):
        gc = client.Client(1, "http://example.com")
        self.assertEqual("http://example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)

    def test_versioned_endpoint(self):
        gc = client.Client(1, "http://example.com/v1")
        self.assertEqual("http://example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)

    def test_versioned_endpoint_no_version(self):
        gc = client.Client(endpoint="http://example.com/v1")
        self.assertEqual("http://example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)

    def test_versioned_endpoint_with_minor_revision(self):
        gc = client.Client(1.1, "http://example.com/v1.2")
        self.assertEqual("http://example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)

    def test_endpoint_with_version_hostname(self):
        gc = client.Client(1, "http://v1.example.com")
        self.assertEqual("http://v1.example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)

    def test_versioned_endpoint_with_version_hostname(self):
        gc = client.Client(endpoint="http://v2.example.com/v1")
        self.assertEqual("http://v2.example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)

    def test_versioned_endpoint_with_minor_revision_and_version_hostname(self):
        gc = client.Client(endpoint="http://v1.example.com/v1.1")
        self.assertEqual("http://v1.example.com", gc.http_client.endpoint)
        self.assertIsInstance(gc, v1.client.Client)
