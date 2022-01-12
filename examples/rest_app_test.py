from flask import Flask
from pf_flask_db.pf_app_database import app_db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pf-flask-rest.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app_db.init_app(app)

with app.app_context():
    app_db.create_all()


@app.route('/')
def bismillah():
    return "PF Flask REST Example"


if __name__ == '__main__':
    app.run()
