"""
Aqui solo administra las rutas que son mas importantes
"""
from flask import Flask, render_template
from app.controllers.routes import user_routes

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configura la clave secreta para las sesiones
app.config['SECRET_KEY'] = 'src_password'

# Registra el blueprint de las rutas de usuario
app.register_blueprint(user_routes)

@app.route('/home')
def home():
    return render_template('home.html')

#@app.route('/admin')
#def admin():
#    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)