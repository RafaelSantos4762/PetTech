from django.test import TestCase,SimpleTestCase


class CoreViewTest(SimpleTestCase):

    def test_index_200(self):
        resposta = self.client.get("")
        self.assertEqual(resposta,status_code,200)