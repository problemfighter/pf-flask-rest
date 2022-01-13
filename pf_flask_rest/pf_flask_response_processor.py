from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest_com.data.pffrc_response_data import PFFRCMessageResponse, PFFRCDataResponse
from pf_flask_rest_com.data.pffrc_response_status import PFFRCResponseStatus, PFFRCResponseCode
from pf_flask_rest_com.pf_flask_response_helper import ResponseHelper


class ResponseProcessor:
    response_helper = ResponseHelper()
    headers: dict = None

    def add_custom_header(self, key: str, value):
        if not self.headers:
            self.headers = {}
        self.headers[key] = value

    def message(self, message: str, status: str, code: str, http_code=200):
        message_response = PFFRCMessageResponse()
        message_response.message = message
        message_response.status = status
        message_response.code = code
        return self.response_helper.json_response(message_response.to_dict(), http_code, self.headers)

    def success_message(self, message: str, code: str = PFFRCResponseCode.success, http_code=200):
        return self.message(message, PFFRCResponseStatus.success, code, http_code)

    def error_message(self, message: str, code: str = PFFRCResponseCode.error, http_code=200):
        return self.message(message, PFFRCResponseStatus.error, code, http_code)

    def data_response(self, model: BaseModel, response_def: APIPrimeDef, many=False, status: str = PFFRCResponseStatus.success, code: str = PFFRCResponseCode.success, http_code=200):
        data_response = PFFRCDataResponse()
        data_response.status = status
        data_response.code = code
        data_response.add_data(model, response_def, many)
        return self.response_helper.json_response(data_response.to_dict(), http_code, self.headers)

    def paginate_response(self):
        pass

    def list_response(self):
        pass

    def dict_response(self):
        pass




