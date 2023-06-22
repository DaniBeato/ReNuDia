from .. import db
from .. models.user_model import UserModel
from werkzeug.security import generate_password_hash


class UserRepository:
    def __init__(self):
        self.users = UserModel

    def get_all(self):
        return self.users.query.all()

    def get_by_id(self, id):
        return self.users.query.get(id)

    def get_by_username(self, username):
        return self.users.query.filter_by(name=username).all()

    def get_by_email(self, email):
        return self.users.query.filter_by(email=email).first()

    def get_diabetics_without_nutritionist(self):
        return self.users.query.filter_by(rol="diabetic", inscription_diabetic=None).all()



    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, id, data):
        user = self.users.query.get(id)
        for key, value in data:
            if key == 'password':
                setattr(user, key, generate_password_hash(value))
            else:
                setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, id):
        user = self.users.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return user