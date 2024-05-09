import unittest
from Actividad_2.modules.clases1 import *
from Actividad_2.modules.clases2 import Cajon, CalculadoraAws

class TestCalculadoraAws(unittest.TestCase):
   


    def test_promedio_total(self):
        calculadora = CalculadoraAws()
        cajon = Cajon()
        cajon.agregar_alimento(Manzana(0.2))
        cajon.agregar_alimento(Kiwi(0.1))
        cajon.agregar_alimento(Papa(0.3))
        cajon.agregar_alimento(Zanahoria(0.4))

        # Verificar el cálculo del promedio total de aw
        self.assertAlmostEqual(calculadora.calculadora_aws(cajon, Alimento), 0.85)
        self.assertAlmostEqual(calculadora.calculadora_aws(cajon, Fruta), 0.78)
        self.assertAlmostEqual(calculadora.calculadora_aws(cajon, Verdura), 0.93)
        self.assertAlmostEqual(calculadora.calculadora_aws(cajon, Manzana), 0.87)


if __name__ == '__main__':
    unittest.main()
