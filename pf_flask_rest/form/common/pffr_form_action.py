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

    def is_valid_data(self) -> bool:
        form_data = self.get_requested_data()
        if form_data and self.definition:
            try:
                self.definition.cast_set_request_value(form_data)
                self.request_processor.validate_data(self.definition.filtered_field_dict, self)
                for field in self.definition.filtered_field_dict:
                    if field in self.fields:
                        setattr(self, field, self.definition.filtered_field_dict[field])
                return True
            except PFFRCException as e:
                if e.messageResponse and e.messageResponse.error:
                    self.definition.set_field_errors(e.messageResponse.error)

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
        return self.request_helper.form_data()
