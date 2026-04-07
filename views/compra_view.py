from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFormLayout, QComboBox)
from controllers.movimentacao_controller import MovimentacaoController, FornecedorController
from controllers.produto_controller import ProdutoController

class CompraView(QWidget):
    def __init__(self):
        super().__init__()
        self.mov_controller = MovimentacaoController()
        self.fornecedor_controller = FornecedorController()
        self.produto_controller = ProdutoController()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Registro de Compras (Entrada de Estoque)")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.combo_fornecedor = QComboBox()
        self.combo_produto = QComboBox()
        self.input_quantidade = QLineEdit()
        self.input_preco = QLineEdit()
        
        form_layout.addRow("Fornecedor:", self.combo_fornecedor)
        form_layout.addRow("Produto:", self.combo_produto)
        form_layout.addRow("Quantidade:", self.input_quantidade)
        form_layout.addRow("Preço de Custo:", self.input_preco)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_comprar = QPushButton("Registrar Compra")
        self.btn_limpar = QPushButton("Limpar")
        
        btn_layout.addWidget(self.btn_comprar)
        btn_layout.addWidget(self.btn_limpar)
        
        layout.addLayout(btn_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Data", "Fornecedor", "Produto", "Qtd", "Custo Total"])
        layout.addWidget(self.table)
        
        # Connect
        self.btn_comprar.clicked.connect(self.registrar_compra)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        
        self.carregar_dados()
        self.carregar_compras()

    def carregar_dados(self):
        fornecedores = self.fornecedor_controller.listar_fornecedores()
        self.combo_fornecedor.clear()
        for f in fornecedores:
            self.combo_fornecedor.addItem(f['nome'], f['id'])
            
        produtos = self.produto_controller.listar_produtos()
        self.combo_produto.clear()
        for p in produtos:
            self.combo_produto.addItem(f"{p['nome']} (Estoque Atual: {p['estoque']})", p['id'])

    def carregar_compras(self):
        compras = self.mov_controller.listar_compras()
        self.table.setRowCount(len(compras))
        for i, c in enumerate(compras):
            total = c['quantidade'] * c['preco_unitario']
            self.table.setItem(i, 0, QTableWidgetItem(str(c['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(c['data_compra'])))
            self.table.setItem(i, 2, QTableWidgetItem(c['fornecedor_nome']))
            self.table.setItem(i, 3, QTableWidgetItem(c['produto_nome']))
            self.table.setItem(i, 4, QTableWidgetItem(str(c['quantidade'])))
            self.table.setItem(i, 5, QTableWidgetItem(f"R$ {total:.2f}"))

    def registrar_compra(self):
        fornecedor_id = self.combo_fornecedor.currentData()
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
            
        if self.mov_controller.registrar_compra(fornecedor_id, produto_id, qtd, preco):
            QMessageBox.information(self, "Sucesso", "Compra registrada e estoque atualizado!")
            self.carregar_compras()
            self.carregar_dados()
            self.limpar_campos()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao registrar compra.")

    def limpar_campos(self):
        self.input_quantidade.clear()
        self.input_preco.clear()
