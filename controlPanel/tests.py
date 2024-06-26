from django.db import connections
from django.test import TestCase, RequestFactory
from controlPanel.models import Timer, Server
from controlPanel.views import ConfigView, AddServerView, DeleteServerView

# class MyTestCase(TestCase):
#     def test_access_test_database(self):
#         test_db_connection = connections['default']
#         print(test_db_connection)
#         # Fai qualcosa con il database di test
#         print(connections.databases)

class TimerTestCase(TestCase):
    def setUp(self):
        Timer.objects.create(timer = 4)
        Server.objects.create(ip = "www.google.com", nome="Google", domanda="Ciao", risposta = "Eccomi", tipoRisposta="Stringa")
    def test_config_get_context_data(self):
        request = RequestFactory().get('/config/')
        configView = ConfigView()
        configView.setup(request)
        print(configView.get_context_data())

class AddServerTestCase(TestCase):
    def setUp(self):
        Server.objects.create(ip="www.instagram.com", nome="Instagram", domanda="ciao", risposta="Eccomi", tipoRisposta = "Stringa")
    def test_addServer_get_context_data(self):
        request = RequestFactory().get('/addServer/')
        addServerView = AddServerView()
        addServerView.setup(request)

class DeleteServerTestCase(TestCase):
    def setUp(self):
        Server.objects.create(ip="www.facebook.com", nome="Facebook", domanda="ciao", risposta="Eccomi", tipoRisposta="Stringa")
    def test_deleteServer_get_context_data(self):
        request = RequestFactory().get('/config/')
        deleteServerView = DeleteServerView()
        deleteServerView.setup(request)