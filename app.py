#!flask/bin/python
import flask
import hashlib
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
            user = User.return_helper(users[0])
            stats = Stats.objects(userId=user["id"])
            user["stats"] = Stats.return_helper(stats[0])
            return {"user": user}
        else:
            return {"error": "Incorrect Password"}

class UserRoutes(Resource): 
    def get(self, user_id):
        users = User.objects(id=user_id)
        user = User.return_helper(users[0])
        stats = Stats.objects(userId=user_id)
        user["stats"] = Stats.return_helper(stats[0])
        return {"user": user}

class GameRoutes(Resource):
    def get(self, user_id, difficulty):
        game = Game(userId=user_id)
        game.answer = Game.pick_word(difficulty)
        game.save()
        return Game.return_helper(game)

class GameOverRoutes(Resource):
    def post(self, game_id):
        game_request_parser = RequestParser(bundle_errors=True)
        game_request_parser.add_argument("outcome", type=bool, required=True)
        game_request_parser.add_argument("correct", type=int, required=True)
        game_request_parser.add_argument("incorrect", type=int, required=True)
        args = game_request_parser.parse_args()
        games = Game.objects(id=game_id, finished=False)
        if len(games) == 0: 
            return "Game was already finished"
        game = games[0]
        Game(id=game_id).update(win=args["outcome"], finished=True)
        if args["outcome"]:
            Stats.objects(userId=game.userId).update_one(inc__wins=1, inc__correct=args["correct"], inc__incorrect=args["incorrect"])
        else:
            Stats.objects(userId=game.userId).update_one(inc__losses=1, inc__correct=args["correct"], inc__incorrect=args["incorrect"])
        users = User.objects(id=game.userId)
        user = User.return_helper(users[0])
        stats = Stats.objects(userId=game.userId)
        user["stats"] = Stats.return_helper(stats[0])
        return {"user": user}


api.add_resource(SignupRoutes, '/signup')
api.add_resource(LoginRoutes, '/login')
api.add_resource(UserRoutes, '/user/<user_id>')
api.add_resource(GameRoutes, '/game/<user_id>/<difficulty>')
api.add_resource(GameOverRoutes, '/game/<game_id>')


if __name__ == '__main__':
    app.run(debug=True)