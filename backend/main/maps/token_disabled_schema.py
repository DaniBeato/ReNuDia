from main.models.token_disabled_model import TokenDisabledModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema



class TokenDisabledSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TokenDisabledModel
        load_instance = True
        include_relationships = True
        include_fk = True