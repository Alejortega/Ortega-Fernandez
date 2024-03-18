from flask import Flask, render_template, request, url_for, redirect
from modules.funciones import listar_peliculas, leer_archivo, obtener_frase_y_opciones
app = Flask(__name__)

@app.route("/")
def index():
    #return "¡Hola mundo!"
    return render_template("index.html")
 
@app.route('/listar_peliculas')
def listar():
    nombre_archivo = "docs/frases_de_peliculas.txt"  # nombre del archivo
    peliculas = leer_archivo(nombre_archivo)
    pelicula = listar_peliculas(peliculas)
    #peliculas = listar_peliculas() #leer_archivo('docs/frases_de_peliculas.txt')
    return render_template('listar_peliculas.html', pelicula=pelicula)



@app.route('/jugar', methods=['POST'])
def jugar():
    num_frases = int(request.form['num_frases'])
    nombre_usuario = request.form['nombre_usuario']
    # Aquí irá la lógica para jugar la trivia
    return "¡A jugar la trivia!"

@app.route('/iniciar_juego')
def iniciar_trivia():
    nombre_archivo = "docs/frases_de_peliculas.txt"  # nombre del archivo
    peliculas = leer_archivo(nombre_archivo)
    frase, opciones, pelicula_correcta = obtener_frase_y_opciones(peliculas)
    opciones = [opcion for opcion in opciones]

    return render_template('mostrar_frases.html', frase=frase, opciones=opciones)
    
""""
@app.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    nombre_archivo = "docs/frases_de_peliculas.txt"  # nombre del archivo
    peliculas = leer_archivo(nombre_archivo)
    frase, opciones, pelicula_correcta = obtener_frase_y_opciones(peliculas)
    respuesta_usuario = request.form['respuesta']
    respuesta_correcta = pelicula_correcta
    if respuesta_usuario == respuesta_correcta:
        mensaje = "¡Correcto!"
    else:
        mensaje = "Incorrecto. La respuesta correcta era: {}".format(respuesta_correcta)
    return render_template('resultados.html', mensaje=mensaje)
"""
@app.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    nombre_archivo = "docs/frases_de_peliculas.txt"  
    peliculas = leer_archivo(nombre_archivo)
    frase, opciones, respuesta_correcta = obtener_frase_y_opciones(peliculas)
    for i in range(len(opciones)):
        if respuesta_correcta == opciones[i]:
            respuesta_correct=opciones[i]

    respuesta_usuario = request.form['respuesta']
    print("Respuesta del usuario:", respuesta_usuario)
    print("Respuesta correcta:", respuesta_correct)
    print(opciones, frase)
    return redirect(url_for('respuesta_incorrecta', respuesta_correcta=respuesta_correct))

@app.route('/respuesta_correcta')
def respuesta_correcta():
    return render_template('respuesta_correcta.html')

@app.route('/respuesta_incorrecta/<respuesta_correcta>')
def respuesta_incorrecta(respuesta_correcta):
    return render_template('respuesta_incorrecta.html', respuesta_correcta=respuesta_correcta)
if __name__=="__main__":
    app.run(debug=True, port=5000)

