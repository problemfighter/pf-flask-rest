from flask import Blueprint, render_template, redirect

from examples.form.person.person_form import PersonForm

person_blueprint = Blueprint(
    "person_blueprint",
    __name__,
    url_prefix="/person",
    static_folder="person-static",
    static_url_path="person-static",
    template_folder="person-template"
)


@person_blueprint.route("/create-form", methods=['POST', 'GET'])
def create_form():
    form = PersonForm()
    if form.is_post_request() and form.is_valid_data():
        model = form.get_model()
        model.save()
        return redirect("/person/list")
    return render_template("create-form.html", form=form.definition)


@person_blueprint.route("/list")
def list():
    return render_template("list.html")




