from marshmallow import fields
from examples.model.person import Person
from pf_flask_rest.api.pf_app_api_def import APIAppDef


class PersonDetailsDTO(APIAppDef):
    class Meta:
        model = Person
        load_instance = True

    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=None)
    email = fields.Email(required=True, error_messages={"required": "Please enter first name"})
    age = fields.Integer(allow_none=None)
    income = fields.Float(allow_none=None)
