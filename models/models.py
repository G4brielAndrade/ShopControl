class Cliente:
    def __init__(self, id=None, nome=None, cpf=None, email=None, telefone=None, endereco=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

class Fornecedor:
    def __init__(self, id=None, nome=None, cnpj=None, email=None, telefone=None, endereco=None):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

class Produto:
    def __init__(self, id=None, nome=None, descricao=None, preco=0.0, estoque=0, fornecedor_id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.fornecedor_id = fornecedor_id

class Venda:
    def __init__(self, id=None, data_venda=None, cliente_id=None, produto_id=None, quantidade=0, preco_unitario=0.0):
        self.id = id
        self.data_venda = data_venda
        self.cliente_id = cliente_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

class Compra:
    def __init__(self, id=None, data_compra=None, fornecedor_id=None, produto_id=None, quantidade=0, preco_unitario=0.0):
        self.id = id
        self.data_compra = data_compra
        self.fornecedor_id = fornecedor_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
