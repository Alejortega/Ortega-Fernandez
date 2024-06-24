from modules.gestores import GestorDeReclamos
from modules.analitica import DatosAnalitica
from modules.reportes import *
class Coordinador_jefe:
    """Coordina las distintas acciones que puede realizar un jefe dentro del sistema"""

    def __init__(self):
        self.gestor_reclamos = GestorDeReclamos('./data/clasificador_svm.pkl')
        
    def cambiar_estado_reclamo(self, reclamo_id, nuevo_estado, tiempo_resolucion):
        """Cambia el estado de un reclamo"""
        self.gestor_reclamos.cambiar_estado_de_reclamo(reclamo_id, nuevo_estado, tiempo_resolucion)
        # Agrega aquí lógica adicional si es necesaria, como notificaciones o registros de cambios

    def mostrar_al_jefe(self, valor):
        """Muestra reclamos del depto para un jefe"""
        return self.gestor_reclamos.obtener_de_db(parametro='departamento', valor=valor)  #Llama al método buscar_reclamos_por_departamento
    def crear_analitica(self, valor):
        reclamos=self.gestor_reclamos.obtener_de_db(parametro="departamento", valor=valor)
        estados_por_depto=self.gestor_reclamos.contar_estados(reclamos)
        analitica=DatosAnalitica(valor, reclamos)
        analitica.generar_grafico_palabras()
        analitica.generar_grafico_torta(estados_por_depto)
        medianas=analitica.obtener_medianas()
        return medianas #tupla de dos numeros 
    def generar_reporte(self, valor, medianas, depto):
            #reporte=BaseReporte(100, medianas[1], medianas[0])
            #Contar la cantidad de reclamos(diccionarios) en la lista
            reclamos=self.gestor_reclamos.obtener_de_db(parametro='departamento', valor=depto)
            total_reclamos = sum(1 for item in reclamos if isinstance(item, dict))
            if valor == 'pdf':
                reporte= ReportePDF()
            elif valor == 'html':
                reporte = ReporteHTML()
            else:
                raise ValueError("Tipo de informe no soportado")
            reporte.generar_reporte(total_reclamos, medianas[1], medianas[0]) 

    def derivar_reclamo(self, reclamo_id, departamento_destino):
        """Deriva un reclamo a otro departamento"""
        self.gestor_reclamos.derivar_reclamo_a_depto(reclamo_id, departamento_destino)



