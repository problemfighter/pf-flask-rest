from marshmallow import missing, ValidationError
from werkzeug.utils import redirect
from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.api.pf_app_api_def import APIBaseDef
from pf_flask_rest.form.common.pffr_form_definition import FormDefinition
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest_com.common.pffr_exception import PFFRCException
from pf_flask_rest_com.pf_flask_request_helper import RequestHelper


class FormAction(APIBaseDef):
    definition: FormDefinition
    request_processor: RequestProcessor = RequestProcessor()
    request_helper: RequestHelper = RequestHelper()

    def cast_and_set_value(self, form_data):
        self.definition.cast_set_request_value(form_data)
        self.set_property()

    def is_valid_data(self) -> bool:
        form_data = self.get_requested_raw_data()
        if form_data and self.definition:
            self.cast_and_set_value(form_data)
            try:
                form_data = self.get_requested_data()
                self.cast_and_set_value(form_data)
                return True
            except PFFRCException as e:
                if e.messageResponse and e.messageResponse.error:
                    self.definition.set_field_errors(e.messageResponse.error)
            except ValidationError as e:
                errors = {}
                if e and e.messages_dict and isinstance(e.messages_dict, dict):
                    for name, error in e.messages_dict.items():
                        errors[name] = ', '.join(error)
                self.definition.set_field_errors(errors)
        return False

    def is_post_request(self) -> bool:
        return self.request_helper.is_post()

    def is_get_request(self) -> bool:
        return self.request_helper.is_get()

    def get_model(self, existing_model=None):
        try:
            return self.request_processor.populate_model(self.definition.filtered_field_dict, self, instance=existing_model)
        except PFFRCException as e:
            if e.messageResponse and e.messageResponse.error:
                self.definition.set_field_errors(e.messageResponse.error)
                return redirect(self.request_helper.get_current_url())

    def set_model_data(self, model: BaseModel):
        self.definition.set_model_value(model)

    def get_requested_data(self):
        return self.request_processor.get_form_data(api_def=self, load_only=True, is_validate=True)

    def get_requested_raw_data(self):
        return self.request_helper.form_and_file_data()

    def set_property(self):
        for field_name in self.fields:
            value = None
            if field_name in self.definition.filtered_field_dict:
                value = self.definition.filtered_field_dict[field_name]
            else:
                field_def = self.fields[field_name]
                if self.fields[field_name].default != missing:
                    value = field_def.default
            setattr(self, field_name, value)
