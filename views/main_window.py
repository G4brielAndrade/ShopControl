from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QTableWidget, 
                             QTableWidgetItem, QMessageBox)
from PySide6.QtCore import Qt
from controllers.produto_controller import ProdutoController
from views.cliente_view import ClienteView
from views.produto_view import ProdutoView
from views.fornecedor_view import FornecedorView
from views.venda_view import VendaView
from views.compra_view import CompraView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão de Loja")
        self.setMinimumSize(1000, 700)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        
        # Sidebar
        self.sidebar = QVBoxLayout()
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_clientes = QPushButton("Clientes")
        self.btn_produtos = QPushButton("Produtos")
        self.btn_fornecedores = QPushButton("Fornecedores")
        self.btn_vendas = QPushButton("Vendas")
        self.btn_compras = QPushButton("Compras")
        
        self.sidebar.addWidget(self.btn_dashboard)
        self.sidebar.addWidget(self.btn_clientes)
        self.sidebar.addWidget(self.btn_produtos)
        self.sidebar.addWidget(self.btn_fornecedores)
        self.sidebar.addWidget(self.btn_vendas)
        self.sidebar.addWidget(self.btn_compras)
        self.sidebar.addStretch()
        
        self.layout.addLayout(self.sidebar, 1)
        
        # Main Content Area
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack, 5)
        
        # Initialize Pages
        self.init_dashboard()
        self.init_pages()
        
        # Connect Buttons
        self.btn_dashboard.clicked.connect(lambda: self.navegar(0))
        self.btn_clientes.clicked.connect(lambda: self.navegar(1))
        self.btn_produtos.clicked.connect(lambda: self.navegar(2))
        self.btn_fornecedores.clicked.connect(lambda: self.navegar(3))
        self.btn_vendas.clicked.connect(lambda: self.navegar(4))
        self.btn_compras.clicked.connect(lambda: self.navegar(5))

    def init_pages(self):
        self.page_clientes = ClienteView()
        self.page_produtos = ProdutoView()
        self.page_fornecedores = FornecedorView()
        self.page_vendas = VendaView()
        self.page_compras = CompraView()
        
        self.stack.addWidget(self.page_clientes)
        self.stack.addWidget(self.page_produtos)
        self.stack.addWidget(self.page_fornecedores)
        self.stack.addWidget(self.page_vendas)
        self.stack.addWidget(self.page_compras)

    def navegar(self, index):
        self.stack.setCurrentIndex(index)
        # Atualiza o dashboard se for a primeira página
        if index == 0:
            self.atualizar_alertas_estoque()
        # Recarrega dados nas outras telas se necessário
        elif index == 2: self.page_produtos.carregar_fornecedores(); self.page_produtos.carregar_produtos()
        elif index == 4: self.page_vendas.carregar_dados(); self.page_vendas.carregar_vendas()
        elif index == 5: self.page_compras.carregar_dados(); self.page_compras.carregar_compras()
        
    def init_dashboard(self):
        self.dash_page = QWidget()
        layout = QVBoxLayout(self.dash_page)
        
        title = QLabel("Dashboard do Sistema")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Alertas de Estoque Baixo
        self.lbl_alertas = QLabel("Verificando estoque...")
        layout.addWidget(self.lbl_alertas)
        
        self.table_estoque_baixo = QTableWidget()
        self.table_estoque_baixo.setColumnCount(3)
        self.table_estoque_baixo.setHorizontalHeaderLabels(["Produto", "Estoque Atual", "Status"])
        layout.addWidget(self.table_estoque_baixo)
        
        self.stack.addWidget(self.dash_page)
        self.atualizar_alertas_estoque()

    def atualizar_alertas_estoque(self):
        controller = ProdutoController()
        produtos_baixos = controller.verificar_estoque_baixo(5)
        
        if not produtos_baixos:
            self.lbl_alertas.setText("✅ Todos os produtos com estoque em dia.")
            self.lbl_alertas.setStyleSheet("color: green; font-weight: bold;")
            self.table_estoque_baixo.setRowCount(0)
        else:
            self.lbl_alertas.setText(f"⚠️ Atenção: {len(produtos_baixos)} produtos com estoque baixo!")
            self.lbl_alertas.setStyleSheet("color: red; font-weight: bold;")
            
            self.table_estoque_baixo.setRowCount(len(produtos_baixos))
            for i, p in enumerate(produtos_baixos):
                self.table_estoque_baixo.setItem(i, 0, QTableWidgetItem(p['nome']))
                self.table_estoque_baixo.setItem(i, 1, QTableWidgetItem(str(p['estoque'])))
                self.table_estoque_baixo.setItem(i, 2, QTableWidgetItem("REPOR ESTOQUE"))
                self.table_estoque_baixo.item(i, 2).setBackground(Qt.red)
