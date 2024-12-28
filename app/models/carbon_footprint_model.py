from db_config import get_connection

class CarbonFootprintModel:
    @staticmethod
    def create_carbon_footprint(id_usuario, resultado):
        """
        Inserta una huella de carbono utilizando el procedimiento almacenado `sp_insert_carbon_footprint`.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc('sp_insert_carbon_footprint', (id_usuario, resultado))
            id_huella = cursor.fetchone()[0]  # Recupera el ID insertado
            conn.commit()
            return id_huella
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all_carbon_footprints():
        """
        Recupera todas las huellas de carbono de la base de datos.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(as_dict=True)
            query = """
                SELECT id_huella, id_usuario, fecha_calculo, resultado
                FROM Huella_Carbono
                ORDER BY fecha_calculo DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()




    @staticmethod
    def get_carbon_footprint_by_user(id_usuario):
        """
        Obtiene las huellas de carbono de un usuario utilizando el procedimiento `sp_get_carbon_footprints_by_user`.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(as_dict=True)
            cursor.callproc('sp_get_carbon_footprints_by_user', (id_usuario,))
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()
            
    @staticmethod
    def get_all_carbon_footprints():
        """
        Obtiene todas las huellas de carbono utilizando el procedimiento `sp_get_all_carbon_footprints`.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(as_dict=True)
            cursor.callproc('sp_get_all_carbon_footprints')
            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()