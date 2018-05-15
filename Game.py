from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import random
db = MongoEngine()

class Game(db.Document):
    userId = db.StringField(required=True)
    answer = db.StringField()
    guesses = db.ListField()
    win = db.BooleanField()
    finished = db.BooleanField(default=False)
    difficulty = db.StringField()

    @staticmethod
    def pick_word(difficulty):
        wordBreakup = {
            "easy": [],
            "medium": [],
            "hard": []
        }
        f = open("dictionary.txt", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for l in fl:
                if len(l) <= 4:
                    wordBreakup["easy"].append(l)
                elif len(l) <= 7:
                    wordBreakup["medium"].append(l)
                else:
                    wordBreakup["hard"].append(l)
        randIdx = random.randint(1, len(wordBreakup[difficulty]))
        return wordBreakup[difficulty][randIdx].strip()

    @staticmethod
    def encrypt(plaintext):
        arr = ["0x" + codecs.encode(elem, encoding="hex") for elem in plaintext]
        return arr

    @staticmethod
    def return_helper(game):
        return {
            "id": str(game.id),
            "answer": Game.encrypt(game.answer)
        }