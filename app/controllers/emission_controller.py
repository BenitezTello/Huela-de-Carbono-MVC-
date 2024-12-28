from flask import request, redirect, url_for, flash, session, render_template
from app.models.emission_model import EmissionModel
from app.models.carbon_footprint_model import CarbonFootprintModel
from app.models.project_model import ProjectModel
from app.services.carbon_calculator import CarbonCalculator

class EmissionController:
    @staticmethod
    def save_emission():
        if 'username' not in session:
            flash('Debes iniciar sesión para registrar una emisión.', 'error')
            return redirect(url_for('user_routes.show_login_form'))

        try:
            # Recopilar los datos del formulario
            datos = request.form['datos']
            fecha_monitoreo = request.form['fecha_monitoreo']
            energia = float(request.form['energia'])
            transporte = float(request.form['transporte'])
            recursos_naturales = float(request.form['recursos_naturales'])
            residuos = float(request.form['residuos'])
            id_usuario = session.get('user_id')

            # Guardar las emisiones en la base de datos
            EmissionModel.create_emission(datos, fecha_monitoreo, id_usuario, energia, transporte, recursos_naturales, residuos)

            # Calcular la huella de carbono
            resultado = CarbonCalculator.calculate_carbon_footprint(energia, transporte, recursos_naturales, residuos)

            # Guardar el resultado de la huella de carbono en la base de datos
            id_huella = CarbonFootprintModel.create_carbon_footprint(id_usuario, resultado)

            # Asignar un proyecto basado en el resultado
            proyecto = EmissionController.assign_project_by_result(id_huella, resultado)

            flash(f'Emisión registrada con éxito. Proyecto asignado: {proyecto["nombre"]}', 'success')
            return redirect(url_for('user_routes.show_carbon_footprint'))
        except Exception as e:
            flash(f'Error al registrar la emisión: {e}', 'error')
            return redirect(url_for('user_routes.show_emission_form'))

    @staticmethod
    def assign_project_by_result(id_huella, resultado):
        """
        Asigna un proyecto basado en el resultado de la huella de carbono.
        """
        try:
            print(f"Asignando proyecto para ID Huella: {id_huella}, Resultado: {resultado}")
            if resultado <= 50:
                nombre = "Conservación Energética"
                descripcion = "Implementa medidas de eficiencia energética en tu hogar."
                estado = "Bajo"
            elif 51 <= resultado <= 100:
                nombre = "Reducción de Transporte"
                descripcion = "Promueve el uso de transporte sostenible como bicicletas o transporte público."
                estado = "Medio"
            else:
                nombre = "Reforestación Urbana"
                descripcion = "Participa en iniciativas de reforestación y captura de carbono."
                estado = "Alto"

            # Crear y asignar el proyecto
            ProjectModel.create_project(nombre, descripcion, estado, id_huella)
            print(f"Proyecto asignado correctamente: {nombre}, Estado: {estado}, ID Huella: {id_huella}")
            return {"nombre": nombre, "descripcion": descripcion, "estado": estado}
        except Exception as e:
            print(f"Error al asignar el proyecto: {e}")
            raise e

    @staticmethod
    def get_carbon_footprint():
        if 'username' not in session:
            flash('Debes iniciar sesión para ver tu huella de carbono.', 'error')
            return redirect(url_for('user_routes.show_login_form'))

        try:
            id_usuario = session.get('user_id')
            role = session.get('role', 'user')

            if role == 'admin':
                carbon_footprints = CarbonFootprintModel.get_all_carbon_footprints()
            else:
                carbon_footprints = CarbonFootprintModel.get_carbon_footprint_by_user(id_usuario)

            if not carbon_footprints:
                flash('No se encontraron registros de huella de carbono.', 'info')
                return redirect(url_for('home'))

            return render_template('carbon_footprint.html', carbon_footprints=carbon_footprints, role=role)
        except Exception as e:
            flash(f'Error al obtener la huella de carbono: {e}', 'error')
            return redirect(url_for('home'))
