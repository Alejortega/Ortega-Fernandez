from universidad import Universidad
from facultad import Facultad

def mostrar_menu_facultad(facultad):
    ruta_alumnos = "./data/alumnos.txt"
    ruta_profesores_csv = "./data/profesores.csv"
    while True:
        print("\n##########################################")
        print("#  Sistema de Información Universitaria  #")
        print("##########################################")
        print("Elige una opción")
        print("1 - Inscribir alumno")
        print("2 - Contratar profesor")
        print("3 - Crear departamento nuevo")
        print("4 - Crear curso nuevo")
        print("5 - Inscribir estudiante a un curso")
        print("6 - Salir de la facultad")

        opcion_facultad = input("Ingrese el número de opción: ")

        if opcion_facultad == '1':
            facultad.inscribir_alumno(ruta_alumnos)
        elif opcion_facultad == '2':
            facultad.contratar_profesor(ruta_profesores_csv)
        elif opcion_facultad == '3':
            facultad.crear_departamento()
        elif opcion_facultad == '4':
            facultad.crear_curso()
        elif opcion_facultad == '5':
            facultad.inscribir_estudiante_a_curso()
        elif opcion_facultad == '6':
            print("Saliendo de la facultad.")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

def mostrar_menu_principal():
    print("\n##########################################")
    print("#  Sistema de Información Universitaria  #")
    print("##########################################")
    print("Elige una opción")
    print("1 - Crear nueva facultad")
    print("2 - Agregar alumno")
    print("3 - Agregar profesor")
    print("4 - Elegir facultad")
    print("5 - Salir")

def main():
    universidad = Universidad()
    facultad_actual = None

    while True:
        mostrar_menu_principal()
        opcion_principal = input("Ingrese el número de opción: ")

        if opcion_principal == '1':
            universidad.crear_facultad()
        elif opcion_principal == '2':
            universidad.agregar_alumno()
        elif opcion_principal == '3':
            universidad.agregar_profesor()
        elif opcion_principal == '4':
            facultad_actual = universidad.elegir_facultad()
            if facultad_actual:
                mostrar_menu_facultad(facultad_actual)
        elif opcion_principal == '5':
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

if __name__ == "__main__":
    main()
