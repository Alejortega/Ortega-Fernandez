class Pelicula:
    def __init__(self, nombre):
        self.nombre = nombre
        self.frases = []


def leer_archivo(nombre_archivo):
    peliculas = {}
   
    with open( nombre_archivo, 'r',encoding="UTF-8") as archivo:
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
