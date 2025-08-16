# Meu Poema Flask

Este é um projeto web desenvolvido com Flask, que permite aos usuários criar, visualizar e interagir com poemas. A aplicação inclui funcionalidades como autenticação de usuários, criação de posts, e exibição de poemas em um feed.

## Funcionalidades

- **Autenticação de Usuários**: Login e registro de contas.
- **Criação de Poemas**: Usuários autenticados podem criar e postar poemas.
- **Feed de Poemas**: Exibição de poemas postados por diferentes usuários.
- **Interação com Posts**: Possibilidade de salvar poemas (bookmark) e visualizar informações do autor.

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS
- **Banco de Dados**: SQLite (ou outro configurado no Flask)
- **Outras Bibliotecas**:
  - Jinja2 (para templates)
  - Flask-WTF (para formulários)
  - Flask-Login (para autenticação)

## Estrutura do Projeto

- `meuPoema/`
  - `templates/`: Contém os arquivos HTML.
  - `static/`: Contém os arquivos CSS, imagens e outros assets.
  - `routes.py`: Define as rotas da aplicação.
  - `models.py`: Define os modelos de dados.
  - `forms.py`: Define os formulários da aplicação.
  - `app.py`: Arquivo principal para rodar o servidor Flask.

## Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone git@github.com:Davi-html/meu-poema-flask.git
   cd meu-poema-flask
