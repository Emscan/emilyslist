from db import db

class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True, nullable=False)
	listings = db.relationship('Listing', backref='category')

	