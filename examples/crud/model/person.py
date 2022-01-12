from pf_flask_db.pf_app_database import app_db
from pf_flask_db.pf_app_model import AppModel


class Person(AppModel):
    first_name = app_db.Column(app_db.String(150), nullable=False)
    last_name = app_db.Column(app_db.String(150))
    email = app_db.Column(app_db.String(120), nullable=False)
    age = app_db.Column(app_db.Integer)
    income = app_db.Column(app_db.Float, default=0)

