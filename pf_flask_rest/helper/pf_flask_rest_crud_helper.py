from pf_flask_rest.pf_flask_request_processor import RequestProcessor

from pf_flask_rest.api.pf_app_api_def import APIPrimeDef


class RestCRUDHelper:
    request_processor = RequestProcessor()

    def rest_create(self, api_def: APIPrimeDef):
        data = self.request_processor.get_rest_json_data(api_def)
        print(data)

    def rest_update(self, api_def: APIPrimeDef):
        pass

    def rest_delete(self, api_def: APIPrimeDef):
        pass

    def rest_details(self, api_def: APIPrimeDef):
        pass

    def rest_list(self, api_def: APIPrimeDef):
        pass
