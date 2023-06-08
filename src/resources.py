from flask import request
from flask_restful import Resource
from models import db, Users
from schemas import user_schema, users_schema
from logging_config import logger
from flask import Flask, jsonify, request
import requests
class UserList(Resource):
	def get(self):
		self.logger = logger
		users = Users.query.all()
		logger.info(f'Received User list Request ')
		# roll_counter.add(len(users))
		return users_schema.dump(users)
class UserUpdate(Resource):
	def put(self, id):
		self.logger = logger
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

class UserAdd(Resource):
	def post(self):
		self.logger = logger
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
class UserDetail(Resource):
	def get(self, id):
		user = Users.query.get(id)
		return user_schema.dump(user)
class UserDelete(Resource):
	def delete(self, id):
		self.logger = logger
		# json_data = request.get_json(force=True)
		user = Users.query.get(id)
		self.logger.info(f"Delete User : {user}")
		if not user:
			return {'message': 'No input data provided'}, 400
		# Validate and deserialize input
		db.session.delete(user)
		db.session.commit()
		result = user_schema.dump(user)
		logger.info(f"Delete User result : {result}")
		data={'message': 'User Deleted Successfully', 'ok': True}
		return jsonify(data)
	
class HealthCheck(Resource):
	def get(self):
		try:
			r = requests.get('http://localhost:5000/user/list')
			if r.status_code == 200:
				return {'status': 'up'}, 200
			else:
				return {'status': 'down'}, 500
		except:
			return {'status': 'down'}, 500