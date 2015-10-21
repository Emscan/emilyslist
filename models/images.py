from db import db

class Image(db.Model):
	__tablename__ = 'images'
	id = db.Column(db.Integer, primary_key=True)
	listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
	filename = db.Column(db.String(255))

	@classmethod
	def create(cls, filename, listing_id):
		image = Image(filename=filename, listing_id=listing_id)
		db.session.add(image)
		db.session.commit()


	#add multiple images interface (maybe another input tag to add another one)