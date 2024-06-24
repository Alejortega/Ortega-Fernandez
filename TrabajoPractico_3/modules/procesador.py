import nltk
from collections import Counter
from nltk.corpus import stopwords
from modules.clases_monticulo import MedianaMonticulo

nltk.download('stopwords')
STOPWORDS = stopwords.words('spanish')

class ProcesadorDeEstadisticas:
    """
    Clase encargada de calcular porcentajes, mediana y obtener las palabras claves.
    """

    def __init__(self, reclamos):
        self.reclamos = reclamos #lista de dics

    def calcular_porcentajes(self, cantidades):
        """Calcula en qué porcentaje se encunetra cada estado de los reclamos de cada depto"""
        total_reclamos = sum(cantidades)
        if total_reclamos == 0:
            return [0.0 for _ in cantidades]
        
        porcentajes = [(cantidad / total_reclamos) * 100 for cantidad in cantidades]
        return porcentajes #lista con cada porcentaje

    def encontrar_keywords(self):
        """
        Encuentra las 15 palabras más repetidas en los contenidos de los reclamos, ignorando 
        stopwords y espacios en blanco.

        """
        contenido_total = " ".join([reclamo['contenido'] for reclamo in self.reclamos])
        palabras = contenido_total.lower().split()
        palabras_filtradas = [palabra for palabra in palabras if palabra not in STOPWORDS and palabra.isalpha()]
        
        conteo_palabras = Counter(palabras_filtradas)
        palabras_comunes = [palabra for palabra, _ in conteo_palabras.most_common(15)]
        
        return palabras_comunes #lista con las 15 palabras más repetidas

    def calcular_mediana(self, estado_reclamo):
        """
        Calcula la mediana del tiempo de resolución para los estados 'En Proceso' y 'Resuelto'.

        """
        tiempos_resolucion = []
        

        for reclamo in self.reclamos:
            estado = reclamo.get('estado')
            tiempo_resolucion = reclamo.get('tiempo_resolucion')

            if estado == estado_reclamo:
                tiempos_resolucion.append(tiempo_resolucion)
            
        mediana_calculator = MedianaMonticulo()

        for tiempo in tiempos_resolucion:
            mediana_calculator.insertar(tiempo)

        return mediana_calculator.obtenerMediana()