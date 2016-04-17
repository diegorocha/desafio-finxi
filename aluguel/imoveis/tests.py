from django.test import TestCase

class HomeViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')
        
    def test_get(self):
        self.assertTrue(200, self.resp.status_code)
