from database import db


class Users(db.Model):
	__tablename__ = 'users'
	__table_args__ = {'schema': 'users'}
	id = db.Column(db.Integer, primary_key=True)
	designation = db.Column(db.String(80), unique=False)
	email = db.Column(db.String(120), unique=False)
	first_name = db.Column(db.String(120), unique=False)
	is_admin = db.Column(db.String(120), unique=False)
	last_name = db.Column(db.String(120), unique=False)
	middle_name = db.Column(db.String(120), unique=False)
	oidc_id = db.Column(db.String(120), unique=False)
	phone_number = db.Column(db.String(120), unique=False)
	previous_exp = db.Column(db.String(120), unique=False)

	def __init__(self, id, designation, email, first_name, is_admin, last_name, middle_name, oidc_id, phone_number, previous_exp):
		self.id = id
		self.designation = designation
		self.email = email
		self.first_name = first_name
		self.is_admin = is_admin
		self.last_name = last_name
		self.middle_name = middle_name
		self.oidc_id = oidc_id
		self.phone_number = phone_number
		self.previous_exp = previous_exp
