import unittest
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from modules.graficador import Graficador  

class TestGraficador(unittest.TestCase):

    def setUp(self):
        #crear un directorio temporal para guardar las imágenes de prueba
        self.output_dir = 'static'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        #eliminar los archivos generados después de cada prueba
        for file in ['grafico_torta.png', 'nube_palabras.png']:
            file_path = os.path.join(self.output_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_graficar_torta(self):
        porcentajes = [20, 10, 30, 40] 
        Graficador.graficar_torta(porcentajes)

        #verificar que el archivo se creó correctamente
        file_path = os.path.join(self.output_dir, 'grafico_torta.png')
        self.assertTrue(os.path.exists(file_path))

    def test_graficar_nube_palabras(self):
        palabras = ['producto', 'calidad', 'servicio', 'rápida', 'eficiente']  
        Graficador.graficar_nube_palabras(palabras)

        #verificar que el archivo se creó correctamente
        file_path = os.path.join(self.output_dir, 'nube_palabras.png')
        self.assertTrue(os.path.exists(file_path))

if __name__ == '__main__':
    unittest.main()
