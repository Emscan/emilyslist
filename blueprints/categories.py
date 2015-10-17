from flask import Flask, Blueprint, render_template, flash, redirect, request
from models import *
from flask_mail import Message, Mail

app = Flask(__name__)
app.config.from_object('config')

cat = Blueprint('category', __name__)


@cat.route('/categories', methods='GET', 'POST')
def categories():
	if request.method == 'GET':
		return render_template('categories.html', categories=Category.query.all())
	elif request.method == 'POST':
		pass

@cat.route('/categories/<path:catname>')
def category(catname):
	category = Category.query.filter(Category.name==catname).first()
	return render_template('category.html', category=category)

@cat.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return render_template('search_results.html')
	if request.method == 'POST':
		db = db
		search = Category.query.filter(db.text(name like "%s"))
		db.cursor().executemany('select * from db where name like %s', request.form['search'])
		return redirect('/search_results')







