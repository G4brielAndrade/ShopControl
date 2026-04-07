from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFormLayout, QComboBox)
from controllers.produto_controller import ProdutoController
from controllers.movimentacao_controller import FornecedorController

class ProdutoView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ProdutoController()
        self.fornecedor_controller = FornecedorController()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Gestão de Produtos")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.input_nome = QLineEdit()
        self.input_desc = QLineEdit()
        self.input_preco = QLineEdit()
        self.input_estoque = QLineEdit()
        self.combo_fornecedor = QComboBox()
        
        form_layout.addRow("Nome:", self.input_nome)
        form_layout.addRow("Descrição:", self.input_desc)
        form_layout.addRow("Preço:", self.input_preco)
        form_layout.addRow("Estoque Inicial:", self.input_estoque)
        form_layout.addRow("Fornecedor:", self.combo_fornecedor)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_salvar = QPushButton("Salvar")
        self.btn_limpar = QPushButton("Limpar")
        self.btn_excluir = QPushButton("Excluir Selecionado")
        
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_limpar)
        btn_layout.addWidget(self.btn_excluir)
        
        layout.addLayout(btn_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Descrição", "Preço", "Estoque", "Fornecedor"])
        layout.addWidget(self.table)
        
        # Connect
        self.btn_salvar.clicked.connect(self.salvar_produto)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_excluir.clicked.connect(self.excluir_produto)
        
        self.carregar_fornecedores()
        self.carregar_produtos()

    def carregar_fornecedores(self):
        fornecedores = self.fornecedor_controller.listar_fornecedores()
        self.combo_fornecedor.clear()
        for f in fornecedores:
            self.combo_fornecedor.addItem(f['nome'], f['id'])

    def carregar_produtos(self):
        produtos = self.controller.listar_produtos()
        self.table.setRowCount(len(produtos))
        for i, p in enumerate(produtos):
            self.table.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(p['nome']))
            self.table.setItem(i, 2, QTableWidgetItem(p['descricao']))
            self.table.setItem(i, 3, QTableWidgetItem(f"R$ {p['preco']:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(str(p['estoque'])))
            self.table.setItem(i, 5, QTableWidgetItem(p['fornecedor_nome']))

    def salvar_produto(self):
        nome = self.input_nome.text()
        desc = self.input_desc.text()
        preco = self.input_preco.text()
        estoque = self.input_estoque.text()
        fornecedor_id = self.combo_fornecedor.currentData()
        
        if not nome or not preco or not estoque:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios!")
            return
            
        try:
            preco = float(preco)
            estoque = int(estoque)
        except ValueError:
            QMessageBox.warning(self, "Aviso", "Preço e Estoque devem ser números!")
            return
            
        if self.controller.cadastrar_produto(nome, desc, preco, estoque, fornecedor_id):
            QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao cadastrar produto.")

    def excluir_produto(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para excluir!")
            return
            
        id_produto = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirmação", f"Deseja realmente excluir o produto ID {id_produto}?")
        
        if confirm == QMessageBox.Yes:
            if self.controller.excluir_produto(id_produto):
                QMessageBox.information(self, "Sucesso", "Produto excluído!")
                self.carregar_produtos()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao excluir produto.")

    def limpar_campos(self):
        self.input_nome.clear()
        self.input_desc.clear()
        self.input_preco.clear()
        self.input_estoque.clear()
