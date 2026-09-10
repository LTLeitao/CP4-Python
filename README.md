# 🏋️‍♂️ Gerenciamento de Alunos e Planos - Academia

Aplicação Web completa para gerenciamento de alunos e planos de academia, construída com **FastAPI** no backend, **SQLite** para persistência de dados e uma interface moderna (*dark mode*) em **HTML/CSS/JavaScript**.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic
- **Banco de Dados:** SQLite3 (Consultas via SQL Puro com `JOIN`)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---

## 📁 Estrutura do Projeto

```text
CP4-Python/
├── app/
│   ├── __init__.py
│   ├── controller.py   # Rotas e endpoints da API
│   ├── database.py     # Criação e conexão com o SQLite
│   ├── main.py         # Instância do FastAPI e inicialização do app
│   ├── schemas.py      # Schemas Pydantic (Validação de entrada)
│   └── services.py     # Regras de negócio e queries SQL
├── static/
│   ├── index.html      # Interface principal
│   ├── script.js       # Consumo da API e manipulação da DOM
│   └── style.css       # Estilização da interface
├── database.db         # Banco de dados SQLite (gerado automaticamente)
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto

🚀 Como Executar o Projeto
Pré-requisitos
Python instalado (versão 3.10 ou superior).

Passo a Passo
Clonar o repositório:

Bash
git clone [https://github.com/LTLeitao/CP4-Python.git](https://github.com/LTLeitao/CP4-Python.git)
cd CP4-Python
Instalar as dependências:

Bash
pip install -r requirements.txt
Iniciar o servidor Backend:

Bash
python -m uvicorn app.main:app --reload
O banco de dados SQLite (database.db) e suas tabelas serão criados automaticamente na primeira inicialização.

Acessar a Aplicação:

Frontend: Abra o arquivo static/index.html diretamente no seu navegador.

Documentação da API (Swagger): Acesse http://127.0.0.1:8000/docs para testar os endpoints interativamente.

📌 Funcionalidades e Rotas
GET /users - Lista todos os alunos (retornando o nome do plano via JOIN)

POST /users - Cadastra um novo aluno

PATCH /users/{user_id} - Atualiza dados de um aluno

DELETE /users/{user_id} - Remove um aluno

GET /users/plans - Lista os planos disponíveis para seleção