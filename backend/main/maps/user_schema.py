#from marshmallow import Schema, fields
#from marshmallow.decorators import post_load
from main.models.user_model import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema



'''class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    email = fields.Str(required = True)
    password = fields.Str(required = True)
    name = fields.Str(required = True)
    surname = fields.Str(required = True)
    age = fields.Int(required = True)
    weight = fields.Int(required = True)
    height = fields.Int(required = True)
    gender = fields.Bool(required = True)
    rol = fields.Bool(required = True)
    diabetes_type = fields.Str(required = True)
    doctor_license = fields.Str(required = True)
    #message = fields.Nested('messages', many = True, exclude = ('user',))
    nutritional_record = fields.Nested('nutritional_records', many = True, exclude = ('user',))
    
    
    
    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)'''



class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = UserModel
        load_instance = True
        include_relationships = True
        include_fk = True







