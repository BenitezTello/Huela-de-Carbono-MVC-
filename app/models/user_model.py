from db_config import get_connection

class UserModel:
    @staticmethod
    def create_user(username, email, password_hash, role):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, email, password_hash, role))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_user_by_username(username):
        try:
            conn = get_connection()
            cursor = conn.cursor(as_dict=True)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_user_by_role(role):
        try:
            conn = get_connection()
            cursor = conn.cursor(as_dict=True)
            query = "SELECT * FROM users WHERE role = %s"
            cursor.execute(query, (role,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            raise e
        finally:
            conn.close()
