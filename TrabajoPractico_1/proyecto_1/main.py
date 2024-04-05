from flask import render_template, request, session, redirect, url_for, send_file
from datetime import datetime
from modules.funciones import listar_peliculas, leer_archivo, guardar_datos_en_archivo, cargar_frases_y_peliculas, verificar_respuesta, leer_archivo_de_resultados, generar_graficas, generar_pdf
import base64 #imágenes a este formato para su intrucción en pfd o html
from modules.config import app
#session: almacenar información específica del usuario 
RUTA = "./docs/"
ARCHIVO = RUTA + 'resultados_historicos.txt'

# (app.route) Que función se va a visualizar al acceder a una determinada ruta 
@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        
        Usuario = request.form['Usuario']  # Obtener el nombre de usuario del formulario
        session['Usuario'] = Usuario # Guardar el nombre de usuario en la sesión
        return redirect(url_for('process_form')) #Rederigir al procesamiento del formulario
    
    return render_template('index.html')

@app.route('/process-form', methods=['GET','POST'])
def process_form():

    if request.method == 'POST':
        num_frases = int(request.form['num_frases'])
        Usuario = request.form['Usuario']
        session['usuario'] = Usuario
        tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session['tiempo'] = tiempo
        session['num_frasess'] = num_frases

        if num_frases < 3:
            return 'Debes ingresar al menos 3 preguntas.'
        
       
    archi="docs/frases_de_peliculas.txt" #archivo que contiene las frases y peliculas
    
    frases_seleccionadas, opciones = cargar_frases_y_peliculas(num_frases, archi)
 
    # Guardar las preguntas y respuestas en la sesión
    session['frases'] = frases_seleccionadas  # Solo las preguntas, sin las opciones
    session['opciones'] = opciones  # Lista de opciones para cada pregunta
    session['indice_seleccionado'] = 0  # Índice de la primera pregunta
    session['contador_correctas'] = 0  # Contador de respuestas correctas


    # Mostrar la primera pregunta al usuario
    return render_template('frases.html', frases=session['frases'][session['indice_seleccionado']], opciones=opciones[session['indice_seleccionado']], Usuario=Usuario)
    
@app.route('/check-respuesta', methods=['POST'])
def check_answer():
    
    respuesta_del_usuario = request.form.get('respuesta')  # Obtener la respuesta seleccionada por el usuario
    respuesta_correcta = session['frases'][session['indice_seleccionado']][1]  # Respuesta correcta de la pregunta actual

 # Verificar si la respuesta del usuario es correcta a través de una función y retornar un mensaje
    mensaje = verificar_respuesta(respuesta_del_usuario, respuesta_correcta)
    if mensaje == '¡Respuesta correcta!':
        session['contador_correctas'] += 1
        session['correctas_totales'] = session.get('correctas_totales',0) +1 #Incrementa los aciertos totales
    
    # Incrementar el índice para pasar a la siguiente pregunta
    session['indice_seleccionado'] += 1

    # Verificar si el usuario ha respondido todas las preguntas
    if session['indice_seleccionado'] == len(session['frases']):
        #Calcular los aciertos totales al final de todas las preguntas
        session['correctas_totales'] = session['contador_correctas']
    
    aciertos_actual = f"{session['correctas_totales']}/{session['num_frasess']}"
    session['aciertos'] = aciertos_actual 
    #Si el usuario ha respondido todas las preguntas, guardar los datos finales en el archivo
    if session['indice_seleccionado'] == len(session['frases']):
        guardar_datos_en_archivo(ARCHIVO, session['usuario'], session['aciertos'], session['tiempo'], session['correctas_totales'])
    # Verificar si el usuario ha respondido menos de 1 pregunta
    if session['indice_seleccionado'] < 1:
        # Mostrar si la respuesta fue correcta o incorrecta y redirigir al inicio
        return render_template('frases.html', frases=session['frases'][0], opciones=session['frases'][0][1:], message=mensaje)
    elif session['indice_seleccionado'] < len(session['frases']):
        # Mostrar la siguiente pregunta
        return render_template('frases.html', frases=session['frases'][session['indice_seleccionado']], opciones=session['opciones'][session['indice_seleccionado']], message=mensaje)
    else:
       return render_template('resultado.html',message=mensaje) 

    
@app.route('/resultados')
def mostrar_resultados():
    resultados = leer_archivo_de_resultados(ARCHIVO) 
    return render_template('resultados_hist.html', resultados=resultados)  


@app.route('/mostrar_graficas')
def mostrar_graficas():
    num_total_preguntas = int(session['num_frasess'])
    curvas_base64, torta_base64 = generar_graficas(ARCHIVO, num_total_preguntas )
    
    global curvas_img, torta_img
    curvas_img = base64.b64decode(curvas_base64.encode('utf-8'))
    torta_img = base64.b64decode(torta_base64.encode('utf-8'))
    
    return render_template('graficas.html', curvas_img=curvas_base64, torta_img=torta_base64)


@app.route('/descargar_pdf', methods=['POST'])
def descargar_pdf():

    global curvas_img, torta_img
    pdf = generar_pdf(curvas_img, torta_img)
    
    return send_file(pdf, as_attachment=True)


@app.route('/listar_peliculas')
def listar():
    nombre_archivo = "docs/frases_de_peliculas.txt"  # nombre del archivo
    peliculas = leer_archivo(nombre_archivo)
    pelicula = listar_peliculas(peliculas)
    return render_template('listar_peliculas.html', pelicula=pelicula)


if __name__ == '__main__':
    app.run(debug=True)





