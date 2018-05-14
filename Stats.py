from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
db = MongoEngine()

class Stats(db.Document):
    userId = db.StringField(required=True)
    wins = db.IntField()
    loses = db.IntField()
    favoriteLetters = db.DictField()