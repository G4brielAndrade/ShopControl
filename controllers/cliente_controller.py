from database.connection import Database

class ClienteController:
    def __init__(self):
        self.db = Database()

    def cadastrar_cliente(self, nome, cpf, email, telefone, endereco):
        query = "INSERT INTO clientes (nome, cpf, email, telefone, endereco) VALUES (%s, %s, %s, %s, %s)"
        params = (nome, cpf, email, telefone, endereco)
        return self.db.execute_query(query, params)

    def listar_clientes(self):
        query = "SELECT * FROM clientes"
        return self.db.fetch_all(query)

    def atualizar_cliente(self, id, nome, cpf, email, telefone, endereco):
        query = "UPDATE clientes SET nome=%s, cpf=%s, email=%s, telefone=%s, endereco=%s WHERE id=%s"
        params = (nome, cpf, email, telefone, endereco, id)
        return self.db.execute_query(query, params)

    def excluir_cliente(self, id):
        query = "DELETE FROM clientes WHERE id=%s"
        params = (id,)
        return self.db.execute_query(query, params)

    def buscar_cliente_por_id(self, id):
        query = "SELECT * FROM clientes WHERE id=%s"
        params = (id,)
        return self.db.fetch_one(query, params)
