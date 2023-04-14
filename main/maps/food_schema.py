from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_load
from main.models.food_model import FoodModel
#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class FoodSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    amount_sugar = fields.Int(required = True)
    nutritional_record = fields.Nested('nutritional_records', many = True, exclude = ('food',))


    @post_load
    def make_food(self, data, **kwargs):
        return FoodModel(**data)


'''class FoodSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FoodModel
        load_instance = True
        include_relationships = True
        include_fk = True'''