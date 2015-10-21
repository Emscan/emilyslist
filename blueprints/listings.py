from flask import Flask, Blueprint, request, session, render_template, send_from_directory
from werkzeug import secure_filename
import os
from flask_mail import Message, Mail

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)

listings = Blueprint('listings', __name__)

@listings.route('/listings', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('listings.html', listings=Listing.query.all())
	elif request.method == 'POST':
		file = request.files['file']
		text = request.form.get('text')
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return text + '<img src="/assets/{0}" />'.format(filename)

@listings.route('/assets', methods=['POST'])
def asset():
	img_file = request.files.get('file')
	filename = secure_filename(img_file.filename) 		
	img_file.save(os.path.join(app.config['ASSET_FOLDER'], filename))
	return '<img src="/assets/{0}" />'.format(filename)

@listings.route('/assets/<path:filename>')
def assets(path):
	return send_from_directory('uploads', path)

@listings.route('/create_listing', methods=['GET', 'POST'])
def create():
	if request.method == 'GET':
		return render_template('create_listing.html', categories=Category.query.all())
	elif request.method == 'POST':
		cat_id = request.form.get('cat_id')
		title = request.form.get('title')
		body = request.form.get('body')
		email = request.form.get('email')
		price = requst.form.get('price')
		filename = 'None'
		token = bcrypt.gensalt()
		if title and body and email and price:
			listing = Listing.create(cat_id=cat_id, title=title, body=body, email=email, price=price, token=token)
			for img_file in request.files.getlist('file[]'):
				filename = secure_filename(img_file.filename)
				if filename:
					img_file.save(os.path.join(app.config['uploads'], filename))
					image = Image.create(filename=filename, listing_id=listing.id)
			link = 'http://localhost:5000/edit/{1}?token={0}'.format(token, listing.id)
			msg = Message('Edit listing email address', sender='emscancode@gmail.com', recipients=[email])
			msg.body = 'Click here to edit your listing: ' + link
			mail.send(msg)
			flash('Listing created. Please check your email for a link to edit it.')
			return redirect('/')
		else:
			flash('Oops, something went wrong. Please create a valid listing.')
			return render_template('create.html')

@listings.route('/listing/delete/<path:listing_id>')
def delete(post_id):
	listing = Listing.query.filter(Listing.id==listing_id).first()
	listing.delete()
	flash('Your listing has been removed.')
	return redirect('/')

@listings.route('/edit_listing/<listing_id>', methods=['GET', 'POST'])
def edit(listing_id):
	if request.method == 'GET':
		token = request.args.get('token')
		listing = Listing.query.filter(Listing.id==listing_id).first()
		category = Category.query.filter(Category.id==listing.cat_id).first()
		if token != listing.token:
			flash('Please use the link sent to your email')
			return render_template('home.html')
		return render_template('edit_listing.html', listing=listing, cat_name=cat_name)
	elif request.method == 'POST':
		listing = Listing.query.filter(Listing.id==listing_id).first()
		title = request.form.get('title')
		body = request.form.get('body')
		email = request.form.get('email')
		price = request.form.get('price')
		img_file = request.form.get('file')
		filename = 'None'
		if img_file:
			if img_file.filename != listing.img_filename:
				filename = secure_filename(img_file.filename)
				img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				image = Image.create(filename=filename, listing_id=listing.id)
			listing.update(title=title, body=body, email=email, price=price, filename=filename)
			flash('update successful')
			return redirect

@listings.route('/listings/<path:listing_id>')
def listing(listing_id):
	listing = Listing.query.filter(Listing.id==listing_id).first()
	images = listing.images
	return render_template('listing.html', listing=listing, images=images)
			
@listings.route('/uploads', methods=['POST'])
def upload():
	img_file = request.files.get('file')
	filename = secure_filename(img_file.filename)
	img_file.save(os.path.join(app.config['ASSET_FOLDER'], filename))
	return '<img src="/assets/{0}" />'.format(filename)

@listings.route('/uploads/<path:filename>')
def uploads(filename):
	return send_from_directory('uploads', filename)	



