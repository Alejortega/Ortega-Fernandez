# Aplicación secundaria
from flask import Flask, render_template, request, session

app = Flask(__name__)

@app.route('/check-answers', methods=['POST'])
def check_answers():
    user = request.form['user']
    num_preguntas = int(request.form['num_preguntas'])
    respuestas_usuario = [request.form[f'respuestas{i}'] for i in range(num_preguntas)]

    # Leer el archivo de preguntas y respuestas nuevamente para verificar las respuestas
    with open('frases_de_peliculas.txt', 'r') as file:
        preguntas_respuestas = [linea.strip().split(';') for linea in file.readlines()]

    # Comparar las respuestas del usuario con las respuestas correctas
    respuestas_correctas = [int(pregunta[-1]) for pregunta in preguntas_respuestas]
    puntaje = sum(1 for resp_user, resp_correcta in zip(respuestas_usuario, respuestas_correctas) if int(resp_user) == resp_correcta)

    return f'<h1>¡Hola, {user}!</h1><p>Tu puntaje es: {puntaje}/{num_preguntas}</p>'
