from django.db import connections
from django.test import TestCase

class MyTestCase(TestCase):
    def test_access_test_database(self):
        test_db_connection = connections['default']
        print(test_db_connection)
        # Fai qualcosa con il database di test
        print(connections.databases)
