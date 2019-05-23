# disk-bode
Aplicação do disk-bode


# Instruções para execução

```
git clone https://github.com/edusantana/disk-bode
cd disk-bode
python3 -m venv venv
source venv/bin/activate
pip install flask flask-bootstrap flask-moment flask-wtf flask-sqlalchemy flask-migrate
```

Agora vamos adicionar valores ao banco de dados:

Digita:

       flask shell

Depois, insere os seguintes valores:

```python
from app import db
db.create_all()

bodinho = ProdutoTipo(nome="Bodinho", valor=70, quantidade=10)
bodao = ProdutoTipo(nome="Bodão", valor=140, quantidade=20)

db.session.add(bodinho)
db.session.add(bodao)
db.session.commit()

```

Digita `exit` para sair ou pressiona `CTRL+D`

E executar a aplicação

```
export FLASK_APP=app.py
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
