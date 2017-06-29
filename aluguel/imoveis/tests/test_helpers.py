from django.test import TestCase

from aluguel.imoveis import helpers


class HelpersTest(TestCase):

    def setUp(self):
        self.lat_delta = 0.0089831
        self.lng_delta = 0.009044

    def test_get_min_max_coordenates(self):
        """Garante que os valores retornados estão corretos."""
        bounds = helpers.get_min_max_coordenates()
        self.assertEqual((-self.lat_delta, self.lat_delta, -self.lng_delta, self.lng_delta), bounds)

    def test_get_min_max_coordenates_2(self):
        """Garante que os valores retornados estão corretos."""
        bounds = helpers.get_min_max_coordenates(20, 30)
        self.assertEqual((20 - self.lat_delta, 20 + self.lat_delta, 30 - self.lng_delta, 30 + self.lng_delta), bounds)

    def test_get_coordenates_endereco_invalido(self):
        coordenadas = helpers.get_coordenates("")
        self.assertEqual(None, coordenadas)

    def test_get_coordenates_endereco_valido(self):
        coordenadas = helpers.get_coordenates("Rua da Quitanda, 86, Rio de Janeiro")
        expected = (-22.9026854, -43.1769713, 'R. da Quitanda, 86 - Centro, Rio de Janeiro - RJ, Brasil')
        self.assertEqual(expected, coordenadas)
