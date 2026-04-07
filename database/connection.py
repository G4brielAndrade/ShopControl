import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host='localhost', database='store_management_system', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        connection = self.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                connection.commit()
                return cursor
            except Error as e:
                print(f"Erro ao executar query: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None

    def fetch_all(self, query, params=None):
        connection = self.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Erro ao buscar dados: {e}")
                return []
            finally:
                cursor.close()
                self.close()
        return []

    def fetch_one(self, query, params=None):
        connection = self.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                result = cursor.fetchone()
                return result
            except Error as e:
                print(f"Erro ao buscar dado: {e}")
                return None
            finally:
                cursor.close()
                self.close()
        return None
