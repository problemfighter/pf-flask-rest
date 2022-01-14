from marshmallow import fields
from examples.form.person.person import Person
from pf_flask_rest.api.pf_app_api_def import FormAppDef


class PersonForm(FormAppDef):
    class Meta:
        model = Person
        load_instance = True

    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=None)
    email = fields.Email(required=True, error_messages={"required": "Please enter first name"})
    age = fields.Integer(allow_none=None)
    income = fields.Float(allow_none=None)


class PersonUpdateForm(PersonForm):
    class Meta:
        model = Person
        load_instance = True

    id = fields.Integer(required=True, error_messages={"required": "Please enter id"})