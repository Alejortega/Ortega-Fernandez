import csv

ruta_alumnos = "./data/alumnos.txt"
ruta_profesores_csv = "./data/profesores.csv"
ruta_depto = "./data/departamentos.csv"
ruta_salida = "./data/inscriptos.csv"
ruta_contra = "./data/contratados.csv"

class Facultad:
    def __init__(self, nombre, alumnos, profesores):
        self.nombre = nombre
        self.alumnos = alumnos
        self.profesores = profesores
        self.departamentos = []
        self.cursos_inscritos = {}

    def mostrar_lista_alumnos(self, alumnos):
        if alumnos:
            print("Alumnos disponibles:")
            for index, alumno in enumerate(alumnos, start=1):
                print(f"{index} - {alumno['Nombre']} {alumno['Apellido']}")
        else:
            print("No hay alumnos disponibles.")

    def inscribir_alumno(self, ruta_alumnos):
        alumnos = self.leer_alumnos_desde_archivo(ruta_alumnos)
        if alumnos:
            self.mostrar_lista_alumnos(alumnos)
            nombre_alumno = input("Ingrese el nombre del alumno a inscribir en la facultad: ")
            apellido_alumno = input("Ingrese el apellido del alumno a inscribir en la facultad: ")
            alumno_encontrado = False
            for alumno in alumnos:
                if alumno['Nombre'] == nombre_alumno and alumno['Apellido'] == apellido_alumno:
                    alumno_encontrado = True
                    break

            if alumno_encontrado:
                self.alumnos.append({'Nombre': nombre_alumno, 'Apellido': apellido_alumno})
                print(f"Alumno '{nombre_alumno} {apellido_alumno}' inscrito en la facultad.")
                self.guardar_alumnos_en_csv("./data/inscriptos.csv")
            else:
                print("Alumno no encontrado en la lista.")
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

    def guardar_alumnos_en_csv(self, ruta_salida):
        try:
            with open(ruta_salida, 'w') as archivo:
                archivo.write('Nombre,Apellido\n')
                for alumno in self.alumnos:
                    archivo.write(f"{alumno['Nombre']},{alumno['Apellido']}\n")
            print(f"Datos de alumnos guardados exitosamente en '{ruta_salida}'.")
        except Exception as e:
            print(f"Error al guardar los datos de alumnos en '{ruta_salida}': {e}")

    def mostrar_lista_profesores(self, profesores):
        if profesores:
            print("Profesores disponibles:")
            for index, profesor in enumerate(profesores, start=1):
                print(f"{index} - {profesor['Nombre']} {profesor['Apellido']}")
        else:
            print("No hay profesores disponibles.")

    def contratar_profesor(self, ruta_profesores_csv):
        profesores = self.leer_profesores_desde_archivo(ruta_profesores_csv)
        if profesores:
            self.mostrar_lista_profesores(profesores)
            nombre_profesor = input("Ingrese el nombre del profesor a contratar: ")
            apellido_profesor = input("Ingrese el apellido del profesor a contratar: ")
            profesor_encontrado = False
            for profesor in profesores:
                if profesor['Nombre'] == nombre_profesor and profesor['Apellido'] == apellido_profesor:
                    profesor_encontrado = True
                    break

            if profesor_encontrado:
                self.profesores.append({'Nombre': nombre_profesor, 'Apellido': apellido_profesor})
                print(f"Profesor '{nombre_profesor} {apellido_profesor}' contratado en la facultad.")
                self.guardar_profesores_en_csv("./data/contratados.csv")
            else:
                print("Profesor no encontrado en la lista.")
        else:
            print("No hay profesores disponibles.")

    def leer_profesores_desde_archivo(self, ruta_profesores_csv):
        profesores = []
        try:
            with open(ruta_profesores_csv, 'r') as archivo:
                lineas = archivo.readlines()
                for linea in lineas:
                    datos_profesor = linea.strip().split(',')
                    profesor = {'Nombre': datos_profesor[0], 'Apellido': datos_profesor[1]}
                    profesores.append(profesor)
        except FileNotFoundError:
            print(f"El archivo {ruta_profesores_csv} no fue encontrado.")
        return profesores

    def guardar_profesores_en_csv(self, ruta_contra):
        try:
            with open(ruta_contra, 'w') as archivo:
                archivo.write('Nombre,Apellido\n')
                for profesor in self.profesores:
                    archivo.write(f"{profesor['Nombre']},{profesor['Apellido']}\n")
            print(f"Datos de profesores guardados exitosamente en '{ruta_contra}'.")
        except Exception as e:
            print(f"Error al guardar los datos de profesores en '{ruta_contra}': {e}")

    def crear_departamento(self):
        nombre_departamento = input("Ingrese el nombre del departamento: ")
        director_elegido = None

        # Mostrar la lista de profesores disponibles para elegir como director
        self.mostrar_lista_profesores(self.profesores)
        
        # Solicitar al usuario que elija al director del departamento
        while True:
            indice_profesor = input("Ingrese el número del profesor que será el director del departamento: ")
            if indice_profesor.isdigit():
                indice = int(indice_profesor) - 1
                if 0 <= indice < len(self.profesores):
                    director_elegido = self.profesores[indice]
                    if director_elegido['Nombre'] not in [depto['Director']['Nombre'] for depto in self.departamentos]:
                        break
                    else:
                        print("Este profesor ya es director de otro departamento. Elija otro.")
                else:
                    print("Número de profesor fuera de rango. Intente nuevamente.")
            else:
                print("Ingrese un número válido.")

        # Crear el departamento y asignar el director
        departamento = {'Nombre': nombre_departamento, 'Director': director_elegido}
        self.departamentos.append(departamento)

        print(f"Departamento '{nombre_departamento}' creado con éxito y {director_elegido['Nombre']} {director_elegido['Apellido']} como director.")

        # Guardar la información del departamento en un archivo CSV
        self.guardar_departamentos_en_csv(ruta_depto)

    def guardar_departamentos_en_csv(self, ruta_depto):
        try:
            with open(ruta_depto, 'w', newline='') as archivo:
                csv_writer = csv.writer(archivo)
                csv_writer.writerow(['Nombre', 'Director'])
                for departamento in self.departamentos:
                    csv_writer.writerow([departamento['Nombre'], f"{departamento['Director']['Nombre']} {departamento['Director']['Apellido']}"])
            print(f"Datos de departamentos guardados exitosamente en '{ruta_depto}'.")
        except Exception as e:
             print(f"Error al guardar los datos de departamentos en '{ruta_depto}': {e}")

# Mostrar la lista de departamentos existentes
        self.mostrar_lista_departamentos()

    def mostrar_lista_departamentos(self):
        if self.departamentos:
            print("Departamentos existentes:")
            for index, depto in enumerate(self.departamentos, start=1):
                print(f"{index} - {depto['Nombre']} (Director: {depto['Director']['Nombre']} {depto['Director']['Apellido']})")
        else:
            print("No hay departamentos existentes.")

    def crear_curso(self):
        # Mostrar la lista de departamentos existentes
        self.mostrar_lista_departamentos()

        # Solicitar al usuario que elija un departamento para crear el curso
        departamento_elegido = None
        while True:
            indice_depto = input("Ingrese el número del departamento donde desea crear el curso: ")
            if indice_depto.isdigit():
                indice = int(indice_depto) - 1
                if 0 <= indice < len(self.departamentos):
                    departamento_elegido = self.departamentos[indice]
                    break
                else:
                    print("Número de departamento fuera de rango. Intente nuevamente.")
            else:
                print("Ingrese un número válido.")

        nombre_curso = input("Ingrese el nombre del curso: ")

        # Mostrar la lista de profesores disponibles para elegir como titular del curso
        self.mostrar_lista_profesores(self.profesores)
        
        # Solicitar al usuario que elija al titular del curso
        titular_elegido = None
        while True:
            indice_profesor = input("Ingrese el número del profesor que será el titular del curso: ")
            if indice_profesor.isdigit():
                indice = int(indice_profesor) - 1
                if 0 <= indice < len(self.profesores):
                    titular_elegido = self.profesores[indice]
                    break
                else:
                    print("Número de profesor fuera de rango. Intente nuevamente.")
            else:
                print("Ingrese un número válido.")

        curso = {'Nombre': nombre_curso, 'Departamento': departamento_elegido, 'Titular': titular_elegido}
        if 'Cursos' not in departamento_elegido:
            departamento_elegido['Cursos'] = []
        departamento_elegido['Cursos'].append(curso)
        print(f"Curso '{nombre_curso}' creado en el departamento '{departamento_elegido['Nombre']}' y con {titular_elegido['Nombre']} {titular_elegido['Apellido']} como titular.")

        # Mostrar la lista de cursos existentes en el departamento después de crear uno nuevo
        self.mostrar_lista_cursos(departamento_elegido)

    def mostrar_lista_cursos(self, departamento):
        if 'Cursos' in departamento and departamento['Cursos']:
            print(f"Cursos en el departamento '{departamento['Nombre']}':")
            for index, curso in enumerate(departamento['Cursos'], start=1):
                print(f"{index} - {curso['Nombre']} (Titular: {curso['Titular']['Nombre']} {curso['Titular']['Apellido']})")
        else:
            print("No hay cursos en este departamento.")
    
    def inscribir_estudiante_a_curso(self):
        self.mostrar_lista_departamentos()

        # Solicitar al usuario que elija un departamento para ver los cursos disponibles
        departamento_elegido = None
        while True:
            indice_depto = input("Ingrese el número del departamento para ver los cursos disponibles: ")
            if indice_depto.isdigit():
                indice = int(indice_depto) - 1
                if 0 <= indice < len(self.departamentos):
                    departamento_elegido = self.departamentos[indice]
                    break
                else:
                    print("Número de departamento fuera de rango. Intente nuevamente.")
            else:
                print("Ingrese un número válido.")

        # Mostrar los cursos disponibles en el departamento elegido
        if 'Cursos' in departamento_elegido and departamento_elegido['Cursos']:
            print(f"Cursos disponibles en el departamento '{departamento_elegido['Nombre']}':")
            for index, curso in enumerate(departamento_elegido['Cursos'], start=1):
                print(f"{index} - {curso['Nombre']} (Titular: {curso['Titular']['Nombre']} {curso['Titular']['Apellido']})")
        else:
            print("No hay cursos disponibles en este departamento.")

        # Solicitar al usuario que elija un curso para inscribir al estudiante
        curso_elegido = None
        while True:
            indice_curso = input("Ingrese el número del curso al que desea inscribir al estudiante: ")
            if indice_curso.isdigit():
                indice = int(indice_curso) - 1
                if 0 <= indice < len(departamento_elegido['Cursos']):
                    curso_elegido = departamento_elegido['Cursos'][indice]
                    break
                else:
                    print("Número de curso fuera de rango. Intente nuevamente.")
            else:
                print("Ingrese un número válido.")

        # Mostrar la lista de alumnos disponibles para inscribir al estudiante
        self.mostrar_lista_alumnos(self.alumnos)

        # Solicitar al usuario que elija un alumno para inscribir en el curso
        alumno_elegido = None
        while True:
            indice_alumno = input("Ingrese el número del alumno que desea inscribir en el curso: ")
            if indice_alumno.isdigit():
                indice = int(indice_alumno) - 1
                if 0 <= indice < len(self.alumnos):
                    alumno_elegido = self.alumnos[indice]
                    break
                else:
                    print("Número de alumno fuera de rango. Intente nuevamente.")
            else:
                print("Ingrese un número válido.")

        # Incribir al estudiante en el curso elegido
        curso_id = curso_elegido['Nombre']
        if curso_id not in self.cursos_inscritos:
            self.cursos_inscritos[curso_id] = []
        self.cursos_inscritos[curso_id].append(alumno_elegido)
        print(f"Estudiante '{alumno_elegido['Nombre']} {alumno_elegido['Apellido']}' inscrito en el curso '{curso_id}'.")

class Estudiante:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.facultades = []

    def inscribir_en_facultad(self, facultad):
        self.facultades.append(facultad)
        facultad.alumnos.append(self)

class Profesor:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.departamentos = []

    def contratar_en_departamento(self, departamento):
        self.departamentos.append(departamento)
        departamento.profesores.append(self)

class Curso:
    def __init__(self, nombre, titular):
        self.nombre = nombre
        self.titular = titular
        self.estudiantes = []

    def inscribir_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)
        estudiante.cursos.append(self)

class Departamento:
    def __init__(self, nombre, director):
        self.nombre = nombre
        self.director = director
        self.profesores = [director]
        director.departamentos.append(self)
        self.cursos = []

    def agregar_curso(self, curso):
        self.cursos.append(curso)





