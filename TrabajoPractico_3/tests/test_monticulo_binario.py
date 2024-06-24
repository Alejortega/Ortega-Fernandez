import unittest
from modules.clases_monticulo import MonticuloBinario, MedianaMonticulo  

class TestMonticuloBinario(unittest.TestCase):
    
    def test_insertar_min(self):
        monticulo = MonticuloBinario(es_min=True)
        monticulo.insertar(5)
        monticulo.insertar(3)
        monticulo.insertar(17)
        monticulo.insertar(10)
        monticulo.insertar(84)
        monticulo.insertar(19)
        monticulo.insertar(6)
        monticulo.insertar(22)
        monticulo.insertar(9)
        self.assertEqual(monticulo.listaMonticulo[1:], [3, 5, 6, 9, 84, 19, 17, 22, 10])

    def test_insertar_max(self):
        monticulo = MonticuloBinario(es_min=False)
        monticulo.insertar(5)
        monticulo.insertar(3)
        monticulo.insertar(17)
        monticulo.insertar(10)
        monticulo.insertar(84)
        monticulo.insertar(19)
        monticulo.insertar(6)
        monticulo.insertar(22)
        monticulo.insertar(9)
        self.assertEqual(monticulo.listaMonticulo[1:], [84, 22, 19, 17, 10, 5, 6, 3, 9])

    def test_eliminarMin(self):
        monticulo = MonticuloBinario(es_min=True)
        monticulo.construirMonticulo([9, 5, 6, 2, 3])
        self.assertEqual(monticulo.eliminarMin(), 2)
        self.assertEqual(monticulo.eliminarMin(), 3)
        self.assertEqual(monticulo.eliminarMin(), 5)
        self.assertEqual(monticulo.eliminarMin(), 6)
        self.assertEqual(monticulo.eliminarMin(), 9)

    def test_construirMonticulo(self):
        monticulo = MonticuloBinario(es_min=True)
        monticulo.construirMonticulo([9, 5, 6, 2, 3])
        self.assertEqual(monticulo.listaMonticulo[1:], [2, 3, 6, 5, 9])

    def test_insertar_y_eliminarMin(self):
        monticulo = MonticuloBinario(es_min=True)
        monticulo.insertar(10)
        monticulo.insertar(20)
        monticulo.insertar(15)
        monticulo.insertar(30)
        monticulo.insertar(40)
        self.assertEqual(monticulo.eliminarMin(), 10)
        self.assertEqual(monticulo.eliminarMin(), 15)
        self.assertEqual(monticulo.eliminarMin(), 20)
        self.assertEqual(monticulo.eliminarMin(), 30)
        self.assertEqual(monticulo.eliminarMin(), 40)

if __name__ == '__main__':
    unittest.main()