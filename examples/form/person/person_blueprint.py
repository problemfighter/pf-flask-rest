from flask import Blueprint, render_template

person_blueprint = Blueprint(
    "person_blueprint",
    __name__,
    url_prefix="/person",
    static_folder="person-static",
    static_url_path="person-static",
    template_folder="person-template"
)


@person_blueprint.route("/create-form")
def create_form():
    return render_template("create-form.html")


