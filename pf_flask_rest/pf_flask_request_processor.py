from pf_flask_rest.api.pf_app_api_def import PFFlaskRestDef
from pf_flask_rest_com.pf_flask_request_helper import RequestHelper


class RequestProcessor:

    request_helper: RequestHelper = RequestHelper()

    def validate_data(self, data: dict, api_def: PFFlaskRestDef):
        pass

    def populate_model(self, data: dict, api_def: PFFlaskRestDef, session=None, instance=None):
        pass

    def get_rest_json_data(self, api_def: PFFlaskRestDef):
        json_obj = self.request_helper.json_data()

    def validate_and_get_form_data(self):
        pass
