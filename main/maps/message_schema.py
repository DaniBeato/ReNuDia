#from marshmallow import Schema, fields, validate
#from marshmallow.decorators import post_load
from main.models.message_model import MessageModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


'''class MessageSchema(Schema):
    id = fields.Int(dump_only = True)
    sender_id = fields.Int(required = True)
    receptor_id = fields.Int(required = True)
    message = fields.Str(required = True)
    #user = fields.Nested('users', many = True, exclude = ('message',))

    @post_load
    def make_message(self, data, **kwargs):
        return MessageModel(**data)'''


class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MessageModel
        load_instance = True
        include_relationships = True
        include_fk = True




