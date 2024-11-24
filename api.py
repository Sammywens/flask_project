from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
#DATABASE Schema
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
	id = db.Column (db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)

	def __repr_(self):
		return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='Name cannot be blank')
user_args.add_argument('email', type=str, required=True, help='Email cannot be blank')


userFields = {
		'id':fields.Integer,
		'name':fields.String,
		'email':fields.String
}

#user CRUD FUNCTIONS

class Users(Resource):
		@marshal_with(userFields)
		def get(self):
			users = UserModel.query.all()
			return users

		@marshal_with(userFields)
		def post(self):
			args = user_args.parse_args()
			user = UserModel(name=args["name"], email=args["email"])
			db.session.add(user)
			db.session.commit()
			users = UserModel.query.all()
			return users, 201


		@marshal_with(userFields)
		def put(self, user_id):
			args = user_args.parse_args()
			user = UserModel.query.get(user_id)

			if not user:
				return {'message': 'User not found'}, 404

			user.name = args['name']
			user.email = args['email']

			db.session.commit()
			return user


		@marshal_with(userFields)
		def delete(self, user_id):
			user = UserModel.query.get(user_id)

			if not user:
				return {'message': 'User not found'}, 404

			db.session.delete(user)
			db.session.commit()
			return {'message': 'User deleted successfully'}, 200

api.add_resource(Users, '/api/users/', endpoint='user')
api.add_resource(Users, '/api/users/<int:user_id>', endpoint='user_details')

@app.route('/')
def home():
	return '<h1>Python is awesome!</h1>'


if __name__ == '__main__':
	app.run(debug=True)