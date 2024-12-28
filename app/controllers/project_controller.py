from app.models.project_model import ProjectModel

@staticmethod
def assign_project_by_result(id_huella, resultado):
    """
    Asigna un proyecto basado en el resultado de la huella de carbono.
    """
    try:
        print(f"ID Huella recibido: {id_huella}, Resultado: {resultado}")  # Log para depuración
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

        # Llamar al método para crear el proyecto
        ProjectModel.create_project(nombre, descripcion, estado, id_huella)
        print(f"Proyecto asignado: {nombre}, {descripcion}, {estado}, ID Huella: {id_huella}")
    except Exception as e:
        print(f"Error al asignar el proyecto: {e}")
        raise e
