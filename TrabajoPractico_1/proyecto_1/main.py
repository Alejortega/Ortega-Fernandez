from flask import Flask, render_template, request, session
import random
from modules.funciones import listar_peliculas, leer_archivo 

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

SESSION_TYPE= "filesysystem"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-form', methods=['POST'])
def process_form():
    num_questions = int(request.form['num_questions'])
    user = request.form['user']

    # Abrir el archivo que contiene las frases y respuestas
    with open('frases_de_peliculas.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Separar las frases y respuestas en listas separadas
    frases = []
    respuestas = []
    for line in lines:
        pregunta, respuesta = line.strip().split(';')
        frases.append(pregunta)
        respuestas.append(respuesta)

    # Verificar que haya suficientes preguntas en el archivo
    if len(frases) < num_questions:
        return 'El archivo no contiene suficientes frases para la cantidad solicitada.'

    # Seleccionar un número aleatorio de índices de preguntas para mostrar al usuario
    selected_indices = random.sample(range(len(frases)), num_questions)
    selected_questions = [(frases[i], respuestas[i]) for i in selected_indices]

    # Generar opciones para cada pregunta
    options = []
    for pregunta, respuesta in selected_questions:
        # Opción correcta
        correct_option = respuesta

        # Opciones falsas aleatorias
        all_options = respuestas[:]  # Copia la lista de respuestas
        all_options.remove(correct_option)  # Elimina la respuesta correcta
        incorrect_options = random.sample(all_options, 2)  # Elige dos respuestas falsas aleatorias

        # Agregar las opciones al listado final
        options.append((pregunta, correct_option, incorrect_options))

    # Guardar las preguntas y respuestas en la sesión
    session['questions'] = options
    session['current_index'] = 0  # Índice de la primera pregunta
    session['correct_count'] = 0  # Contador de respuestas correctas
    session['answered_correctly'] = False  # Indica si se respondió correctamente

    return render_template('questions.html', options=options, user=user)

@app.route('/check-answer', methods=['POST'])
def check_answer():
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']

    if user_answer == correct_answer:
        message = '¡Respuesta correcta!'
        session['correct_count'] += 1
        session['answered_correctly'] = True
    else:
        message = f'Respuesta incorrecta. La respuesta correcta es: {correct_answer}'
        session['answered_correctly'] = False

    session['current_index'] += 1  # Pasar a la siguiente pregunta

    return render_template('result.html', message=message)

@app.route('/listar_peliculas')
def listar():
    nombre_archivo = "frases_de_peliculas.txt"  # nombre del archivo
    peliculas = leer_archivo(nombre_archivo)
    pelicula = listar_peliculas(peliculas)
    #peliculas = listar_peliculas() #leer_archivo('docs/frases_de_peliculas.txt')
    return render_template('listar_peliculas.html', pelicula=pelicula)


if __name__ == '__main__':
    app.run(debug=True)




