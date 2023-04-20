#from marshmallow import Schema, fields, validate
#from marshmallow.decorators import post_load
from main.models.nutritional_record_model import NutritionalRecordModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from main.maps.user_schema import UserSchema
from main.maps.food_schema import FoodSchema


'''class NutritionalRecordSchema(Schema):
    id = fields.Int(dump_only = True)
    user_id = fields.Int(required = True)
    date = fields.DateTime(required = True)
    food_id = fields.Int(required = True)
    glucose_value = fields.Int(required = True)
    user = fields.Nested('users', many = True, exclude = ('nutritional_record',))
    #food = fields.Nested('foods', many = True, exclude = ('nutritional_record',))


    @post_load
    def make_nutritional_record(self, data, **kwargs):
        return NutritionalRecordModel(**data)'''


class NutritionalRecordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NutritionalRecordModel
        load_instance = True
        include_relationships = True
        include_fk = True

    users = fields.Nested((UserSchema), exclude = ('nutritional_records', 'messages_sent', 'messages_recept',))
    foods = fields.Nested((FoodSchema), exclude = ('nutritional_records',))

