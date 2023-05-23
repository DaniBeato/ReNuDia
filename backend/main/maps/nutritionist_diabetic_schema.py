from main.models import NutritionistDiabeticModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from main.maps.user_schema import UserSchema


class NutritionistDiabeticSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NutritionistDiabeticModel
        load_instance = True
        include_relationships = True
        include_fk = True



    user_nutritionist = fields.Nested((UserSchema), exclude = ('nutritionist',))
    user_diabetic = fields.Nested((UserSchema), exclude = ('diabetic',))