from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from database import Database
from flask_bcrypt import Bcrypt
from qr_generator import QRGenerator  # Asegúrate de importar QRGenerator

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura
bcrypt = Bcrypt(app)

# Ruta de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
        except KeyError as e:
            flash(f"Falta el campo {e}", "danger")
            return redirect(url_for('login'))

        db = Database()
        user = db.validate_login(username, password)
        db.close()

        if user:
            session['user_id'] = user['id']
            flash('Login exitoso.', 'success')
            return redirect(url_for('show_personnel'))
        else:
            flash('Credenciales inválidas.', 'danger')

    return render_template('login.html')

# Ruta para mostrar tarjetas de personal
@app.route('/personnel')
def show_personnel():
    db = Database()
    personnel = db.fetch_personnel()
    db.close()
    return render_template('show_personnel.html', personnel=personnel)

# Ruta para generar QR
@app.route('/generate_qr/<int:id>')
def generate_qr(id):
    db = Database()
    person = db.get_person_by_id(id)
    db.close()

    if person:
        qr_code = QRGenerator.generate_qr(f'http://localhost:5000/scan_qr/{id}')
        return render_template('show_qr.html', person=person, qr_code=qr_code)
    else:
        flash('Personal no encontrado.', 'danger')
        return redirect(url_for('show_personnel'))

# Ruta para escanear QR y actualizar estado
@app.route('/scan_qr/<int:id>', methods=['GET'])
def scan_qr(id):
    db = Database()
    person = db.get_person_by_id(id)

    if person:
        # Alternar estado entre 'activo' e 'inactivo'
        new_status = 'activo' if person['status'] == 'inactivo' else 'inactivo'
        db.update_person_status(id, new_status)
        db.close()

        # Devolver los datos del personal en formato JSON
        return jsonify({
            'name': person['name'],
            'status': new_status,
            'photo': person['photo'] if person['photo'] else None
        })
    else:
        db.close()
        return jsonify({'error': 'Personal no encontrado'}), 404

# Ruta para mostrar el stock de productos
@app.route('/stock')
def show_stock():
    db = Database()
    stock = db.fetch_stock()
    db.close()
    return render_template('show_stock.html', stock=stock)

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
