# disk-bode

Aplicação do disk-bode

## Requisitos

- Gerenciar o estoque de bodes
    - Mostrar a quantidade de bodes no estoque
    - Ajustar a quantidade
    - Cadastrar/Atualizar novos tipos e valores


# Instruções para execução

```
git clone https://github.com/edusantana/disk-bode
cd disk-bode
# cria ambiente virtual do python
python3 -m venv venv
# ativa ambiente virtual do python
source venv/bin/activate
# instala essas bibliotecas no ambiente virtal ativado
pip install flask flask-bootstrap flask-moment flask-wtf flask-sqlalchemy flask-migrate
```

Configurar as variáveis de ambiente para execução do flask:

    export FLASK_APP=app.py
    export FLASK_DEBUG=1


Agora vamos adicionar valores ao banco de dados, ativa o python em modo interativo, com o flask ativado.

       flask shell

Depois, insere os seguintes valores:

```python
from app import db, ProdutoTipo

db.create_all()

bodinho = ProdutoTipo(nome="Bodinho", valor=70, quantidade=10)
bodao = ProdutoTipo(nome="Bodão", valor=140, quantidade=20)

db.session.add(bodinho)
db.session.add(bodao)
db.session.commit()

# Consultando

ProdutoTipo.query.all() 

# Saindo ou pressiona `CTRL+D`
exit()

```

E executar a aplicação

```
flask run -p 8080
```

# Sobre o livro

```
git clone https://github.com/miguelgrinberg/flasky.git
cd flasky
git checkout -f 4c
cd ..
```

# faz o de voces

```
git clone https://github.com/seu-login/seu-projeto
cd seu-projeto

python3 -m venv venv
source venv/bin/activate

```
