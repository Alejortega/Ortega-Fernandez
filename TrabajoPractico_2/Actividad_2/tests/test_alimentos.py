import unittest #sirve para crear pruebas unitarias en python, usamos coverage para medir la cobertura de código de las pruebas
from Actividad_2.modules.clases1 import * 


class TestAlimento(unittest.TestCase):
    def test_calculo_aw_manzana(self):
        manzana = Manzana(0.2)
        self.assertAlmostEqual(manzana.calcular_aw(), 0.87) 
        
    def test_calculo_aw_kiwi(self):
        kiwi = Kiwi(0.1)  
        self.assertAlmostEqual(kiwi.calcular_aw(), 0.69)

    def test_calculo_aw_papa(self):
        papa = Papa(0.3)  
        self.assertAlmostEqual(papa.calcular_aw(), 0.92) 

    def test_calculo_aw_zanahoria(self):
        zanahoria = Zanahoria(0.4)  
        self.assertAlmostEqual(zanahoria.calcular_aw(), 0.94)  

    
if __name__ == '__main__':
    unittest.main()

