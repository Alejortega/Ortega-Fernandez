from modules.config import db
from modules.models import PersonaDB, ReclamoDB
from modules.preprocesamiento import TextVectorizer
from modules.preprocesamiento import ProcesadorArchivo
import pickle as p
from modules.clasificador import Clasificador 
from modules.reclamos_similares import reclamos_similares 

class GestorDB:
    """El gestor de base de datos almacena, consulta y actualiza la información de la base de datos """

    def __init__(self, db):
        self.db = db #definimos el parámetro db que solo puede controlar este gestor 

    def guardar_persona(self, usuario_data, tipo):
        """Guarda en la db una persona usando tablas, las personas puede solo pueden ser Jefe o Usuario común"""
        if tipo == 'usuario':
            nuevo_usuario = PersonaDB(
                nombre=usuario_data['nombre'],
                apellido=usuario_data['apellido'],
                email=usuario_data['email'],
                username=usuario_data['username'],
                password=usuario_data['password'],
                claustro=usuario_data['claustro'],
                departamento=None  #usuarios normales no tienen departamento
            )
        elif tipo == 'jefe':
            nuevo_usuario = PersonaDB(
                nombre=usuario_data['nombre'],
                apellido=usuario_data['apellido'],
                email=usuario_data['email'],
                username=usuario_data['username'],
                password=usuario_data['password'],
                claustro="",  #jefes no tienen claustro
                departamento=usuario_data['departamento']
            )
        else:
            raise ValueError("Tipo de usuario no válido")

        
        self.db.session.add(nuevo_usuario)
        self.db.session.commit()

    def obtener_reclamos_por_parametro(self, parametro=None, valor=None):
        """Obtiene los reclamos según un parámetro y un valor especificado, si no especifica,
        se obtienen todos los reclamos de la db"""
        if parametro and valor:
            parametro = parametro.lower()
            if isinstance(valor, str):  
                valor = valor.lower()  
            if parametro == 'departamento':
                reclamos = ReclamoDB.query.filter_by(departamento=valor.lower()).all()
            elif parametro == 'estado':
                reclamos = ReclamoDB.query.filter_by(estado=valor.lower()).all()
            elif parametro == 'usuario':
                reclamos = ReclamoDB.query.filter_by(user_id=valor).all()
            elif parametro == 'id':
                reclamos = ReclamoDB.query.filter_by(id=valor).all()
            else:
                raise ValueError(f'Parámetro "{parametro}" no válido.')
        else:
            reclamos = ReclamoDB.query.all()  # devuelve todos los reclamos

        if not reclamos:
            raise ValueError('No se encontraron reclamos que coincidan con los valores especificados.')
        reclamos = [{
            'id': reclamo.id,
            'estado': reclamo.estado,
            'tiempo_resolucion': reclamo.tiempo_resolucion,
            'timestamp': reclamo.timestamp,
            'contenido': reclamo.contenido,
            'adherentes': reclamo.adherentes,
            'user_id': reclamo.user_id,
            'foto': reclamo.foto,
            'departamento': reclamo.departamento} for reclamo in reclamos]

        return reclamos  # lista de dic con los reclamos que correspondan a los filtros
        
        
    def verificar_disponibilidad(self, dato_a_chequear, dato):
        """Chequea en la db la disponibilidad de un email y un nombre de usuario"""
        dato_a_chequear = dato_a_chequear.lower()
        
        if dato_a_chequear in ["username", "email"]:
            if dato_a_chequear == "email":
                email_en_uso = PersonaDB.query.filter_by(email=dato).first()
                if email_en_uso:
                    return False  #el email no está disponible para usar
            else:
                username_en_uso = PersonaDB.query.filter_by(username=dato).first()
                if username_en_uso:
                    return False  #el username no está disponible para usar
            return True  #el dato está disponible para usar
        else:
            raise ValueError("Este dato no necesita ser verificado para disponibilidad")

    def guardar_reclamo(self, datos_reclamo):
        """Recibe un diccionario como dato y guarda el reclamo en la db"""
        nuevo_reclamo = ReclamoDB(
            estado=datos_reclamo['estado'],
            tiempo_resolucion=datos_reclamo['tiempo_resolucion'],
            timestamp=datos_reclamo['timestamp'],
            contenido=datos_reclamo['contenido'],
            adherentes=datos_reclamo['adherentes'],
            user_id=datos_reclamo['user_id'],
            foto=datos_reclamo.get('foto'),
            departamento=datos_reclamo['departamento']
        )
        self.db.session.add(nuevo_reclamo)
        self.db.session.commit()
    

  
    def derivar_reclamo(self, reclamo_id, departamento_destino):
        """Deriva un reclamo que se encuentra en un depto a otro depto especificado"""
        reclamo = self.obtener_reclamos_por_parametro(parametro='id', valor=reclamo_id)
        if reclamo:
            reclamo_objeto = ReclamoDB.query.filter_by(id=reclamo_id).first()
            reclamo_objeto.departamento = departamento_destino.lower()  
            self.db.session.commit()
    
    def sumar_adherentes(self, reclamo_id):
        reclamo = self.obtener_reclamos_por_parametro(parametro='id', valor=reclamo_id)
        if reclamo:
            reclamo = reclamo[0]  # Obtener el primer reclamo de la lista, suponiendo que solo hay uno
            reclamo_objeto = ReclamoDB.query.filter_by(id=reclamo_id).first()  # Obtener el objeto reclamo de la base de datos
            reclamo_objeto.adherentes += 1  # Incrementar el contador de adherentes en la base de datos
            self.db.session.commit()
    
    def cambiar_estado(self, reclamo_id, nuevo_estado, tiempo_resolucion=None, departamento_destino=None):
        reclamo = self.obtener_reclamos_por_parametro(parametro='id', valor=reclamo_id)
        if reclamo:
            reclamo = reclamo[0]  # Obtener el primer reclamo de la lista, suponiendo que solo hay uno
            reclamo_objeto = ReclamoDB.query.filter_by(id=reclamo_id).first()  # Obtener el objeto reclamo de la base de datos
            reclamo_objeto.estado = nuevo_estado
        if nuevo_estado == 'en_proceso' and tiempo_resolucion:
            reclamo_objeto.tiempo_resolucion = tiempo_resolucion
        if departamento_destino:
            reclamo_objeto.departamento = departamento_destino  # Actualiza el departamento del reclamo al destino
        self.db.session.commit()
    
#lower: convierte a minúsculas


class GestorDeReclamos():
    def __init__(self, ruta):
        
        with open(ruta, 'rb') as archivo:
           self.__clasificador = p.load(archivo)
        
        self.gestordb = GestorDB(db)
           
    def crear_reclamo(self, contenido, fecha_hora, user_id, foto):
        """Crea un diccionario con la información de un reclamo realizado por un usuario"""

        departamento = self.clasificar_reclamo(contenido)
        datos_reclamo = {
                'estado': 'pendiente',  #estado por default
                'tiempo_resolucion': None,  #Lo determina un jefe después
                'timestamp': fecha_hora ,  
                'contenido': contenido,
                'adherentes': 0,  #valor por defecto, se modifica cuando se adhiere algún usuario
                'user_id': user_id,
                'foto': foto,  #puede ser None, es decir, el usuario no cargó foto
                'departamento': departamento
            }
            #obtener el departamento mediante el clasificador
        

        
        return datos_reclamo
    #self.__gestordb.guardar_reclamo(datos_reclamo)

         
    def buscar_reclamos_similares(self, contenido, depto_perteneciente):
        reclamos_same_depto = self.gestordb.obtener_reclamos_por_parametro(parametro='departamento', valor=depto_perteneciente)
        reclamos_similares_lista = reclamos_similares(reclamos_same_depto, contenido) #devuelve lista de ids de reclamos
        reclamos_sim=[] 
        for r_id in reclamos_similares_lista:

                reclamo_por_id = self.gestordb.obtener_reclamos_por_parametro(parametro="id", valor=r_id)
                
                # Extender la lista de reclamos con el reclamo obtenido
                reclamos_sim.extend(reclamo_por_id) 
        
        return reclamos_sim
    
    def clasificar_reclamo(self, contenido):
        """Clasifica el reclamo en un depto según el contendio del mismo"""
        return self.__clasificador.clasificar([contenido])[0]
    
    def guardar_reclamo_en_db(self, datos_reclamo):
        """Guarda el reclamo creado en la db usando el gestordb"""
        self.gestordb.guardar_reclamo(datos_reclamo)   # guardar el reclamo

    def contar_estados(self, reclamos):
        """Cuenta la cantidad de estados (pendiente, en proceso, resueltos e inválidos) en la lista de reclamos"""

        pendiente = 0
        invalido = 0
        en_proceso = 0
        resuelto = 0
        
        for reclamo in reclamos:
            if reclamo['estado'] == 'pendiente':
                pendiente += 1
            elif reclamo['estado'] == 'invalido':
                invalido += 1
            elif reclamo['estado'] == 'en_proceso':
                en_proceso += 1
            elif reclamo['estado'] == 'resuelto':
                resuelto += 1
        
        return [pendiente, invalido, en_proceso, resuelto]

    def obtener_de_db(self, parametro, valor):
        if parametro=="todos":
            reclamos_de_db=self.gestordb.obtener_reclamos_por_parametro() #todos los reclamos de la db
            return reclamos_de_db
        elif parametro=="departamento":
            reclamos_depto=self.gestordb.obtener_reclamos_por_parametro(parametro=parametro, valor=valor) #todos los reclamos de un depto
            return reclamos_depto
        elif parametro=="usuario":
            reclamos_de_un_user = self.gestordb.obtener_reclamos_por_parametro(parametro="usuario", valor=valor) #todos los reclamos de un user
            return reclamos_de_un_user
        else:
            raise ValueError('No se encontraron reclamos que coincidan con los valores especificados.')
       
    def sumar_adherente_a_reclamo(self, reclamo_id):
        """Incrementa el contador de adherentes para un reclamo específico"""
        self.gestordb.sumar_adherentes(reclamo_id)

    def derivar_reclamo_a_depto(self, reclamo_id, departamento_destino):
        """Deriva un reclamo específico a otro departamento"""
        self.gestordb.derivar_reclamo(reclamo_id, departamento_destino)

    def cambiar_estado_de_reclamo(self, reclamo_id, nuevo_estado, tiempo_resolucion=None, departamento_destino=None):
        """Cambia el estado de un reclamo específico"""
        self.gestordb.cambiar_estado(reclamo_id, nuevo_estado, tiempo_resolucion, departamento_destino)

        