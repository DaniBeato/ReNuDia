from .. import db
from .. models.inscription_model import InscriptionModel


class InscriptionRepository:
    def __init__(self):
        self.inscriptions = InscriptionModel

    def get_all(self):
        return self.inscriptions.query.all()

    def get_by_id(self, id):
        return self.inscriptions.query.get(id)

    def get_by_nutritionist_and_diabetic_id(self, nutritionist_id, diabetic_id):
        return self.inscriptions.query.filter_by(
            nutritionist_id = nutritionist_id, diabetic_id = diabetic_id).first()

    def get_by_nutritionist_id(self, nutritionist_id):
        return self.inscriptions.query.filter_by(nutritionist_id = nutritionist_id).all()



    def create(self, inscription):
        db.session.add(inscription)
        db.session.commit()
        return inscription


    def update(self, id, data):
        inscription = self.inscriptions.query.get(id)
        for key, value in data:
            setattr(inscription, key, value)
        db.session.add(inscription)
        db.session.commit()
        return inscription


    def delete(self, id):
        inscription = self.inscriptions.query.get(id)
        db.session.delete(inscription)
        db.session.commit()
        return inscription, 200
