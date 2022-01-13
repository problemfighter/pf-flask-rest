from pf_flask_rest.pf_flask_response_processor import ResponseProcessor
from examples.crud.model.person import Person
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef


class RestCRUDHelper:
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()

    def rest_create(self, request_def: APIPrimeDef, response_def: APIPrimeDef = None, response_message: str = "Successfully Created"):
        data = self.request_processor.get_rest_json_data(request_def)
        model: Person = self.request_processor.populate_model(data, request_def)
        model.save()
        if not response_def:
            return self.response_processor.success_message(response_message)
        return self.response_processor.data_response(model, response_def)

    def rest_update(self, api_def: APIPrimeDef):
        pass

    def rest_delete(self, api_def: APIPrimeDef):
        pass

    def rest_details(self, api_def: APIPrimeDef):
        pass

    def rest_list(self, api_def: APIPrimeDef):
        pass
