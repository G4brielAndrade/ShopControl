from database.connection import Database

class ProdutoController:
    def __init__(self):
        self.db = Database()

    def cadastrar_produto(self, nome, descricao, preco, estoque, fornecedor_id):
        query = "INSERT INTO produtos (nome, descricao, preco, estoque, fornecedor_id) VALUES (%s, %s, %s, %s, %s)"
        params = (nome, descricao, preco, estoque, fornecedor_id)
        return self.db.execute_query(query, params)

    def listar_produtos(self):
        query = "SELECT p.*, f.nome as fornecedor_nome FROM produtos p JOIN fornecedores f ON p.fornecedor_id = f.id"
        return self.db.fetch_all(query)

    def atualizar_produto(self, id, nome, descricao, preco, estoque, fornecedor_id):
        query = "UPDATE produtos SET nome=%s, descricao=%s, preco=%s, estoque=%s, fornecedor_id=%s WHERE id=%s"
        params = (nome, descricao, preco, estoque, fornecedor_id, id)
        return self.db.execute_query(query, params)

    def excluir_produto(self, id):
        query = "DELETE FROM produtos WHERE id=%s"
        params = (id,)
        return self.db.execute_query(query, params)

    def buscar_produto_por_id(self, id):
        query = "SELECT * FROM produtos WHERE id=%s"
        params = (id,)
        return self.db.fetch_one(query, params)

    def verificar_estoque_baixo(self, limite=5):
        query = "SELECT * FROM produtos WHERE estoque <= %s"
        params = (limite,)
        return self.db.fetch_all(query, params)

    def atualizar_estoque(self, id, quantidade):
        # quantidade pode ser positiva (compra) ou negativa (venda)
        query = "UPDATE produtos SET estoque = estoque + %s WHERE id=%s"
        params = (quantidade, id)
        return self.db.execute_query(query, params)
