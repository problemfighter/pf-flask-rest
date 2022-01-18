from marshmallow import fields
from examples.form.person.person import Person
from pf_flask_rest.form.pf_app_form_def import FormAppDef


class PersonForm(FormAppDef):
    class Meta:
        model = Person
        load_instance = True

    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=True, default="NA")
    email = fields.Email(required=True, error_messages={"required": "Please enter email"})
    age = fields.Integer(required=True, error_messages={"required": "Please enter age"})
    income = fields.Float(allow_none=True)


class PersonUpdateForm(PersonForm):
    class Meta:
        model = Person
        load_instance = True

    id = fields.Integer(required=True, error_messages={"required": "Please enter id"})
