from db import db
from categories import *

CATEGORY_NAMES = ['Appliances', 
				'Baby and Child', 
				'Bikes', 
				'Camping and Outdoors', 
				'Cars', 
				'Computers', 
				'Entertainment', 
				'Furniture', 
				'Garden', 
				'Health and Beauty', 
				'Household', 
				'Sports Equipment', 
				'Toys & Games']

for cat in Category.query.all():
	db.session.delete(cat)

for name in CATEGORY_NAMES:
	category = Category(name=name)
	db.session.add(category)
db.session.commit()