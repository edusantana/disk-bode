import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
#from wtforms.fields.html5 import IntegerField
from wtforms.widgets.html5 import NumberInput
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

# https://devcenter.heroku.com/articles/heroku-postgresql
# https://devcenter.heroku.com/articles/heroku-cli

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get('DYNO'):
    # Produção no heroku
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SECRET_KEY'] = 'hard to guess string'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')






bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ProdutoTipo(db.Model):
    __tablename__ = 'produto_tipos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), unique=True, index=True)
    valor = db.Column(db.Float)
    quantidade = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<ProdutoTipo %r quantidade=%s>' % (self.nome, self.quantidade)

    @staticmethod
    def inserir_tipos():
        db.session.add(ProdutoTipo(nome="Bode 130", valor="130"))
        db.session.add(ProdutoTipo(nome="Bode 150", valor="150"))
        db.session.add(ProdutoTipo(nome="Cabra 140", valor="140"))
        db.session.add(ProdutoTipo(nome="Cabra 160", valor="160"))
        db.session.add(ProdutoTipo(nome="Carneiro 180", valor="180"))
        db.session.add(ProdutoTipo(nome="Cabrito 110", valor="110"))
        db.session.add(ProdutoTipo(nome="Cabrita 110", valor="110"))
        db.session.add(ProdutoTipo(nome="Frango", valor="30"))
        db.session.add(ProdutoTipo(nome="Galinha", valor="30"))
        db.session.commit()

class AjusteForm(FlaskForm):
    quantidade = IntegerField('Quantidade', validators=[DataRequired()], widget=NumberInput(step=1))
    produto = HiddenField('ProdutoTipo', validators=[DataRequired()])

    submit = SubmitField('Ajustar')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/ajuste/<operacao>', methods=['GET', 'POST'])
def estoque(operacao):
    form = AjusteForm()
    if form.validate_on_submit():
        produto = form.produto.data
        quantidade = form.quantidade.data
        p = ProdutoTipo.query.get(int(produto))
        if 'vender' == operacao:
            p.quantidade -= quantidade
        else:
            p.quantidade += quantidade
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('estoque', operacao=operacao))

    produtos = ProdutoTipo.query.order_by(ProdutoTipo.nome).all()
    forms = {}
    for p in produtos:
        f = AjusteForm(produto=str(p.id), quantidade=0)
        forms[p] = f
    return render_template('vender.html', produtos=produtos, forms=forms)

@app.route('/ajuste/', methods=['GET'])
@app.route('/ajuste', methods=['GET'])
def ajuste():
    return render_template('ajuste.html')


@app.route('/', methods=['GET'])
def index():
    produtos = ProdutoTipo.query.order_by(ProdutoTipo.nome).all()
    return render_template('index.html', produtos=produtos)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ProdutoTipo=ProdutoTipo)



@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
    # Insere valores iniciais
    ProdutoTipo.inserir_tipos()
