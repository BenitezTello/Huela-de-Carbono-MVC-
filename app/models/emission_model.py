from db_config import get_connection

class EmissionModel:
    @staticmethod
    def create_emission(datos, fecha_monitoreo, id_usuario, energia, transporte, recursos_naturales, residuos):
        """
        Inserta una nueva emisión utilizando el procedimiento almacenado `sp_insert_emission`.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc('sp_insert_emission', (datos, fecha_monitoreo, id_usuario, energia, transporte, recursos_naturales, residuos))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()