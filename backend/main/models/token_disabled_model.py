from .. import db




class TokenDisabledModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)



