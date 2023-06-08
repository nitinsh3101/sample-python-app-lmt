from flask_marshmallow import Marshmallow
from models import Users

ma = Marshmallow()

class UsersSchema(ma.Schema):
	class Meta:
		# Fields to expose
		fields = ('id','designation', 'email', 'first_name', 'is_admin', 'last_name', 'middle_name', 'oidc_id', 'phone_number', 'previous_exp')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)