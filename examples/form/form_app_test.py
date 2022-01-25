from flask import Flask, redirect
from pf_flask_db.pf_app_database import app_db
from examples.form.person.person_blueprint import person_blueprint
from pf_flask_rest.pf_flask_rest import pf_flask_rest

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-form.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app_db.init_app(app)

with app.app_context():
    app_db.create_all()

app.register_blueprint(person_blueprint)
pf_flask_rest.init_app(app)


@app.route('/')
def bismillah():
    return redirect("/person")


if __name__ == '__main__':
    app.run(debug=True)
