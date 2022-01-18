### In the name of God, the Most Gracious, the Most Merciful.

# PF-Flask-REST

Problem Fighter Flask Representational State Transfer (PF-Flask-REST) library is build for rapid API development & Monolithic 
application development. It has useful class and methods which allow developer to build set of CRUD API end points within 5 minutes. 
Automatic Data validation, Data processing, & Data CRUD with Database. Let's see what is waiting for us.



<br/><br/><br/>
## Documentation
Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):
```bash
pip install -U PF-Flask-REST
```

*Codes*
```python
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
```

## PF Flask REST Test the API end points

Open POSTMan or any other REST API client and try below end-points

* *Create End-Points (POST, application/json) :* http://127.0.0.1:5000/create
* *Request Payload :*
```json
{
    "data": {
    	"first_name": "hmtmcse",
    	"last_name": "com",
    	"email": "hmtmcse.com@gmail.com",
    	"age": 7,
    	"income": 5000
    }
}
```

<br/><br/>

* *Details End-Points (GET):* http://127.0.0.1:5000/details/<id>
* *Update End-Points (POST, application/json):* http://127.0.0.1:5000/update
* *Request Payload :*
```json
{
    "data": {
    	"id": 1,
    	"first_name": "Touhid",
    	"last_name": "Mia",
    	"email": "hmtmcse.com@gmail.com",
    	"age": 7,
    	"income": 5000
    }
}
```
* *Soft Delete End-Points (DELETE):* http://127.0.0.1:5000/delete/<id>
* *Restore Soft Delete End-Points (GET):* http://127.0.0.1:5000/restore/<id>
* *List with pagination End-Points (GET):* http://127.0.0.1:5000/list
* Params
  * per-page
  * page
  * sort-field
  * sort-order
  * search


**Please find [the Documentation](https://www.hmtmcse.com/pf/pf-flask-rest/latest/quickstart) with example from [hmtmcse.com](https://www.hmtmcse.com/pf/pf-flask-rest/latest/quickstart)**


<br/><br/><br/>
## Donate
[Problem Fighter](https://www.problemfighter.com/) develops and supports PF-Flask-REST and the libraries it uses. In order to grow
the community of contributors and users, and allow the maintainers to devote more time to the projects.


<br/><br/><br/>
## Contributing
For guidance on setting up a development environment and how to make a contribution to PF-Flask-REST, see the contributing guidelines.


<br/><br/><br/>
## Links
* **Changes :** [https://opensource.problemfighter.org/flask/pf-flask-rest](https://opensource.problemfighter.org/flask/pf-flask-rest)
* **PyPI Releases :** [https://pypi.org/project/pf-flask-rest](https://pypi.org/project/pf-flask-rest)
* **Source Code :** [https://github.com/problemfighter/pf-flask-rest](https://github.com/problemfighter/pf-flask-rest)
* **Issue Tracker :** [https://github.com/problemfighter/pf-flask-rest/issues](https://github.com/problemfighter/pf-flask-rest/issues)
* **Website :** [https://www.problemfighter.com/open-source](https://www.problemfighter.com/open-source)

