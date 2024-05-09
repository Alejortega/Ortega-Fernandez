import csv

def agregar_alumno(ruta_alumnos):
    print("Agregar nuevo alumno")
    nombre = input("Ingrese el nombre del alumno: ")
    apellido = input("Ingrese el apellido del alumno: ")
    edad = input("Ingrese la edad del alumno: ")

    nuevo_alumno = f"{nombre},{apellido},{edad}\n"
    with open(ruta_alumnos, mode='r') as archivo:
        if nuevo_alumno not in archivo.readlines():  # Verificar si el alumno ya está en el archivo
            with open(ruta_alumnos, mode='a') as archivo:
                archivo.write(nuevo_alumno)
            print("Alumno agregado exitosamente.")
        else:
            print("El alumno ya está en la lista de alumnos.")

def agregar_profesor(ruta_profesores_csv):
    print("Agregar nuevo profesor")
    nombre = input("Ingrese el nombre del profesor: ")
    apellido = input("Ingrese el apellido del profesor: ")
    edad = input("Ingrese la edad del profesor: ")

    nuevo_profesor = f"{nombre},{apellido},{edad}\n"
    with open(ruta_profesores_csv, mode='r') as archivo:
        if nuevo_profesor not in archivo.readlines():  # Verificar si el profesor ya está en el archivo
            with open(ruta_profesores_csv, mode='a') as archivo:
                archivo.write(nuevo_profesor)
            print("Profesor agregado exitosamente.")
        else:
            print("El profesor ya está en la lista de profesores.")

def crear_universidad(ruta_universidades_csv, ruta_facultades_csv, universidades):
    nombre_universidad = input("Ingrese el nombre de la facultad: ")
    # Leer las universidades existentes desde el archivo CSV
    with open(ruta_universidades_csv, 'r') as archivo_universidades:
        universidades_exist = [line.strip() for line in archivo_universidades.readlines()]

    if nombre_universidad not in universidades_exist:  # Verificar si la universidad/facultad ya existe
        nueva_universidad = {'Nombre': nombre_universidad}
        universidades.append(nueva_universidad)
        print(f"¡Facultad '{nombre_universidad}' creada exitosamente!")

        # Guardar la nueva universidad/facultad en el archivo CSV de universidades y facultades
        with open(ruta_universidades_csv, 'a', newline='') as archivo_universidades:
            escritor_universidades = csv.writer(archivo_universidades)
            escritor_universidades.writerow([nombre_universidad])

    else:
        print(f"La facultad '{nombre_universidad}' ya están en la lista de facultades.")


def agregar_alumno(ruta_alumnos):
    print("Agregar nuevo alumno")
    nombre = input("Ingrese el nombre del alumno: ")
    apellido = input("Ingrese el apellido del alumno: ")
    edad = input("Ingrese la edad del alumno: ")

    nuevo_alumno = f"{nombre},{apellido},{edad}\n"
    with open(ruta_alumnos, mode='r') as archivo:
        if nuevo_alumno not in archivo.readlines():  # Verificar si el alumno ya está en el archivo
            with open(ruta_alumnos, mode='a') as archivo:
                archivo.write(nuevo_alumno)
            print("Alumno agregado exitosamente.")
        else:
            print("El alumno ya está en la lista de alumnos.")

def agregar_profesor(ruta_profesores_csv):
    print("Agregar nuevo profesor")
    nombre = input("Ingrese el nombre del profesor: ")
    apellido = input("Ingrese el apellido del profesor: ")
    edad = input("Ingrese la edad del profesor: ")

    nuevo_profesor = f"{nombre},{apellido},{edad}\n"
    with open(ruta_profesores_csv, mode='r') as archivo:
        if nuevo_profesor not in archivo.readlines():  # Verificar si el profesor ya está en el archivo
            with open(ruta_profesores_csv, mode='a') as archivo:
                archivo.write(nuevo_profesor)
            print("Profesor agregado exitosamente.")
        else:
            print("El profesor ya está en la lista de profesores.")



def inscribir_alumno(self, ruta_alumnos):
    alumnos = self.leer_alumnos_desde_archivo(ruta_alumnos)
    if alumnos:
        nombre_alumno = input("Ingrese el nombre del alumno a inscribir en la facultad: ")
        apellido_alumno = input("Ingrese el apellido del alumno a inscribir en la facultad: ")
        alumno_encontrado = False
        for alumno in alumnos:
            if alumno['Nombre'] == nombre_alumno and alumno['Apellido'] == apellido_alumno:
                alumno_encontrado = True
                break

            if alumno_encontrado:
                print(f"Alumno '{nombre_alumno} {apellido_alumno}' inscrito en la facultad.")
            else:
                print("Alumno no encontrado en la lista.")
        else:
            print("No hay alumnos disponibles.")

def mostrar_lista_alumnos(self, alumnos):
        if alumnos:
            print("Alumnos disponibles:")
            for index, alumno in enumerate(alumnos, start=1):
                print(f"{index} - {alumno['Nombre']} {alumno['Apellido']}")
        else:
            print("No hay alumnos disponibles.")

def leer_alumnos_desde_archivo(self, ruta_alumnos):
        alumnos = []
        try:
            with open(ruta_alumnos, 'r') as archivo:
                lineas = archivo.readlines()
                for linea in lineas:
                    datos_alumno = linea.strip().split(',')
                    alumno = {'Nombre': datos_alumno[0], 'Apellido': datos_alumno[1]}
                    alumnos.append(alumno)
        except FileNotFoundError:
            print(f"El archivo {ruta_alumnos} no fue encontrado.")
        return alumnos
