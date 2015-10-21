from db import db

class Listing(db.Model):
	__tablename__ = 'listings'
	id = db.Column(db.Integer, primary_key=True)
	cat_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	email = db.Column(db.String(255), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(100), index=True, nullable=False)
	body = db.Column(db.Text(length=10000), nullable=False)
	images = db.relationship('Image', backref='listing')
	token = db.Column(db.String(255), nullable=False)

	def update(self, *args, **kwargs):
		try:
			self.email = kwargs['email']
			self.title = kwargs['title']
			self.body = kwargs['body']
			self.price = kwargs['price']
			db.session.add(self)
			db.session.commit()
		except:
			db.session.rollback()

	def delete(self):
		try:
			db.session.delete(self)
			for image in self.images:
				db.session.delete(image)
			db.session.commit()
		except:
			db.session.rollback()

	@classmethod
	def create(cls, *args, **kwargs):
		try:
			listing = Listing(**kwargs)
			db.session.add(listing)
			db.session.commit()
		except:
			db.session.rollback()
		return listing
