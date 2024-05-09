from facultad import Facultad
from modules.funciones import crear_universidad, agregar_alumno, agregar_profesor

ruta_facultades_csv = "./data/facultades.csv"
ruta_alumnos = "./data/alumnos.txt"
ruta_profesores_csv = "./data/profesores.csv"

class Universidad:
    def __init__(self):
        self.facultades = self.cargar_facultades_desde_csv(ruta_facultades_csv)
        self.alumnos = []
        self.profesores = []

    def cargar_facultades_desde_csv(self, ruta_facultades_csv):
        with open(ruta_facultades_csv, 'r') as archivo_csv:
            return [line.strip() for line in archivo_csv.readlines()]


    def crear_facultad(self):
        nueva_facultad = crear_universidad(ruta_facultades_csv, ruta_facultades_csv, self.facultades)


    def agregar_alumno(self):
        agregar_alumno(ruta_alumnos)
        print("Alumno agregado exitosamente.")

    def agregar_profesor(self):
        agregar_profesor(ruta_profesores_csv)
        print("Profesor agregado exitosamente.")

    def elegir_facultad(self):
        if not self.facultades:
            print("No hay facultades disponibles para elegir.")
            return None

        print("Facultades disponibles:")
        for index, facultad in enumerate(self.facultades, start=1):
            print(f"{index} - {facultad}")

        opcion_facultad = input("Ingrese el número de la facultad: ")
        try:
            opcion_facultad = int(opcion_facultad)
            if 1 <= opcion_facultad <= len(self.facultades):
                print(f"Ha elegido la facultad '{self.facultades[opcion_facultad - 1]}'.")
                return Facultad(self.facultades[opcion_facultad - 1], self.alumnos, self.profesores)
            else:
                print("Número de facultad no válido.")
        except ValueError:
            print("Ingrese un número válido para la facultad.")
        return None

    def guardar_facultades(self):
        with open(ruta_facultades_csv, 'w') as archivo_csv:
            for facultad in self.facultades:
                archivo_csv.write(f"{facultad}\n")




