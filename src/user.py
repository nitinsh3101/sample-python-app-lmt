from urllib import response
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import sqlalchemy
import logging
import os
import requests
import json as JSON

app_name = 'User Backend Service'
app = Flask('User Backend Service')
CORS(app)
logger = logging.getLogger(app_name)

DB_USER='ctgdevops' #os.getenv('DB_USER')
DB_PASS='devops123' #os.getenv('DB_PASS')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@54.163.126.233:5432/ctg-devops-ktracker'
db = SQLAlchemy(app)
ma = Marshmallow(app)

api = Api(app)
# logger = logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s; %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s; %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app1.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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

	def __init__(self, designation, email, first_name, is_admin, last_name, middle_name, oidc_id, phone_number, previous_exp):
		self.designation = designation
		self.email = email
		self.first_name = first_name
		self.is_admin = is_admin
		self.last_name = last_name
		self.middle_name = middle_name
		self.oidc_id = oidc_id
		self.phone_number = phone_number
		self.previous_exp = previous_exp

class UsersSchema(ma.Schema):
	class Meta:
		# Fields to expose
		fields = ('designation', 'email', 'first_name', 'is_admin', 'last_name', 'middle_name', 'oidc_id', 'phone_number', 'previous_exp')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

class UsersList(Resource):
	def get(self):
		users = Users.query.all()
		# roll_counter.add(len(users))
		return users_schema.dump(users)

api.add_resource(UsersList, '/users')
class UsersDetail(Resource):
	def get(self, id):
		user = Users.query.get(id)
		return user_schema.dump(user)
	
api.add_resource(UsersDetail, '/user/<int:id>')

class UserAdd(Resource):
	def post(self):
		logger.info(f'Received User Create Request ')

		logger.info(f'Received User Create Request with data {request.data}')
		# json_data = request.get_json(force=True)
		json_data = request.get_json(force=True)
		if not json_data:
			return {'message': 'No input data provided'}, 400
		designation = json_data['designation']
		email = json_data['email']
		first_name = json_data['first_name']
		is_admin = json_data['is_admin']
		last_name = json_data['last_name']
		middle_name = json_data['middle_name']
		oidc_id = json_data['oidc_id']
		phone_number = int(json_data['phone_number'])
		previous_exp = json_data['previous_exp']
		logger.info(f'New User Object is gertting created')
		new_user = Users(designation, email, first_name, is_admin, last_name, middle_name, oidc_id, phone_number, previous_exp)
		logger.info(f'New User Object {new_user}')
		db.session.add(new_user)
		db.session.commit()
		headers={'Content-Type': 'application/json'}
		data={'ok': 'true','message': 'New User Created Successfully', 'ok': True}
		return jsonify(data)
api.add_resource(UserAdd, '/add_user')
# # create rest api for updating a user in the users table
class UsersUpdate(Resource):
	def put(self, id):
		user = Users.query.get(id)

		designation = request.json['designation']
		email = request.json['email']
		first_name = request.json['first_name']
		is_admin = request.json['is_admin']
		last_name = request.json['last_name']
		middle_name = request.json['middle_name']
		oidc_id = request.json['oidc_id']
		phone_number = request.json['phone_number']
		previous_exp = request.json['previous_exp']

		user.designation = designation
		user.email = email
		user.first_name = first_name
		user.is_admin = is_admin
		user.last_name = last_name
		user.middle_name = middle_name
		user.oidc_id = oidc_id
		user.phone_number = phone_number
		user.previous_exp = previous_exp

		db.session.commit()
		return user_schema.dump(user)

api.add_resource(UsersUpdate, '/user/<int:id>')
# 		

# class HealthCheck(Resource):
# 	def get(self):
# 		try:
# 			r = requests.get('http://localhost:5000/users')
# 			if r.status_code == 200:
# 				return {'status': 'up'}, 200
# 			else:
# 				return {'status': 'down'}, 500
# 		except:
# 			return {'status': 'down'}, 500
		
# api.add_resource(HealthCheck, '/health')
@app.route('/error', methods=['GET'])
def error():
    data = {
        'message': 'This is Error Page displayed after error'
    }
#     error_counter.inc()
    logger.info(f'Received API request{data}')
    return jsonify(data)

# write code to handle 404 errors 
@app.errorhandler(404)
def not_found(e):
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 404

# write code to handle 500 errors
@app.errorhandler(500)
def internal_error(e):
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 500

# write code to handle 503 errors
@app.errorhandler(503)
def service_unavailable(e):
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 503

# write code to handle any generic errors 
@app.errorhandler(Exception)
def unhandled_exception(e):
    logger.error(f'Error  {e}')
    return jsonify(error=str(e)), 500


from appmetrics.wsgi import AppMetricsMiddleware
app.wsgi_app = AppMetricsMiddleware(app.wsgi_app)
app.run(host='0.0.0.0', debug=True)

# app.run(
#     host="0.0.0.0",
#     port=int("5001"),
#     debug=True
#     )
