from flask import Flask, render_template, session, g
from models import *
from blueprints import *

application = Flask(__name__, static_url_path='/static')
application.config.from_object('config')

@application.teardown_appcontext
def shutdown_session(exception=None):
	db.session.remove()

@application.route('/')
def home():
	categories = Category.query.all()
	return render_template('index.html', categories=categories)

@application.route('/search_results')
def search_results():
	return render_template('search_results.html')


application.register_blueprint(listings.listings, session=session, g=g)
application.register_blueprint(categories.cat, session=session, g=g)

if __name__ == '__main__':
	application.run()
