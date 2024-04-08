class Pelicula:
    def __init__(self, nombre):
        self.nombre = nombre
        self.frases = []


def leer_archivo(nombre_archivo):
    """Lee un archivo y obtiene los nombres de peliculas y sus frases, retorna un diccionario"""
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
    """A partir de un diccionario (parámetro) obtiene los nombre únicos de las películas(por si hay nombres repetidos),
       y los dsordena en orden alfabético"""
    nombres_unicos = set()
    for pelicula in peliculas.values():
        nombres_unicos.add(pelicula.nombre.capitalize())
    nombres_unicos = sorted(nombres_unicos)
    for idx, nombre in enumerate(nombres_unicos, start=1):
        print(f"{idx}. {nombre}")
    return nombres_unicos

def guardar_datos_en_archivo(nombre_archivo, usuario, aciertos, fecha, tot_ac):
    """Guarda la información de la lista histórica en un archivo para no perder los datos
    """  
    with open(nombre_archivo, "a") as archi:
        archi.write(f"{usuario},{aciertos},{fecha},{tot_ac}\n")


import random

def cargar_frases_y_peliculas(num_frases, nombre_archivo):
    """funcion para elegir la frase y las opciones(peliculas) de la primera ronda"""
    # Abrir el archivo que contiene las frases y respuestas
    with open(nombre_archivo, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Separar las frases y respuestas en listas separadas
    frases = []
    peliculas = []
    for line in lines:
        frase, pelicula = line.strip().split(';')
        frases.append(frase)
        peliculas.append(pelicula)

    # Verificar que haya suficientes preguntas en el archivo
    if len(frases) < num_frases:
        return 'El archivo no contiene suficientes frases para la cantidad solicitada.'

    # Seleccionar un número aleatorio de índices de preguntas para mostrar al usuario
    indice_seleccionado = random.sample(range(len(frases)), num_frases)
    frases_seleccionadas = [(frases[i], peliculas[i]) for i in indice_seleccionado]

    # Generar opciones para cada pregunta
    opciones = []
    for frase, pelicula in frases_seleccionadas:
        # Opción correcta
        opcion_correcta = pelicula

        # Opciones falsas aleatorias
        todas_las_opciones = peliculas[:]  # Copia la lista de respuestas
        todas_las_opciones.remove(opcion_correcta)  # Elimina la respuesta correcta

        # Elegir dos respuestas falsas aleatorias sin repetir y mezclarlas con la respuesta correcta
        opciones_incorrectas = random.sample(todas_las_opciones, 2)
        opciones_para_preguntas = [opcion_correcta] + opciones_incorrectas

        # Mezclar las opciones para que no siempre aparezcan en el mismo orden
        random.shuffle(opciones_para_preguntas)

        # Agregar las opciones al listado final
        opciones.append(opciones_para_preguntas)  # Solo las opciones, sin la pregunta

    return frases_seleccionadas, opciones

def verificar_respuesta(respuesta_del_usuario, respuesta_correcta):
    """Verifica si la respuesta del usuario fue correcta o incorrecta y retorna un mensaje dependiendo 
       cuál sea el caso """
    
    if respuesta_del_usuario == respuesta_correcta:
        message = '¡Respuesta correcta!'
    else:
        message = f'Respuesta incorrecta. La respuesta correcta es: {respuesta_correcta}'
    return message

def leer_archivo_de_resultados(nom_archi):
    """Lee un archivo y devuelve una lista con las líneas del archivo"""
    with open(nom_archi, "r") as archi:
        resultados = [linea.strip().split(',') for linea in archi]
    return resultados


import base64
from io import BytesIO
import matplotlib.pyplot as plt
from collections import defaultdict #defaultdict:  proporciona un valor predeterminado para las claves que aún no están presentes en el diccionario
def generar_graficas(nom_archi, num_total_preguntas ):
    """Lee un archivo y en función de los datos crea dos gráficas (una de tortas y una de curvas)"""
    with open(nom_archi, "r") as f:
         lineas = f.readlines()
         aciertos_por_fecha = defaultdict(int)
         desaciertos_por_fecha = defaultdict(int)
        
    for l in lineas:
        usuario, fraccion, fecha, acierto = l.strip().split(',')
        fecha_sin_hora = fecha.split()[0]
        aciertos, total_preguntas = fraccion.strip().split('/')
        acierto_int = int(acierto)
        num_total_frases = int(total_preguntas)
        desacierto = num_total_frases - acierto_int
            
        aciertos_por_fecha[fecha_sin_hora] += acierto_int
        if desacierto >= 0:
            desaciertos_por_fecha[fecha_sin_hora] += desacierto
                
    # Ordenar las fechas
    fechas = sorted(aciertos_por_fecha.keys())
    
    # Obtener aciertos y desaciertos para cada fecha ordenada
    aciertos = [aciertos_por_fecha[fecha] for fecha in fechas]
    desaciertos = [desaciertos_por_fecha[fecha] for fecha in fechas]
    # Gráfica de Curvas
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, aciertos, label='Aciertos')
    plt.plot(fechas, desaciertos, label='Desaciertos')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad')
    plt.title('Aciertos y Desaciertos en función de la Fecha')
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para evitar superposiciones
    plt.legend()
   
    curvas_img = BytesIO()
    plt.savefig(curvas_img, format='png')
    curvas_img.seek(0)
    curvas_base64 = base64.b64encode(curvas_img.getvalue()).decode('utf-8')
    plt.close()

    # Gráfica de Torta
    plt.figure(figsize=(5, 5))
    plt.pie([sum(aciertos), sum(desaciertos)], labels=['Aciertos', 'Desaciertos'], autopct='%1.1f%%')
    plt.title('Proporción de Aciertos y Desaciertos')
    torta_img = BytesIO()
    plt.savefig(torta_img, format='png')
    torta_img.seek(0)
    torta_base64 = base64.b64encode(torta_img.getvalue()).decode('utf-8')
    plt.close()

    return curvas_base64, torta_base64

import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas  #superficie para agregar contenido gráfico a un pdf
from reportlab.lib.utils import ImageReader
from flask import send_file

def generar_pdf(curvas_img, torta_img):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Dibujar títulos en el PDF
    c.drawString(100, 750, "Gráficas")
    c.drawString(100, 730, "Aciertos y Desaciertos en función de la Fecha")

    # Convertir BytesIO a ImageReader
    buffer_curvas = ImageReader(BytesIO(curvas_img))
    buffer_torta = ImageReader(BytesIO(torta_img))

    # Dibujar imágenes en el PDF
    c.drawImage(buffer_curvas, 100, 500, width=400, height=200)
    c.drawString(100, 300, "Proporción de Aciertos y Desaciertos")
    c.drawImage(buffer_torta, 100, 100, width=200, height=200)

    c.save()

    buffer.seek(0)

    # Guardar PDF en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(buffer.getvalue())
        pdf_path = tmp_file.name

    return pdf_path
