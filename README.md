# 🔧 Sistema de Gestão de Ordens de Serviço (OS)

Um sistema web simples e intuitivo para abertura, controlo e monitorização de Ordens de Serviço (OS) em tempo real, desenvolvido com Python (Flask) e MySQL.

---

## 📝 Descrição do Projeto
🔧 Sistema web simples para gestão de Ordens de Serviço (OS). Permite criar chamados com descrição e prioridade (Baixa, Média, Alta), atualizar o status (Aberta, Em andamento, Concluída) em tempo real e listar todas as demandas na tela. Conta com banco de dados MySQL e recursos para exportar relatórios das ordens em formatos CSV e PDF.

---

## 📁 Estrutura de Arquivos

* `app.py`: Arquivo principal em Python. Contém o servidor Flask, a conexão com o banco MySQL e as rotas da API.
* `templates/index.html`: Interface visual do sistema. Criada com Tailwind CSS e JavaScript para controlar a tela sem recarregar a página.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Banco de Dados:** MySQL
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API)
* **Bibliotecas auxiliares:** ReportLab (Geração de PDF), CSV (Nativa do Python)

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
* Ter o **Python 3** instalado na máquina.
* Ter o **XAMPP** (ou outro servidor MySQL) instalado e em execução.

### 2. Configurar o Banco de Dados (MySQL)
1. Abra o painel do XAMPP e clique em **Start** no Apache e no MySQL.
2. Acesse o phpMyAdmin (`http://localhost/phpmyadmin`).
3. Crie um banco de dados chamado `sistema_os`.
4. Vá até a aba **SQL** e execute o seguinte comando para criar a tabela:

```sql
CREATE TABLE IF NOT EXISTS ordens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    prioridade ENUM('Baixa', 'Média', 'Alta') NOT NULL,
    status ENUM('Aberta', 'Em andamento
