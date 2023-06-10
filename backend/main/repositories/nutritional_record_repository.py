from .. import db
from .. models.nutritional_record_model import NutritionalRecordModel


class NutritionalRecordRepository:
    def __init__(self):
        self.nutritional_records = NutritionalRecordModel

    def get_all(self):
        return self.nutritional_records.query.all()

    def get_by_id(self, id):
        return self.nutritional_records.query.get(id)


    def get_by_diabetic_id(self, diabetic_id):
        return self.nutritional_records.query.filter_by(diabetic_id = diabetic_id).all()


    def get_last_nutritional_record(self, diabetic_id):
        nutritional_records = self.get_by_diabetic_id(diabetic_id)
        nutritional_records = sorted(nutritional_records, key=lambda nutritional_record : nutritional_record['id'])
        last_nutritional_record = nutritional_records[-1]
        return last_nutritional_record

    def create(self, nutritional_record):
        db.session.add(nutritional_record)
        db.session.commit()
        return nutritional_record

    def update(self, id, data):
        nutritional_record = self.nutritional_records.query.get(id)
        for key, value in data:
            setattr(nutritional_record, key, value)
        db.session.add(nutritional_record)
        db.session.commit()
        return nutritional_record

    def delete(self, id):
        nutritional_record = self.nutritional_records.query.get(id)
        db.session.delete(nutritional_record)
        db.session.commit()
        return nutritional_record
