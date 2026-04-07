-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS store_management_system;
USE store_management_system;

-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(255),
    telefone VARCHAR(20),
    endereco VARCHAR(255)
);

-- Tabela de Fornecedores
CREATE TABLE IF NOT EXISTS fornecedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    email VARCHAR(255),
    telefone VARCHAR(20),
    endereco VARCHAR(255)
);

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL DEFAULT 0,
    fornecedor_id INT,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
);

-- Tabela de Compras
CREATE TABLE IF NOT EXISTS compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    fornecedor_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Tabela de Vendas
CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Dados de exemplo

INSERT INTO clientes (nome, cpf, email, telefone, endereco) VALUES
('João Silva', '111.222.333-44', 'joao.silva@email.com', '(11) 98765-4321', 'Rua A, 123, São Paulo'),
('Maria Oliveira', '555.666.777-88', 'maria.o@email.com', '(21) 91234-5678', 'Av. B, 456, Rio de Janeiro');

INSERT INTO fornecedores (nome, cnpj, email, telefone, endereco) VALUES
('Fornecedor Alpha', '00.111.222/0001-33', 'contato@alpha.com', '(31) 3333-4444', 'Rua C, 789, Belo Horizonte'),
('Fornecedor Beta', '44.555.666/0001-77', 'vendas@beta.com', '(41) 5555-6666', 'Av. D, 101, Curitiba');

INSERT INTO produtos (nome, descricao, preco, estoque, fornecedor_id) VALUES
('Notebook X', 'Notebook de alta performance', 3500.00, 10, 1),
('Mouse Gamer', 'Mouse com alta precisão', 150.00, 50, 1),
('Teclado Mecânico', 'Teclado com switches mecânicos', 400.00, 30, 2),
('Monitor Ultrawide', 'Monitor de 34 polegadas', 2000.00, 5, 2);

INSERT INTO compras (fornecedor_id, produto_id, quantidade, preco_unitario) VALUES
(1, 1, 5, 3000.00),
(1, 2, 20, 120.00),
(2, 3, 10, 350.00);

INSERT INTO vendas (cliente_id, produto_id, quantidade, preco_unitario) VALUES
(1, 1, 1, 3500.00),
(2, 3, 1, 400.00);
