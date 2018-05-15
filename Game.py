from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import random
import binascii
from Crypto.Cipher import AES
import base64
db = MongoEngine()

KEY = 'nate_is_the_best'
IV = 'This is an IV456'
MODE = AES.MODE_CFB
BLOCK_SIZE = 16
SEGMENT_SIZE = 128

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
    def encrypt(key, iv, plaintext):
        arr = ["0x" + elem.encode("hex") for elem in plaintext]
        return arr

    @staticmethod
    def decrypt(key, iv, encrypted_text):
        aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
        encrypted_text_bytes = binascii.a2b_hex(encrypted_text)
        decrypted_text = aes.decrypt(encrypted_text_bytes)
        decrypted_text = Game._unpad_string(decrypted_text)
        return decrypted_text

    @staticmethod
    def _pad_string(value):
        length = len(value)
        pad_size = BLOCK_SIZE - (length % BLOCK_SIZE)
        return value.ljust(length + pad_size, '\x00')

    @staticmethod
    def _unpad_string(value):
        while value[-1] == '\x00':
            value = value[:-1]
        return value


    @staticmethod
    def return_helper(game):
        return {
            "id": str(game.id),
            "answer": Game.encrypt(KEY, IV, game.answer)
        }