from flask import request
from flask_restful import Resource
from models import db, Users
from schemas import user_schema, users_schema
from logging_config import logger
from flask import Flask, jsonify, request

class UserList(Resource):
	def get(self):
		users = Users.query.all()
		# roll_counter.add(len(users))
		return users_schema.dump(users)
class UserUpdate(Resource):
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
class UserDetail(Resource):
	def get(self, id):
		user = Users.query.get(id)
		return user_schema.dump(user)
class UserDelete(Resource):
	def delete(self, id):
		json_data = request.get_json(force=True)
		logging.info(f"Delete User json_data : {json_data}")
		if not json_data:
			return {'message': 'No input data provided'}, 400
		# Validate and deserialize input
		data = user_schema.load(json_data)
		user = Users.query.get(id).delete()
		db.session.commit()
		result = user_schema.dump(user)
		logging.info(f"Delete User result : {result}")
		return { "status": 'success', 'data': result}, 204