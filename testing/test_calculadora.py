import unittest

from testing.calculadora import Calculadora


class TestCalculadora(unittest.TestCase):


    def setUp(self):
        self.calculadora = Calculadora()

    def test_suma(self):
        valor_actual = self.calculadora.sumar(3, 2)
        valor_esperado = 5
        self.assertEqual(valor_esperado, valor_actual)


    def test_division_por_cero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculadora.dividir(10, 0)

