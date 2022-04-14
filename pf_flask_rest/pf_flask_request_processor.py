from flask import sessions
from marshmallow import ValidationError, EXCLUDE
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest.common.pf_flask_rest_config import PFFRMessageConfig, PFFRConfig
from pf_flask_rest.common.pffr_exception_handler import pffr_exception_handler
from pf_flask_rest_com.common.pffr_exception import pffrc_exception
from pf_flask_rest_com.data.pffrc_response_status import PFFRCResponseCode
from pf_flask_rest_com.pf_flask_request_helper import RequestHelper


class RequestProcessor:

    request_helper: RequestHelper = RequestHelper()

    def validate_data(self, data: dict, api_def: APIPrimeDef, session=sessions, unknown=EXCLUDE):
        try:
            api_def.unknown = unknown
            errors = api_def.validate(data, session=session)
            if errors:
                errors = pffr_exception_handler.process_validation_error(errors)
                raise pffrc_exception.error_details_exception(
                    message=PFFRMessageConfig.validation_error,
                    details=errors
                )
            return data
        except ValidationError as error:
            errors = pffr_exception_handler.process_validation_error(error.messages)
            raise pffrc_exception.error_details_exception(
                message=PFFRMessageConfig.validation_error,
                details=errors
            )

    def populate_model(self, data: dict, api_def: APIPrimeDef, session=sessions, instance=None):
        try:
            return api_def.load(data, session=session, instance=instance, unknown=EXCLUDE)
        except ValidationError as error:
            errors = pffr_exception_handler.process_validation_error(error.messages)
            raise pffrc_exception.error_details_exception(
                message=PFFRMessageConfig.validation_error,
                details=errors
            )

    def get_rest_json_data(self, api_def: APIPrimeDef, is_validate=True):
        json_obj = self.request_helper.json_data()
        if not json_obj or PFFRConfig.json_root_node not in json_obj:
            raise pffrc_exception.error_message_exception(
                PFFRMessageConfig.invalid_request_data, code=PFFRCResponseCode.error
            )
        json_obj = json_obj[PFFRConfig.json_root_node]
        if is_validate:
            self.validate_data(json_obj, api_def)
        return json_obj

    def get_form_data(self, api_def: APIPrimeDef, is_validate=True, is_populate_model=False):
        form_data = self.request_helper.form_and_file_data()
        if not form_data:
            raise pffrc_exception.error_message_exception(
                PFFRMessageConfig.invalid_request_data, code=PFFRCResponseCode.error
            )
        if is_validate:
            model = self.validate_data(form_data, api_def)
            if is_populate_model:
                return model
        return form_data
