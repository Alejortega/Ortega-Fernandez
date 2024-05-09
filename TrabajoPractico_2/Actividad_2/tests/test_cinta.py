import unittest
from Actividad_2.modules.clases1 import Manzana, Kiwi, Papa, Zanahoria
from Actividad_2.modules.clases2 import CintaTransportadora

class TestCintaTransportadora(unittest.TestCase):
    def test_cargar_cajon(self):
        cinta = CintaTransportadora()

        cajon = cinta.cargar_cajon(7)

        #Verificar si se han cargado los alimentos correctamente
        self.assertEqual(len(cajon), 7)  #El cajón debe tener 7 alimentos
        
        #Verificar si todos los alimentos en el cajón son de clases válidas
        for alimento in cajon:
            self.assertTrue(isinstance(alimento, (Manzana, Kiwi, Papa, Zanahoria)))

if __name__ == '__main__':
    unittest.main()

