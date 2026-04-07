from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QFormLayout)
from controllers.cliente_controller import ClienteController

class ClienteView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ClienteController()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Gestão de Clientes")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        self.input_nome = QLineEdit()
        self.input_cpf = QLineEdit()
        self.input_email = QLineEdit()
        self.input_telefone = QLineEdit()
        self.input_endereco = QLineEdit()
        
        form_layout.addRow("Nome:", self.input_nome)
        form_layout.addRow("CPF:", self.input_cpf)
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
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Email", "Telefone", "Endereço"])
        layout.addWidget(self.table)
        
        # Connect
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_excluir.clicked.connect(self.excluir_cliente)
        
        self.carregar_clientes()

    def carregar_clientes(self):
        clientes = self.controller.listar_clientes()
        self.table.setRowCount(len(clientes))
        for i, c in enumerate(clientes):
            self.table.setItem(i, 0, QTableWidgetItem(str(c['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(c['nome']))
            self.table.setItem(i, 2, QTableWidgetItem(c['cpf']))
            self.table.setItem(i, 3, QTableWidgetItem(c['email']))
            self.table.setItem(i, 4, QTableWidgetItem(c['telefone']))
            self.table.setItem(i, 5, QTableWidgetItem(c['endereco']))

    def salvar_cliente(self):
        nome = self.input_nome.text()
        cpf = self.input_cpf.text()
        email = self.input_email.text()
        telefone = self.input_telefone.text()
        endereco = self.input_endereco.text()
        
        if not nome or not cpf:
            QMessageBox.warning(self, "Aviso", "Nome e CPF são obrigatórios!")
            return
            
        if self.controller.cadastrar_cliente(nome, cpf, email, telefone, endereco):
            QMessageBox.information(self, "Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_clientes()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao cadastrar cliente. Verifique os dados.")

    def excluir_cliente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir!")
            return
            
        id_cliente = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Confirmação", f"Deseja realmente excluir o cliente ID {id_cliente}?")
        
        if confirm == QMessageBox.Yes:
            if self.controller.excluir_cliente(id_cliente):
                QMessageBox.information(self, "Sucesso", "Cliente excluído!")
                self.carregar_clientes()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao excluir cliente.")

    def limpar_campos(self):
        self.input_nome.clear()
        self.input_cpf.clear()
        self.input_email.clear()
        self.input_telefone.clear()
        self.input_endereco.clear()
