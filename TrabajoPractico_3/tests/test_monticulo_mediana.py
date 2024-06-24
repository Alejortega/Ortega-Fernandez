import unittest
from modules.clases_monticulo import MedianaMonticulo
class TestMedianaMonticulo(unittest.TestCase):

    def test_insertar_y_obtenerMediana(self):
        mediana_monticulo = MedianaMonticulo()

        #insertar un único elemento
        mediana_monticulo.insertar(10)
        self.assertEqual(mediana_monticulo.obtenerMediana(), 10)

        #insertar otro elemento
        mediana_monticulo.insertar(20)
        self.assertEqual(mediana_monticulo.obtenerMediana(), 15)

        #insertar más elementos
        mediana_monticulo.insertar(30)
        self.assertEqual(mediana_monticulo.obtenerMediana(), 20)

        mediana_monticulo.insertar(5)
        self.assertEqual(mediana_monticulo.obtenerMediana(), 15)

        mediana_monticulo.insertar(25)
        self.assertEqual(mediana_monticulo.obtenerMediana(), 20)

    def test_balancear(self):
        mediana_monticulo = MedianaMonticulo()
        mediana_monticulo.insertar(10)
        mediana_monticulo.insertar(20)
        mediana_monticulo.insertar(30)
        self.assertEqual(mediana_monticulo.maxHeap.listaMonticulo[1:], [20, 10])
        self.assertEqual(mediana_monticulo.minHeap.listaMonticulo[1:], [30])

    def test_obtenerMediana_con_elementos_pares(self):
        mediana_monticulo = MedianaMonticulo()
        valores = [10, 20, 30, 40]
        for valor in valores:
            mediana_monticulo.insertar(valor)
        self.assertEqual(mediana_monticulo.obtenerMediana(), (20 + 30) / 2.0)

    def test_obtenerMediana_con_elementos_impares(self):
        mediana_monticulo = MedianaMonticulo()
        valores = [10, 20, 30, 40, 50]
        for valor in valores:
            mediana_monticulo.insertar(valor)
        self.assertEqual(mediana_monticulo.obtenerMediana(), 30)

if __name__ == '__main__':
    unittest.main()
