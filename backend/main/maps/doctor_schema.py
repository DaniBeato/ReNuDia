# from marshmallow import Schema, fields
# from marshmallow.decorators import post_load, post_dump
from main.models.doctor_model import DoctorModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields



class DoctorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DoctorModel
        load_instance = True
        include_relationships = True
        include_fk = True








