from database.connection import Database
from controllers.produto_controller import ProdutoController

class MovimentacaoController:
    def __init__(self):
        self.db = Database()
        self.produto_controller = ProdutoController()

    def registrar_venda(self, cliente_id, produto_id, quantidade, preco_unitario):
        # Verifica se há estoque suficiente
        produto = self.produto_controller.buscar_produto_por_id(produto_id)
        if produto and produto['estoque'] >= quantidade:
            query = "INSERT INTO vendas (cliente_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
            params = (cliente_id, produto_id, quantidade, preco_unitario)
            if self.db.execute_query(query, params):
                # Baixa no estoque
                return self.produto_controller.atualizar_estoque(produto_id, -quantidade)
        return False

    def registrar_compra(self, fornecedor_id, produto_id, quantidade, preco_unitario):
        query = "INSERT INTO compras (fornecedor_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
        params = (fornecedor_id, produto_id, quantidade, preco_unitario)
        if self.db.execute_query(query, params):
            # Aumento no estoque
            return self.produto_controller.atualizar_estoque(produto_id, quantidade)
        return False

    def listar_vendas(self):
        query = """
            SELECT v.*, c.nome as cliente_nome, p.nome as produto_nome 
            FROM vendas v 
            JOIN clientes c ON v.cliente_id = c.id 
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
        """
        return self.db.fetch_all(query)

    def listar_compras(self):
        query = """
            SELECT c.*, f.nome as fornecedor_nome, p.nome as produto_nome 
            FROM compras c 
            JOIN fornecedores f ON c.fornecedor_id = f.id 
            JOIN produtos p ON c.produto_id = p.id
            ORDER BY c.data_compra DESC
        """
        return self.db.fetch_all(query)

class FornecedorController:
    def __init__(self):
        self.db = Database()

    def cadastrar_fornecedor(self, nome, cnpj, email, telefone, endereco):
        query = "INSERT INTO fornecedores (nome, cnpj, email, telefone, endereco) VALUES (%s, %s, %s, %s, %s)"
        params = (nome, cnpj, email, telefone, endereco)
        return self.db.execute_query(query, params)

    def listar_fornecedores(self):
        query = "SELECT * FROM fornecedores"
        return self.db.fetch_all(query)

    def atualizar_fornecedor(self, id, nome, cnpj, email, telefone, endereco):
        query = "UPDATE fornecedores SET nome=%s, cnpj=%s, email=%s, telefone=%s, endereco=%s WHERE id=%s"
        params = (nome, cnpj, email, telefone, endereco, id)
        return self.db.execute_query(query, params)

    def excluir_fornecedor(self, id):
        query = "DELETE FROM fornecedores WHERE id=%s"
        params = (id,)
        return self.db.execute_query(query, params)
