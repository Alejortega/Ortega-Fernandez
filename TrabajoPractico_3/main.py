#importaciones de clases
from modules.config import app, db
from modules.gestores import *
from modules.gestores import GestorDB, GestorDeReclamos
from modules.coordinador_usuario import Coordinador_usuario
from modules.coordinador_jefe import Coordinador_jefe  

#otras importaciones importantes
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from io import BytesIO
import os

#instancias gestores
gestorR = GestorDeReclamos('./data/clasificador_svm.pkl')
gestordb = GestorDB(db)
#instancias coordinadores
coordinador_usuario = Coordinador_usuario(gestordb)  
coordinador_jefe = Coordinador_jefe()

#configuración del LoginManager (preguntar si va en el config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Clase User para Flask-Login
class User(UserMixin, PersonaDB):
    pass

#Configuración Flask Login
#Cargador de usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Desarrollo main:

#ruta para el registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repeated_password = request.form['repeated_password']
        claustro = request.form['claustro']

        
        if password != repeated_password:
            flash('Las contraseñas no coinciden, inténtalo de nuevo', 'error')
            return redirect(url_for('register'))

        #datos del usuario
        usuario_data = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'username': username,
            'password': password,
            'claustro': claustro
        }

        #Se prueba si se cumplen lso requisitos de validación de datos
        resultado = coordinador_usuario.cargar_usuario(usuario_data)

        #si el resultado es una lista, hay errores, por lo tanto se retornan los errores
        if isinstance(resultado, list):
            for error in resultado:
                flash(error, 'error')
            return redirect(url_for('register'))
        else: #si no los hay, se guarda en db el nuevo user
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

#inicio de sesión, tanto para jefes como para usuarios comunes

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                if user.departamento :  #Verifica si el usuario tiene un departamento asignado, si lo tiene es jefe
                    return redirect(url_for('jefe', departamento=user.departamento)) # a la ruta 'jefe' con el parámetro 'departamento'
                else:
                    return redirect(url_for('inicio'))  #a la template usuarios comunes
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no registrado', 'error')

    return render_template('login.html')

#Ruta para el inicio de usuarios comunes
@app.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html', name=current_user.username)

#Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#vistas de usuarios comunes 

@app.route('/crear_reclamo', methods=['GET', 'POST'])
@login_required
def crear_reclamo():
    if request.method == 'POST':
        contenido = request.form['contenido']
        foto = request.form.get('foto') if 'foto' in request.form else None
        fecha_hora = datetime.utcnow()
        user_id = current_user.id 

        #usar¿mos el coordinador_usuario para iniciar el reclamo
        reclamos_similares = coordinador_usuario.iniciar_reclamo(user_id, contenido, fecha_hora, foto)

        if reclamos_similares:
            #si se encontraron reclamos similares, redirigir a una plantilla para que el usuario pueda adherirse a algún reclamo ya realizado
            return render_template('reclamos_similares.html', reclamos_similares=reclamos_similares)
        else: #si no se encontraron reclamos simiares, se guarda el reclamo en la db
            flash('Reclamo creado con éxito.')
            return redirect(url_for('inicio'))
    
    return render_template('crear_reclamo.html')


@app.route('/adherir_reclamo', methods=['POST'])
@login_required
def adherir_reclamo():
    reclamo_id = request.form['reclamo_id']
    coordinador_usuario.mostrar_al_usuario(accion="adherirse", valor=reclamo_id)  
    flash('Adherido a reclamo existente', 'success')
    return redirect(url_for('inicio'))
    

#Ruta para listar todos los reclamos de la db
@app.route('/listar_reclamos', methods=['GET'])
@login_required
def listar_reclamos():
    reclamos = coordinador_usuario.mostrar_al_usuario(accion="listar_reclamos",valor=None)  
    return render_template('listar_reclamos.html', reclamos=reclamos)

#Ruta para ver los reclamos del usuario
@app.route('/mis_reclamos', methods=['GET'])
@login_required
def mis_reclamos():
    reclamos_usuario = coordinador_usuario.mostrar_al_usuario(accion="mis_reclamos", valor=current_user.id)  
    return render_template('mis_reclamos.html', reclamos=reclamos_usuario)

#vistas jefes
@app.route('/jefe/<departamento>')
def jefe(departamento):
    reclamos = coordinador_jefe.mostrar_al_jefe(valor=departamento)  
    return render_template('jefe.html', reclamos=reclamos, departamento=departamento)

#a partir de acá empezar a cambiar

@app.route('/analitica/<departamento>', methods=['GET', 'POST'])
def analitica(departamento):

    medianas=coordinador_jefe.crear_analitica(valor=departamento)
    mediana_proceso=medianas[1]
    mediana_resueltos=medianas[0]

    if request.method == 'POST':
        formato = request.form.get('formato')
        depto=departamento
    
        if formato == 'pdf':
                coordinador_jefe.generar_reporte(valor="pdf", medianas=medianas, depto=depto)
                pdf_path = os.path.join(os.getcwd(), 'static', 'reporte.pdf')
                return send_file(pdf_path, as_attachment=True, download_name='reporte.pdf')
        elif formato == 'html':
                coordinador_jefe.generar_reporte(valor="html", medianas=medianas, depto=depto)
                html_path = os.path.join(os.getcwd(), 'static', 'reporte.html')
                return send_file(html_path, as_attachment=True, download_name='reporte.html')
        else:
                return redirect(url_for('analitica', departamento=departamento))
    # Renderizar la plantilla analitica.html con los datos necesarios
    return render_template('analitica.html', departamento=departamento, mediana_en_proceso=mediana_proceso,
                           mediana_resuelto=mediana_resueltos)




@app.route('/ayuda/<departamento>')
def mostrar_video(departamento):
    return render_template('ayuda.html', departamento=departamento)

#modificar
@app.route('/manejar_reclamos/<departamento>', methods=['GET', 'POST'])
@login_required
def manejar_reclamos(departamento):
    if request.method == 'POST':
        reclamo_id = request.form.get('reclamo_id')
        accion = request.form.get('accion')
        
        if accion == 'cambiar_estado':
            nuevo_estado = request.form.get('estado')
            tiempo_resolucion = request.form.get('tiempo_resolucion')
            
            #Verifica si el tiempo de resolución es válido, esto de acá capas esta de más, se tendría que hacer en otro lado?:
            if tiempo_resolucion:
                try:
                    tiempo_resolucion = int(tiempo_resolucion)
                    if tiempo_resolucion < 1 or tiempo_resolucion > 15:
                        raise ValueError
                except ValueError:
                    flash('El tiempo de resolución debe estar entre 1 y 15 días.', 'error')
                    return redirect(url_for('manejar_reclamos', departamento=departamento))
            
            #Cambiar el estado del reclamo utilizando el GestorDB
            coordinador_jefe.cambiar_estado_reclamo(reclamo_id, nuevo_estado, tiempo_resolucion)
            flash('Estado del reclamo actualizado correctamente.', 'success')
        
    
    reclamos = coordinador_jefe.mostrar_al_jefe(departamento)

 
    # Renderiza el template con el formulario y demás contenido
    return render_template('manejar_reclamos.html', departamento=departamento, reclamos=reclamos)

@app.route('/derivar_reclamo', methods=['POST'])
def derivar_reclamo():
    reclamo_id = request.form['reclamo_id']
    departamento_destino = request.form['departamento_destino']
   
    coordinador_jefe.derivar_reclamo(reclamo_id, departamento_destino)  # Llamar al método derivar_reclamo
    # Redirigir a la página de manejar reclamos con un mensaje de éxito
    return redirect(url_for('manejar_reclamos', departamento=current_user.departamento))

#Ejecución de la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

