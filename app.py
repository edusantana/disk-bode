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
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

@app.route('/ajuste', methods=['GET', 'POST'])
def vender():
    form = AjusteForm()
    if form.validate_on_submit():
        produto = form.produto.data
        quantidade = form.quantidade.data
        p = ProdutoTipo.query.get(int(produto))
        p.quantidade += quantidade
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('vender'))
        
    produtos = ProdutoTipo.query.all()
    forms = {}
    for p in produtos:
        f = AjusteForm(produto=str(p.id), quantidade=0)
        forms[p] = f
    return render_template('vender.html', produtos=produtos, forms=forms)


@app.route('/', methods=['GET'])
def index():
    produtos = ProdutoTipo.query.all()
    return render_template('index.html', produtos=produtos)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ProdutoTipo=ProdutoTipo)
