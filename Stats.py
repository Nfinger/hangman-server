from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
db = MongoEngine()

class Stats(db.Document):
    userId = db.StringField(required=True)
    wins = db.IntField(default=0)
    losses = db.IntField(default=0)
    favoriteLetters = db.DictField()
    correct = db.FloatField(default=0)
    incorrect = db.FloatField(default=0)

    @staticmethod
    def return_helper(stat):
        if stat.correct == 0:
            return {
                "wins": stat.wins,
                "losses": stat.losses,
                "accuracy": 0
            }
        else:
            return {
                "wins": stat.wins,
                "losses": stat.losses,
                "accuracy": (stat.correct / (stat.correct + stat.incorrect)) * 100
            }