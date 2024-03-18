class Pelicula:
    def __init__(self, nombre):
        self.nombre = nombre
        self.frases = []

def leer_archivo(nombre_archivo):
    peliculas = {}
   
    with open( nombre_archivo, 'r') as archivo:
        for linea in archivo:
            partes = linea.strip().split(';')
            nombre_pelicula = partes[1].strip().lower()
            frase = partes[0].strip()
            if nombre_pelicula not in peliculas:
                peliculas[nombre_pelicula] = Pelicula(nombre_pelicula)
            peliculas[nombre_pelicula].frases.append(frase)
    return peliculas

def listar_peliculas(peliculas):
    nombres_unicos = set()
    for pelicula in peliculas.values():
        nombres_unicos.add(pelicula.nombre.capitalize())
    nombres_unicos = sorted(nombres_unicos)
    for idx, nombre in enumerate(nombres_unicos, start=1):
        print(f"{idx}. {nombre}")
    return nombres_unicos

if __name__ == "__main__":
    nombre_archivo = "frases_de_peliculas.txt"  # nombre del archivo
    peliculas = leer_archivo(nombre_archivo)
    listar_peliculas(peliculas)

import random

def obtener_frase_y_opciones(peliculas):
    lista_peliculas = list(peliculas.values())  # Obtener una lista de todas las películas
    pelicula = random.choice(lista_peliculas)   # Seleccionar una película al azar de la lista
    frase = random.choice(pelicula.frases)      # Seleccionar una frase al azar de la película
    pelicula_correcta = pelicula.nombre         # Obtener el nombre de la película correcta
    opciones = [pelicula_correcta]              # Agregar la película correcta como la primera opción

    # Seleccionar otras dos películas incorrectas, diferentes de la correcta
    while len(opciones) < 3:
        opcion = random.choice(lista_peliculas).nombre
        if opcion != pelicula_correcta and opcion not in opciones:
            opciones.append(opcion)

    # Mezclar las opciones para que no estén en el mismo orden siempre
    random.shuffle(opciones)

    return frase, opciones, pelicula_correcta




