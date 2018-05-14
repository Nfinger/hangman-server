from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from werkzeug.security import generate_password_hash, \
     check_password_hash
db = MongoEngine()

class User(db.Document):
    email = db.EmailField(required=True)
    password = db.StringField()

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(pw_hash, password):
        return check_password_hash(pw_hash, password)

    @staticmethod
    def return_helper(user):
        return {
            "email": user.email,
            "id": str(user.id)
        }