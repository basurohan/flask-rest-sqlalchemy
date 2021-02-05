from flask_restful import Resource, reqparse

from model import User


class UserResource(Resource):

    def get(self, user_id):
        user = User.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 400

    def delete(self, user_id):
        user = User.find_by_id(user_id)
        if user:
            user.delete()
        return {'message': 'User deleted.'}


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='username must be provided'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='password must be provided'
    )

    def post(self):
        data = RegisterUser.parser.parse_args()
        try:
            if User.find_by_username(data['username']):
                return {'message': 'User already exists'}, 400
            user = User(**data)
            user.persist()
        except Exception:
            return {'message': 'User could not be saved'}, 500
        else:
            return {'message': 'User created'}, 201