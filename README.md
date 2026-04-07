# Sistema de Gestão de Loja

Este é um sistema desktop completo para gestão de lojas, desenvolvido em Python com PySide6 para a interface gráfica e MySQL para o banco de dados. Ele inclui funcionalidades para controle de clientes, produtos, fornecedores, compras, vendas e estoque.

## 🎯 Funcionalidades

- **Clientes**: Cadastro, listagem, edição e exclusão.
- **Produtos**: Cadastro, controle de preço e estoque, associação com fornecedor.
- **Fornecedores**: Cadastro completo, relacionamento com produtos.
- **Compras**: Registro de compras, atualização automática do estoque.
- **Vendas**: Registro de vendas, baixa automática no estoque, associação com cliente.
- **Estoque**: Controle automático, alertas de estoque baixo no dashboard.

## 🛠️ Tecnologias

- **Linguagem**: Python 3.x
- **Interface Gráfica**: PySide6 (Qt for Python)
- **Banco de Dados**: MySQL
- **Arquitetura**: MVC (Model-View-Controller)

## 📁 Estrutura do Projeto

```
store_management_system/
├── controllers/
│   ├── cliente_controller.py
│   ├── movimentacao_controller.py
│   └── produto_controller.py
├── database/
│   ├── connection.py
│   └── schema.sql
├── models/
│   └── models.py
├── ui/ (para arquivos .ui gerados pelo Qt Designer, se usados)
├── utils/ (para utilitários diversos, se necessário)
├── views/
│   ├── main_window.py
│   ├── cliente_view.py
│   ├── produto_view.py
│   ├── fornecedor_view.py
│   ├── venda_view.py
│   └── compra_view.py
├── main.py
└── README.md
```

- `controllers/`: Contém a lógica de negócios e a interação com o banco de dados.
- `database/`: Contém o script de conexão com o MySQL e o script SQL para criação do esquema.
- `models/`: Define as classes de modelo de dados.
- `ui/`: Diretório para armazenar arquivos `.ui` gerados pelo Qt Designer (não implementado diretamente neste projeto, mas a estrutura está pronta).
- `utils/`: Para funções utilitárias gerais.
- `views/`: Contém as classes da interface gráfica (telas).
- `main.py`: Ponto de entrada da aplicação.

## ▶️ Como Rodar o Projeto

### 1. Pré-requisitos

Certifique-se de ter o Python 3.x e o MySQL Server instalados em sua máquina.

### 2. Configuração do Banco de Dados

1. **Crie o banco de dados e as tabelas**: 
   - Acesse seu servidor MySQL (ex: via `mysql -u root -p`).
   - Execute o script `database/schema.sql` para criar o banco de dados `store_management_system` e todas as tabelas necessárias, além de popular com dados de exemplo.
   ```bash
   mysql -u root -p < store_management_system/database/schema.sql
   ```
   - **Importante**: Se você usa um usuário e senha diferentes para o MySQL, edite o arquivo `database/connection.py` com suas credenciais.

### 3. Instalação das Dependências

Navegue até o diretório raiz do projeto (`store_management_system`) e instale as dependências Python:

```bash
cd store_management_system
pip install PySide6 mysql-connector-python
```

### 4. Execução da Aplicação

Após instalar as dependências e configurar o banco de dados, você pode rodar a aplicação:

```bash
python main.py
```

## 🎨 Uso do Qt Designer (Opcional)

Embora as interfaces neste projeto tenham sido criadas programaticamente para demonstração, você pode usar o Qt Designer para criar arquivos `.ui` visualmente. Para integrá-los:

1. **Crie seu design no Qt Designer**: Salve o arquivo como `minha_tela.ui` no diretório `ui/`.
2. **Converta o arquivo .ui para .py**: Use `pyside6-uic` (ou `pyuic5` para PyQt5):
   ```bash
   pyside6-uic ui/minha_tela.ui -o views/ui_minha_tela.py
   ```
3. **Importe e use na sua View**: Na sua classe de View, você pode carregar a interface gerada:
   ```python
   from PySide6.QtWidgets import QWidget
   from views.ui_minha_tela import Ui_MinhaTela

   class MinhaTelaView(QWidget, Ui_MinhaTela):
       def __init__(self):
           super().__init__()
           self.setupUi(self)
           # Conecte seus sinais e slots aqui
   ```

## 🚀 Sugestões de Melhorias Futuras

- **Autenticação de Usuários**: Adicionar um sistema de login e controle de acesso.
- **Relatórios**: Geração de relatórios de vendas, estoque, etc.
- **Busca e Filtros**: Implementar funcionalidades de busca e filtragem mais avançadas nas tabelas.
- **Internacionalização**: Suporte a múltiplos idiomas.
- **Persistência de Configurações**: Salvar configurações do usuário (ex: tamanho da janela).
- **Testes Unitários**: Adicionar testes para a lógica de negócios e controladores.
- **Empacotamento**: Criar um executável standalone (ex: com PyInstaller).
- **Melhorias na UI/UX**: Refinar o design e a usabilidade com estilos CSS (QSS) ou ícones.
- **Validação de Entrada**: Validações mais robustas para campos de formulário (ex: regex para CPF/CNPJ).

---
