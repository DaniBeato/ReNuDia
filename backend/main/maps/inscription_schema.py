from main.models import InscriptionModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from main.maps.user_schema import UserSchema


class InscriptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InscriptionModel
        load_instance = True
        include_relationships = True
        include_fk = True



    user_nutritionist = fields.Nested((UserSchema), exclude = ('inscription_nutritionist',))
    user_diabetic = fields.Nested((UserSchema), exclude = ('inscription_diabetic',))