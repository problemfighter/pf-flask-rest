from pf_flask_rest_com.pf_flask_response_helper import response_helper

from pf_flask_rest.common.pf_flask_rest_config import PFFRMessageConfig
from pf_flask_rest_com.common.pffr_exception import PFFRCException, pffrc_exception


class PFFRExceptionHandler:

    def process_validation_error(self, errors: dict):
        message_dict: dict = {}
        for message in errors:
            error_text = ""
            for text in errors[message]:
                error_text += str(text) + " "
            message_dict[message] = error_text
        return message_dict

    def response_global_exception(self, exception: Exception):
        if isinstance(exception, PFFRCException):
            return self.get_pffrc_exception_response(exception)
        return self.get_rest_message_response(PFFRMessageConfig.unknown_error)

    def get_pffrc_exception_response(self, exception: PFFRCException):
        json_string_response = {}
        if exception.messageResponse:
            json_string_response = exception.messageResponse.to_dict()
        elif exception.error_details_exception:
            json_string_response = exception.errorResponse.to_dict()
        elif exception.message:
            json_string_response = self.get_rest_message_response(exception.message)
        else:
            json_string_response = self.get_rest_message_response(PFFRMessageConfig.unknown_error)
        return response_helper.json_string_response(json_string_response)

    def get_rest_message_response(self, message: str):
        error_exception = self.get_rest_error_exception(message)
        return error_exception.messageResponse.to_dict()

    def get_rest_error_exception(self, message: str):
        return pffrc_exception.error_message_exception(message)


pffr_exception_handler = PFFRExceptionHandler()
