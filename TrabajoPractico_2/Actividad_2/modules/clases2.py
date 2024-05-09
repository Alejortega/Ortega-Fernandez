import numpy as np
import random
from Actividad_2.modules.clases1 import *

class DetectorAlimento: #Nos la dá la cátedra
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su peso.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """función softmax para crear vector de probabilidades 
        que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.alimentos)
        alimento_detectado = self.alimentos[random.randint(0, n_alimentos-1)]
        peso_detectado = random.choices(self.peso_alimentos, self.prob_pesos)[0]
        return {"alimento": alimento_detectado, "peso": peso_detectado}

class CintaTransportadora:
    """Clase que detecta los alimentos que son cargados en el cajón """
    def __init__(self):
        self.sensor = DetectorAlimento()
        
    def cargar_cajon(self, cantidad):
        """Función que carga el cajón con la cantidad de alimentos seleccionada por el usuario"""
        cajon = Cajon() # Crear una instancia de la clase Cajon para cargar los alimentos
        alimentos_generados = 0  # Variable para rastrear la cantidad de alimentos generados
        while alimentos_generados < cantidad:
            alimento_detectado = self.sensor.detectar_alimento()  # Se llama a la función de la clase DetectorAlimento
            if alimento_detectado["alimento"] != "undefined":
                alimento = None  # Se inicializa la variable alimento
                if alimento_detectado["alimento"] == "kiwi":
                    alimento = Kiwi(alimento_detectado["peso"])
                elif alimento_detectado["alimento"] == "manzana":
                    alimento = Manzana(alimento_detectado["peso"])
                elif alimento_detectado["alimento"] == "papa":
                    alimento = Papa(alimento_detectado["peso"])
                elif alimento_detectado["alimento"] == "zanahoria":
                    alimento = Zanahoria(alimento_detectado["peso"])
                if alimento:
                    cajon.agregar_alimento(alimento)  # Agregar el alimento al cajón
                alimentos_generados += 1
        return cajon

class Cajon:
    """Clase que representa un contenedor de alimentos (cajón), para luego poder iterar sobre él"""
    def __init__(self):
        self.contenido = []

    def agregar_alimento(self, alimento):
        """Función para agregar un alimento al cajón"""
        if isinstance(alimento, Alimento):
            self.contenido.append(alimento)

    def __iter__(self):
        """Iterador sobre los alimentos en el cajón"""
        return iter(self.contenido)

    def __len__(self):
        """Función para obtener la cantidad de alimentos en el cajón"""
        return len(self.contenido)


class CalculadoraAws:
    """Clase para calcular los aws promedios de los alimentos cargados en el cajón"""

    def calculadora_aws(self, cajon, tipo_alimento):
        contador = 0
        total_aw = 0
        for alimento in cajon:
            if isinstance(alimento, tipo_alimento):
                total_aw += alimento.calcular_aw()
                contador += 1
                
        if contador == 0:
            return 0  # Retorna 0 si no hay alimentos del tipo especificado en el cajón
        else:
            return round(total_aw / contador, 2)

    def peso_total(self, cajon):
        """Función que calcula el peso total del cajón"""
        peso_total = sum(alimento.peso for alimento in cajon)
        return round(peso_total, 2)



