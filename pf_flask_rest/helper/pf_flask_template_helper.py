import json
from flask import render_template, get_flashed_messages
from pf_flask_rest.form.pf_app_form_def import FormBaseDef


class TemplateUtil:

    def get_status_message(self):
        messages = get_flashed_messages(with_categories=True)
        response = {}
        message_stack = ""
        for status, message in messages:
            if not status or not message:
                continue
            if status == "success":
                response["isSuccess"] = True
            elif "isSuccess" not in response:
                response["isSuccess"] = False

            if message:
                message_stack += message + " "

        if response and message_stack:
            response["message"] = message_stack.strip()
        return json.dumps(response)


template_util = TemplateUtil()


class TemplateHelper:

    def render(self, name, params={}, form: FormBaseDef = None):
        if form and form.definition:
            params["form"] = form.definition
        params["util"] = template_util
        return render_template(f"{name}.html", **params)
