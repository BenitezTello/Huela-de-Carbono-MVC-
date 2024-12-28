from flask import request, jsonify, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user_model import UserModel

class UserController:
    @staticmethod
    def register():
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = 'user' 

        if not username or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            UserModel.create_user(username, email, hashed_password, role)
            flash('User successfully registered!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Error registering user', 'error')
            return jsonify({'message': 'Error registering user', 'error': str(e)}), 500

from flask import request, jsonify, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user_model import UserModel

class UserController:
    @staticmethod
    def login():
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            flash('Debes ingresar el usuario y la contraseña.', 'error')
            return redirect(url_for('user_routes.show_login_form'))

        try:
            user = UserModel.get_user_by_username(username)
            if user and check_password_hash(user['password_hash'], password):
                # Guardar los datos en la sesión
                session['username'] = user['username']
                session['user_id'] = user['id']
                session['role'] = user['role']
                
                flash('Inicio de sesión exitoso.', 'success')
                # Redirigir dependiendo del rol del usuario
                if user['role'] == 'admin':
                    return redirect(url_for('user_routes.admin_dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                flash('Usuario o contraseña incorrectos.', 'error')
                return redirect(url_for('user_routes.show_login_form'))
        except Exception as e:
            flash(f'Error al iniciar sesión: {e}', 'error')
            return redirect(url_for('user_routes.show_login_form'))
