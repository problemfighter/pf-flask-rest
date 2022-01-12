from flask import Flask

from examples.crud.controller.contact_controller import person_controller
from pf_flask_db.pf_app_database import app_db
from pf_flask_rest.pf_flask_rest import pf_flask_rest

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-rest.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app_db.init_app(app)

with app.app_context():
    app_db.create_all()

app.register_blueprint(person_controller)
pf_flask_rest.init_app(app)


@app.route('/')
def bismillah():
    return "PF Flask REST Example"


if __name__ == '__main__':
    app.run()
