from flask import Blueprint, render_template, redirect
from examples.form.person.person import Person
from pf_flask_rest.helper.pf_flask_form_crud_helper import FormCRUDHelper
from examples.form.person.person_form import PersonForm, PersonUpdateForm

person_blueprint = Blueprint(
    "person_blueprint",
    __name__,
    url_prefix="/person",
    static_folder="person-static",
    static_url_path="person-static",
    template_folder="person-template"
)

form_crud_helper = FormCRUDHelper(Person)


@person_blueprint.route("/create-form", methods=['POST', 'GET'])
def create_form():
    form = PersonForm()
    if form.is_post_request() and form.is_valid_data():
        model = form.get_model()
        model.save()
        return redirect("/person/list")
    return render_template("create-form.html", form=form.definition)


@person_blueprint.route("/")
@person_blueprint.route("/list")
def list():
    data_list = form_crud_helper.form_list()
    return render_template("list.html", data_list=data_list)


@person_blueprint.route("/delete/<int:id>", methods=['GET'])
def delete(id: int):
    response = form_crud_helper.form_delete(id)
    return redirect("/person/list")


@person_blueprint.route("/update/<int:id>", methods=['POST', 'GET'])
def update_form(id: int):
    form = PersonUpdateForm()
    if form.is_post_request() and form.is_valid_data():
        existing_model = form_crud_helper.form_details(id)
        if existing_model:
            model = form.get_model(existing_model=existing_model)
            model.save()
            return redirect("/person/list")
    elif form.is_get_request():
        model = form_crud_helper.form_details(id)
        if not model:
            return redirect("/person/list")
        form.set_model_data(model)
    return render_template("update-form.html", form=form.definition, id=id)
