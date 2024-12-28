from db_config import get_connection

class ProjectModel:
    @staticmethod
    def create_project(nombre, descripcion, estado, id_huella):
        """
        Asigna un proyecto utilizando el procedimiento almacenado `sp_assign_project`.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc('sp_assign_project', (id_huella, nombre, descripcion, estado))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def create_project_by_result(id_huella, resultado):
        """
        Asigna un proyecto basado en el resultado de la huella de carbono.
        """
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

        # Llama a la función para crear el proyecto
        ProjectModel.create_project(nombre, descripcion, estado, id_huella)

    @staticmethod
    def get_project_by_huella(id_huella):
        """
        Obtiene el proyecto asociado a una huella de carbono específica.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(as_dict=True)
            query = """
                SELECT id_proyecto, nombre, descripcion, estado, id_huella
                FROM Proyectos
                WHERE id_huella = %s
            """
            cursor.execute(query, (id_huella,))
            project = cursor.fetchone()
            return project
        except Exception as e:
            print(f"Error al obtener proyecto: {e}")
            raise e
        finally:
            conn.close()
