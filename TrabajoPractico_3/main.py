from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from modules.config import app, db
from modules.usuario import Usuario
from modules.reclamo import Reclamo
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from modules.gestor_datos import Gestor
# Configurar la sesión para que sea permanente y establecer su tiempo de vida
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Crear tablas en la base de datos
with app.app_context(): 
    db.create_all()

# Configuración de la carpeta de carga de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)




# Ruta para el inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return redirect(url_for('login'))
    return render_template('iniciarsesion.html')

# Ruta para verificar las credenciales de inicio de sesión
@app.route('/verificar_credenciales', methods=['POST'])
def verificar_credenciales():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = Usuario.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({'valid': True}), 200
    return jsonify({'valid': False}), 200

# Ruta para verificar si el correo electrónico está en uso
@app.route('/verificar_email', methods=['POST'])
def verificar_email():
    email = request.json['email']
    user = Usuario.query.filter_by(email=email).first()
    if user:
        return jsonify({'used': True}), 200
    return jsonify({'used': False}), 200
gestor = Gestor()
# Ruta para el registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        username = request.form['username']
        claustro = request.form['claustro']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        if password != password_repeat:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('register'))

        # Verificar si el email ya está en uso
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está en uso', 'error')
            return redirect(url_for('register'))

        # Verificar si el nombre de usuario ya está en uso
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'error')
            return redirect(url_for('register'))

        # Crear un nuevo usuario y guardarlo en la base de datos
        
        gestor.guardar_user({'nombre': nombre, 'apellido': apellido, 'email': email, 'username': username, 'password': password,'claustro': claustro })
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

# Ruta para el panel de usuario
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Ruta para crear un reclamo
@app.route('/crear_reclamo', methods=['GET', 'POST'])
def crear_reclamo():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        contenido = request.form['contenido']
        user_id = session['user_id']
        foto = None

        if 'foto' in request.files:
            file = request.files['foto']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                foto = filename

        # Creamos un diccionario con los datos del reclamo
        reclamo_data = {
            'contenido': contenido,
            'user_id': user_id,
            'foto': foto
        }

        # Guardamos el reclamo usando el gestor
        gestor.guardar_reclamo(reclamo_data)
        
        flash('Reclamo creado exitosamente', 'success')
        return redirect(url_for('dashboard'))

    return render_template('crear_reclamo.html')

# Ruta para listar reclamos
@app.route('/listar_reclamos', methods=['GET'])
def listar_reclamos():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('login'))

    departamento_filtro = request.args.get('departamento')
    if departamento_filtro:
        reclamos = Reclamo.query.filter_by(departamento=departamento_filtro).all()
    else:
        reclamos = Reclamo.query.all()

    return render_template('listar_reclamos.html', reclamos=reclamos)

# Ruta para adherirse a un reclamo
@app.route('/adherirse_reclamo/<int:id>', methods=['POST'])
def adherirse_reclamo(id):
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('login'))

    reclamo = Reclamo.query.get(id)
    if reclamo:
        reclamo.adherentes += 1
        db.session.commit()
        flash('Te has adherido al reclamo exitosamente', 'success')
    else:
        flash('Reclamo no encontrado', 'error')

    return redirect(url_for('listar_reclamos'))

# Ruta para ver los reclamos del usuario
@app.route('/mis_reclamos')
def mis_reclamos():
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    reclamos_usuario = Reclamo.query.filter_by(user_id=user_id).all()
    
    return render_template('mis_reclamos.html', reclamos=reclamos_usuario)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

# Ejecución de la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
