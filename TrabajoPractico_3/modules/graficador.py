import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
import os

class Graficador:
    """
    Clase encargada de generar gráficos para visualizar estadísticas de reclamos.
    """

    @staticmethod
    def graficar_torta(porcentajes):
        """
        Genera un gráfico de tortas con los porcentajes de cada estado.

        """
        etiquetas = ['Pendiente', 'Inválido', 'En Proceso', 'Resuelto']
        #filename = os.path.join('static\grafico_torta.png')

        plt.figure(figsize=(8, 8))
        plt.pie(porcentajes, labels=etiquetas, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  #asegura que el gráfico sea un círculo.
        plt.savefig('static/grafico_torta.png',format='png')
        plt.close()  #cerramos el gráfico para liberar memoria

        #return filename

    @staticmethod
    def graficar_nube_palabras(palabras):
        """
        Genera una nube de palabras con las palabras clave más repetidas.

        """
        #filename = os.path.join('static','nube_palabras.png')

        #crear un diccionario con las palabras y su frecuencia
        frecuencia_palabras = {palabra: i+1 for i, palabra in enumerate(reversed(palabras))}

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frecuencia_palabras)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  #no mostrar ejes
        plt.savefig('static/nube_palabras.png',format='png')
        plt.close()  #cerramos el gráfico para liberar memoria

        #return filename

    