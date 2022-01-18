from flask import Flask
from marshmallow import fields
from pf_flask_db.pf_app_model import AppModel
from pf_flask_rest.helper.pf_flask_rest_crud_helper import RestCRUDHelper
from pf_flask_rest.api.pf_app_api_def import APIAppDef
from pf_flask_db.pf_app_database import app_db
from pf_flask_rest.pf_flask_rest import pf_flask_rest

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-rest-quick-start.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database Initialization
app_db.init_app(app)


# Person Model
class Person(AppModel):
    first_name = app_db.Column(app_db.String(150), nullable=False)
    last_name = app_db.Column(app_db.String(150))
    email = app_db.Column(app_db.String(120), nullable=False)
    age = app_db.Column(app_db.Integer)
    income = app_db.Column(app_db.Float, default=0)


# Person DTO
class PersonDTO(APIAppDef):
    class Meta:
        model = Person
        load_instance = True

    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=True)
    email = fields.Email(required=True, error_messages={"required": "Please enter first name"})
    age = fields.Integer(allow_none=True)
    income = fields.Float(allow_none=True)


# Person Update DTO with Primary Key
class PersonUpdateDTO(PersonDTO):
    class Meta:
        model = Person
        load_instance = True

    id = fields.Integer(required=True, error_messages={"required": "Please enter id"})


# Create Database Tables
with app.app_context():
    app_db.create_all()

# REST API Initialization
pf_flask_rest.init_app(app)


# Initialization Build-in REST CRUD system
rest_curd_helper = RestCRUDHelper(Person)

@app.route('/')
def bismillah():
    return "PF Flask REST Example"


# CREATE REQUEST with JSON Data
@app.route("/create", methods=['POST'])
def create():
    return rest_curd_helper.rest_create(PersonDTO())


# DETAILS by person id
@app.route("/details/<int:id>", methods=['GET'])
def details(id: int):
    return rest_curd_helper.rest_details(id, PersonDTO())


# UPDATE by person existing data
@app.route("/update", methods=['POST'])
def update():
    return rest_curd_helper.rest_update(PersonUpdateDTO())


# SOFT DELETE person entity
@app.route("/delete/<int:id>", methods=['DELETE'])
def delete(id: int):
    return rest_curd_helper.rest_delete(id)


# RESTORE SOFT DELETED person entity
@app.route("/restore/<int:id>", methods=['GET'])
def restore(id: int):
    return rest_curd_helper.rest_restore(id)


# LIST of person entity with pagination
@app.route("/list", methods=['GET'])
def list():
    search_fields = ['first_name', 'last_name', 'email']
    return rest_curd_helper.rest_paginated_list(PersonDTO(), search_fields=search_fields)


if __name__ == '__main__':
    app.run()
