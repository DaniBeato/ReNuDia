from .. import db
from .. models.token_disabled_model import TokenDisabledModel


class TokenDisabledRepository:
    def __init__(self):
        self.tokens_disabled = TokenDisabledModel

    def get_all(self):
        return self.tokens_disabled.query.all()

    def get_by_id(self, id):
        return self.tokens_disabled.query.get(id)

    def get_by_jti(self, jti):
        return self.tokens_disabled.query.filter_by(jti=jti).all()




    def create(self, token_disabled):
        db.session.add(token_disabled)
        db.session.commit()
        return token_disabled

    def update(self, id, data):
        token_disabled = self.tokens_disabled.query.get(id)
        for key, value in data:
            setattr(token_disabled, key, value)
        db.session.add(token_disabled)
        db.session.commit()
        return token_disabled

    def delete(self, id):
        token_disabled = self.tokens_disabled.query.get(id)
        db.session.delete(token_disabled)
        db.session.commit()
        return token_disabled
