from django.test import TestCase, RequestFactory
from .views import ConfigView

# Create your tests here.

class ConfigViewTest(TestCase):
    def test_get_context_data(self):
        request = RequestFactory().get('/')
        view = ConfigView()
        view.setup()
        view.get_context_data()
