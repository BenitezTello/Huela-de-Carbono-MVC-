from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.controllers.user_controller import UserController
from app.controllers.emission_controller import EmissionController
from app.models.project_model import ProjectModel
from app.models.carbon_footprint_model import CarbonFootprintModel

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

@user_routes.route('/register', methods=['POST'])
def register():
    return UserController.register()

@user_routes.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')

@user_routes.route('/login', methods=['POST'])
def login():
    return UserController.login()

@user_routes.route('/emission', methods=['GET'])
def show_emission_form():
    # Verifica que el usuario esté autenticado
    if 'user_id' not in session:
        flash('Debes iniciar sesión para registrar emisiones.', 'error')
        return redirect(url_for('user_routes.show_login_form'))
    return render_template('emission_form.html')

@user_routes.route('/emission', methods=['POST'])
def save_emission():
    return EmissionController.save_emission()

@user_routes.route('/carbon-footprint', methods=['GET'])
def show_carbon_footprint():
    # Verifica que el usuario esté autenticado
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver tu huella de carbono.', 'error')
        return redirect(url_for('user_routes.show_login_form'))
    return EmissionController.get_carbon_footprint()

@user_routes.route('/project/<int:id_huella>', methods=['GET'])
def show_project(id_huella):
    """
    Muestra el proyecto asignado a una huella de carbono específica.
    """
    try:
        # Verifica que el usuario esté autenticado
        if 'user_id' not in session:
            flash('Debes iniciar sesión para ver los proyectos.', 'error')
            return redirect(url_for('user_routes.show_login_form'))
        
        project = ProjectModel.get_project_by_huella(id_huella)
        if not project:
            flash('No se encontró ningún proyecto asociado.', 'info')
            return redirect(url_for('user_routes.show_carbon_footprint'))
        return render_template('project.html', project=project)
    except Exception as e:
        flash(f'Error al cargar el proyecto: {e}', 'error')
        return redirect(url_for('user_routes.show_carbon_footprint'))

@user_routes.route('/admin-dashboard', methods=['GET'])
def admin_dashboard():
    """
    Vista exclusiva para administradores.
    """
    if 'role' not in session or session.get('role') != 'admin':
        flash('Acceso denegado. Solo los administradores pueden acceder a esta página.', 'error')
        return redirect(url_for('home'))

    try:
        # Carga todas las huellas de carbono para el panel de administración
        carbon_footprints = CarbonFootprintModel.get_all_carbon_footprints()
        return render_template('admin_dashboard.html', carbon_footprints=carbon_footprints)
    except Exception as e:
        flash(f'Error al cargar el panel de administrador: {e}', 'error')
        return redirect(url_for('home'))

@user_routes.route('/admin', methods=['GET'])
def admin():
    if 'role' in session and session.get('role') == 'admin':
        return redirect(url_for('user_routes.admin_dashboard'))
    else:
        flash('Acceso denegado.', 'error')
        return redirect(url_for('home'))
