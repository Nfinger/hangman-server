#!flask/bin/python
import flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from flask_mongoengine import MongoEngine
from flask_cors import CORS

# Model imports
from User import User
from Stats import Stats
from Game import Game

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'hangman'}

CORS(app)
db = MongoEngine()
db.init_app(app)
api = Api(app)


class SignupRoutes(Resource):
    def post(self):
        user_request_parser = RequestParser(bundle_errors=True)
        user_request_parser.add_argument("password", required=True)
        user_request_parser.add_argument("email", required=True)
        args = user_request_parser.parse_args()
        user = User(email=args["email"], password=User.set_password(args["password"]))
        user.save()
        user = User.return_helper(user)
        print(user)
        stat = Stats(userId=user['id'])
        stat.save()
        return {"user": user}

class LoginRoutes(Resource):
    def post(self):
        user_request_parser = RequestParser(bundle_errors=True)
        user_request_parser.add_argument("password", required=True)
        user_request_parser.add_argument("email", required=True)
        args = user_request_parser.parse_args()
        users = User.objects(email=args["email"])
        if User.check_password(users[0].password, args["password"]):
            return {"user": User.return_helper(users[0])}
        else:
            return {"error": "Incorrect Password"}

class UserRoutes(Resource): 
    def get(self, user_id):
        users = User.objects(id=user_id)
        user = User.return_helper(users[0])
        return {"user": user}

class GameRoutes(Resource):
    def get(self, user_id, difficulty):
        game = Game(userId=user_id)
        game.answer = Game.pick_word(difficulty)
        print(game.answer)
        game.save()
        return game.to_json()


api.add_resource(SignupRoutes, '/signup')
api.add_resource(LoginRoutes, '/login')
api.add_resource(UserRoutes, '/user/<user_id>')
api.add_resource(GameRoutes, '/game/<user_id>/<difficulty>')


if __name__ == '__main__':
    app.run(debug=True)