from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resource import ItemResource, ItemListResource, RegisterUser, \
    StoreResource, StoreListResource, UserResource
from service import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'secret_key'
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(RegisterUser, '/register')
api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(StoreListResource, '/stores')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemListResource, '/items')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
