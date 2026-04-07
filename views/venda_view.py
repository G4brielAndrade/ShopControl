from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFormLayout, QComboBox)
from controllers.movimentacao_controller import MovimentacaoController
from controllers.cliente_controller import ClienteController
from controllers.produto_controller import ProdutoController

class VendaView(QWidget):
    def __init__(self):
        super().__init__()
        self.mov_controller = MovimentacaoController()
        self.cliente_controller = ClienteController()
        self.produto_controller = ProdutoController()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Registro de Vendas")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.combo_cliente = QComboBox()
        self.combo_produto = QComboBox()
        self.input_quantidade = QLineEdit()
        self.input_preco = QLineEdit()
        
        form_layout.addRow("Cliente:", self.combo_cliente)
        form_layout.addRow("Produto:", self.combo_produto)
        form_layout.addRow("Quantidade:", self.input_quantidade)
        form_layout.addRow("Preço Unitário:", self.input_preco)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_vender = QPushButton("Registrar Venda")
        self.btn_limpar = QPushButton("Limpar")
        
        btn_layout.addWidget(self.btn_vender)
        btn_layout.addWidget(self.btn_limpar)
        
        layout.addLayout(btn_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Data", "Cliente", "Produto", "Qtd", "Total"])
        layout.addWidget(self.table)
        
        # Connect
        self.btn_vender.clicked.connect(self.registrar_venda)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.combo_produto.currentIndexChanged.connect(self.atualizar_preco_sugerido)
        
        self.carregar_dados()
        self.carregar_vendas()

    def carregar_dados(self):
        clientes = self.cliente_controller.listar_clientes()
        self.combo_cliente.clear()
        for c in clientes:
            self.combo_cliente.addItem(c['nome'], c['id'])
            
        produtos = self.produto_controller.listar_produtos()
        self.combo_produto.clear()
        for p in produtos:
            self.combo_produto.addItem(f"{p['nome']} (Estoque: {p['estoque']})", p['id'])

    def carregar_vendas(self):
        vendas = self.mov_controller.listar_vendas()
        self.table.setRowCount(len(vendas))
        for i, v in enumerate(vendas):
            total = v['quantidade'] * v['preco_unitario']
            self.table.setItem(i, 0, QTableWidgetItem(str(v['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(v['data_venda'])))
            self.table.setItem(i, 2, QTableWidgetItem(v['cliente_nome']))
            self.table.setItem(i, 3, QTableWidgetItem(v['produto_nome']))
            self.table.setItem(i, 4, QTableWidgetItem(str(v['quantidade'])))
            self.table.setItem(i, 5, QTableWidgetItem(f"R$ {total:.2f}"))

    def atualizar_preco_sugerido(self):
        produto_id = self.combo_produto.currentData()
        if produto_id:
            produto = self.produto_controller.buscar_produto_por_id(produto_id)
            if produto:
                self.input_preco.setText(str(produto['preco']))

    def registrar_venda(self):
        cliente_id = self.combo_cliente.currentData()
        produto_id = self.combo_produto.currentData()
        qtd = self.input_quantidade.text()
        preco = self.input_preco.text()
        
        if not qtd or not preco:
            QMessageBox.warning(self, "Aviso", "Preencha quantidade e preço!")
            return
            
        try:
            qtd = int(qtd)
            preco = float(preco)
        except ValueError:
            QMessageBox.warning(self, "Aviso", "Valores inválidos!")
            return
            
        if self.mov_controller.registrar_venda(cliente_id, produto_id, qtd, preco):
            QMessageBox.information(self, "Sucesso", "Venda realizada com sucesso!")
            self.carregar_vendas()
            self.carregar_dados() # Atualiza estoque no combo
            self.limpar_campos()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao realizar venda. Verifique o estoque!")

    def limpar_campos(self):
        self.input_quantidade.clear()
        self.input_preco.clear()
