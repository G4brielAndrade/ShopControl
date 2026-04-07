from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFormLayout)
from controllers.movimentacao_controller import FornecedorController

class FornecedorView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = FornecedorController()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Gestão de Fornecedores")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.input_nome = QLineEdit()
        self.input_cnpj = QLineEdit()
        self.input_email = QLineEdit()
        self.input_telefone = QLineEdit()
        self.input_endereco = QLineEdit()
        
        form_layout.addRow("Nome:", self.input_nome)
        form_layout.addRow("CNPJ:", self.input_cnpj)
        form_layout.addRow("Email:", self.input_email)
        form_layout.addRow("Telefone:", self.input_telefone)
        form_layout.addRow("Endereço:", self.input_endereco)
        
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
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CNPJ", "Email", "Telefone", "Endereço"])
        layout.addWidget(self.table)
        
        # Connect
        self.btn_salvar.clicked.connect(self.salvar_fornecedor)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_excluir.clicked.connect(self.excluir_fornecedor)
        
        self.carregar_fornecedores()

    def carregar_fornecedores(self):
        fornecedores = self.controller.listar_fornecedores()
        self.table.setRowCount(len(fornecedores))
        for i, f in enumerate(fornecedores):
            self.table.setItem(i, 0, QTableWidgetItem(str(f['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(f['nome']))
            self.table.setItem(i, 2, QTableWidgetItem(f['cnpj']))
            self.table.setItem(i, 3, QTableWidgetItem(f['email']))
            self.table.setItem(i, 4, QTableWidgetItem(f['telefone']))
            self.table.setItem(i, 5, QTableWidgetItem(f['endereco']))

    def salvar_fornecedor(self):
        nome = self.input_nome.text()
        cnpj = self.input_cnpj.text()
        email = self.input_email.text()
        telefone = self.input_telefone.text()
        endereco = self.input_endereco.text()
        
        if not nome or not cnpj:
            QMessageBox.warning(self, "Aviso", "Nome e CNPJ são obrigatórios!")
            return
            
        if self.controller.cadastrar_fornecedor(nome, cnpj, email, telefone, endereco):
            QMessageBox.information(self, "Sucesso", "Fornecedor cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_fornecedores()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao cadastrar fornecedor.")

    def excluir_fornecedor(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um fornecedor para excluir!")
            return
            
        id_fornecedor = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirmação", f"Deseja realmente excluir o fornecedor ID {id_fornecedor}?")
        
        if confirm == QMessageBox.Yes:
            if self.controller.excluir_fornecedor(id_fornecedor):
                QMessageBox.information(self, "Sucesso", "Fornecedor excluído!")
                self.carregar_fornecedores()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao excluir fornecedor.")

    def limpar_campos(self):
        self.input_nome.clear()
        self.input_cnpj.clear()
        self.input_email.clear()
        self.input_telefone.clear()
        self.input_endereco.clear()
