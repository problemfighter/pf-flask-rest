from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from pf_flask_rest_com.api_def import APIDef


class PFFlaskRestDef(object):
    pass


class APIPrimeDef(PFFlaskRestDef, APIDef):
    pass


class APIBaseDef(APIPrimeDef, SQLAlchemySchema):
    pass


class APIAppDef(APIBaseDef):

    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
    uuid = fields.UUID(dump_only=True)
