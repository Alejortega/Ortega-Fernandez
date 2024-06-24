
from modules.graficador import Graficador
from modules.procesador import ProcesadorDeEstadisticas  
from modules.gestores import GestorDeReclamos


class DatosAnalitica:
    """Genera los datos para la analitica de un jefe"""

    def __init__(self, depto,info):
        self.depto=depto
        self.info=info
        self.__graficador=Graficador()
        self.__procesador=ProcesadorDeEstadisticas(self.info)
        #self.__gestor=GestorDeReclamos()
    def generar_grafico_torta(self, estados_lista):
        #info=self.__gestor.obtener_de_db(parametro="departamento", valor=self.depto) #obtengo los deptos del reclamo
        #estados_por_depto=self.__gestor.contar_estados(info) #calcula la cant de estados por depto y devuelve una lista con cada cant
        porcentajes= self.__procesador.calcular_porcentajes(estados_lista) 
        self.__graficador.graficar_torta(porcentajes)
    def generar_grafico_palabras(self):
        #info=self.__gestor.obtener_de_db(parametro="departamento", valor=self.depto)
        palabras_claves=self.__procesador.encontrar_keywords()
        self.__graficador.graficar_nube_palabras(palabras_claves)      
    def obtener_medianas(self):
        mediana_proceso=self.__procesador.calcular_mediana('en_proceso')
        mediana_resueltos=self.__procesador.calcular_mediana('resuelto')
        return mediana_resueltos, mediana_proceso 