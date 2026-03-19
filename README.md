# 🤖 MCP CRM Assistant

Um servidor **MCP (Model Context Protocol)** para gerenciamento de CRM, com busca semântica baseada em **FAISS** e embeddings locais usando `sentence-transformers`.

## ✨ Funcionalidades

| Ferramenta MCP | Descrição |
|---|---|
| `create_user` | Cria um novo usuário e indexa o embedding da sua descrição no FAISS |
| `get_user` | Busca um usuário pelo ID no banco de dados |
| `search_users` | Realiza **busca semântica** para encontrar usuários por similaridade de texto |

## 🏗️ Arquitetura

```
app/
├── server.py                   # Interface MCP (ferramentas expostas)
├── langchain_client.py         # Cliente de teste com LangChain + Gemini
├── modules/
│   ├── database/
│   │   ├── database.py         # Configuração do SQLite (SQLAlchemy)
│   │   ├── models.py           # Modelo de dados (User)
│   │   └── seed.py             # Script para popular o banco com dados de exemplo
│   └── llm/
│       ├── embeddings.py       # Geração de embeddings (all-MiniLM-L6-v2)
│       └── vector_store.py     # Indexação e busca vetorial (FAISS)
├── tests/
│   └── test_server.py          # Testes de integração
└── utils/
    └── paths.py                # Caminhos centralizados do projeto
```

**Por que essa estrutura modular?**

A arquitetura foi organizada em módulos independentes (`database`, `llm`, `utils`) para permitir **crescimento sem atrito**. Precisa trocar o SQLite por Postgres? Só mexe em `database/`. Quer testar outro modelo de embeddings? Só mexe em `llm/`. Novos módulos (ex: `notifications/`, `analytics/`) podem ser adicionados sem impactar o restante do sistema. Cada camada tem uma responsabilidade única e bem definida.

**Fluxo de dados:**
1.  `create_user` → salva no **SQLite** + gera embedding → indexa no **FAISS**
2.  `search_users` → gera embedding da query → busca no **FAISS** → cruza IDs com o **SQLite**
3.  O protocolo **MCP via stdio** conecta qualquer LLM (Claude, Gemini) ao servidor

## 🚀 Como Rodar

### Pré-requisitos
- Python 3.12+
- Docker (opcional)

### 1. Configuração local

```bash
# Clone o repositório e crie o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e adicione sua GOOGLE_API_KEY
```

### 2. Rodar os testes

```bash
make test
```

### 3. Popular o banco com dados de exemplo

```bash
make seed
```

### 4. Testar a integração MCP + Gemini (LangChain)

```bash
# Roda o cliente LangChain que conversa com o servidor MCP via subprocess
python app/langchain_client.py
```

## 🐳 Rodar com Docker

```bash
# Constrói a imagem e executa o teste de integração completo
make docker-run

# Apenas popular o banco via Docker
make docker-seed
```

## 🧪 Testes

A suíte de testes valida a integração entre as camadas SQL e FAISS:

- **`test_create_user`**: Cria um usuário e verifica a persistência no banco.
- **`test_get_user`**: Busca um usuário pelo ID e valida o retorno em JSON.
- **`test_search_users`**: Realiza uma busca semântica e valida o formato da resposta.

```bash
make test
```

## 🔌 Integração com Clientes MCP

O servidor usa o transporte **stdio** (padrão MCP). Para conectar ao **Claude Desktop**, adicione ao seu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "crm-assistente": {
      "command": "python",
      "args": ["/caminho/para/mcp-server/app/server.py"]
    }
  }
}
```

Via Docker:
```json
{
  "mcpServers": {
    "crm-assistente": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GOOGLE_API_KEY", "mcp-server-app"]
    }
  }
}
```

## 📦 Stack Tecnológica

- **[FastMCP](https://github.com/jlowin/fastmcp)** — Framework para criar servidores MCP
- **[FAISS](https://github.com/facebookresearch/faiss)** — Busca vetorial de alta performance
- **[Sentence Transformers](https://sbert.net/)** — Modelo `all-MiniLM-L6-v2` para embeddings locais
- **[SQLAlchemy](https://www.sqlalchemy.org/)** + **SQLite** — Persistência de dados
- **[LangChain](https://langchain.com/)** + **LangGraph** — Orquestração de agentes LLM
- **[Google Gemini](https://ai.google.dev/)** — LLM para o cliente de teste
