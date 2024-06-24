import unittest
from collections import Counter
from nltk.corpus import stopwords
from modules.clases_monticulo import MedianaMonticulo
import nltk
from modules.procesador import ProcesadorDeEstadisticas 

nltk.download('stopwords')
STOPWORDS = stopwords.words('spanish')

class TestProcesadorDeEstadisticas(unittest.TestCase):

    def setUp(self):
        # Datos de prueba
        self.reclamos = [
            {'contenido': 'El producto llegó roto y no funciona', 'estado': 'En Proceso', 'tiempo_resolucion': 5},
            {'contenido': 'No estoy satisfecho con la atención recibida', 'estado': 'Resuelto', 'tiempo_resolucion': 3},
            {'contenido': 'La entrega fue muy rápida y eficiente', 'estado': 'Resuelto', 'tiempo_resolucion': 2},
            {'contenido': 'El producto es de muy baja calidad', 'estado': 'En Proceso', 'tiempo_resolucion': 4},
            {'contenido': 'No recomiendo este servicio a nadie', 'estado': 'Pendiente', 'tiempo_resolucion': None},
        ]

        self.procesador = ProcesadorDeEstadisticas(self.reclamos)

    def test_calcular_porcentajes(self):
        cantidades = [2, 1, 2]  # En Proceso, Resuelto, Pendiente
        porcentajes = self.procesador.calcular_porcentajes(cantidades)
        self.assertAlmostEqual(porcentajes[0], 40.0, places=1)
        self.assertAlmostEqual(porcentajes[1], 20.0, places=1)
        self.assertAlmostEqual(porcentajes[2], 40.0, places=1)

    def test_encontrar_keywords(self):
        palabras_comunes = self.procesador.encontrar_keywords()
        expected_keywords = ['producto', 'llegó', 'roto', 'funciona', 'satisfecho', 'atención', 'recibida', 
                             'entrega', 'rápida', 'eficiente', 'baja', 'calidad', 'recomiendo', 'servicio', 'nadie']
        self.assertEqual(sorted(palabras_comunes), sorted(expected_keywords))

    def test_calcular_mediana(self):
        mediana_proceso = self.procesador.calcular_mediana('En Proceso')
        self.assertEqual(mediana_proceso, 4.5)

        mediana_resuelto = self.procesador.calcular_mediana('Resuelto')
        self.assertEqual(mediana_resuelto, 2.5)


if __name__ == '__main__':
    unittest.main()
