from flask import render_template
from pf_flask_rest.form.pf_app_form_def import FormBaseDef


class TemplateHelper:

    def render(self, name, params={}, form: FormBaseDef = None):
        if form and form.definition:
            params["form"] = form.definition
        return render_template(f"{name}.html", **params)
