from modules.gestores import GestorDeReclamos

class Coordinador_usuario:
    """Coordina las distintas acciones que puede realizar un usuario dentro del sistema"""

    def __init__(self,  GestorDB ):
        self.gestor_r = GestorDeReclamos('./data/clasificador_svm.pkl')
        self.gestor_db = GestorDB

    def cargar_usuario(self, datos_usuario): # datos_usuario es un diccionario

        """Gestiona la carga de un usuario nuevo a la base de datos verificando que cumpla 
           con las condiciones de validación de datos"""
        
        email = datos_usuario["email"]
        username = datos_usuario["username"]

        errores = []

        if not self.gestor_db.verificar_disponibilidad(dato_a_chequear="email", dato=email):
            errores.append("El email ya está en uso.")
        if not self.gestor_db.verificar_disponibilidad(dato_a_chequear="username", dato=username):
            errores.append("El nombre de usuario ya está en uso.")

        if errores:
            return errores
        else:
            self.gestor_db.guardar_persona(datos_usuario, 'usuario')
            return "Usuario guardado exitosamente."
        
    def iniciar_reclamo(self, id, contenido, fecha_hora, foto):

        """Gestiona la creación de un reclamo, verificando si hay reclamos similares a mostrar"""
        posible_reclamo = self.gestor_r.crear_reclamo(contenido, fecha_hora, id, foto)  #diccionario
        depto = posible_reclamo["departamento"]  #obtengo el depto del posible reclamo

        lista_reclamos_similares = self.gestor_r.buscar_reclamos_similares(contenido, depto)  # busco reclamos similares según el posible reclamo
        if lista_reclamos_similares:  #es decir, se encontraron reclamos similares
            return lista_reclamos_similares
        else:  #es decir, la lista está vacía y no se encontraron reclamos similares para mostrar
            self.gestor_r.guardar_reclamo_en_db(posible_reclamo)
            return None

    def mostrar_al_usuario(self, accion, valor):

        """Gestiona las acciones de vista que puede tener un usuario"""

        if accion == "mis_reclamos":
            lista_mis_reclamos = self.gestor_r.obtener_de_db(parametro="usuario", valor=valor)
            return lista_mis_reclamos
        elif accion == "listar_reclamos":
            lista_reclamos = self.gestor_r.obtener_de_db(parametro="todos", valor=None)
            return lista_reclamos
        elif accion == "adherirse":
            self.gestor_r.sumar_adherente_a_reclamo(valor)

            