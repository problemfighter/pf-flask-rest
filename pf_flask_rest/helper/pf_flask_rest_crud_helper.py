import traceback

from pf_flask_rest.common.pf_flask_rest_config import PFFRConfig
from pf_flask_rest.helper.pf_flask_crud_helper import CRUDHelper
from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.helper.pf_flask_rest_file_helper import RestFileHelper
from pf_flask_rest.pf_flask_response_processor import ResponseProcessor
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef


class RestCRUDHelper:
    model: BaseModel = None
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()
    crud_helper = CRUDHelper()
    rest_file_helper = RestFileHelper()

    def __init__(self, model: BaseModel):
        self.model = model

    def get_by_id(self, model_id, exception=True):
        return self.crud_helper.get_by_id(self.model, id=model_id, exception=exception)

    def create(self, request_def: APIPrimeDef):
        data = self.request_processor.get_rest_json_data(request_def)
        model = self.request_processor.populate_model(data, request_def)
        model.save()
        return model

    def rest_create_response(self, model, response_def: APIPrimeDef = None, response_message: str = "Successfully created!"):
        if not response_def:
            return self.response_processor.success_message(response_message)
        return self.response_processor.data_response(model, response_def)

    def rest_create(self, request_def: APIPrimeDef, response_def: APIPrimeDef = None, response_message: str = "Successfully created!"):
        model = self.create(request_def)
        return self.rest_create_response(model, response_def, response_message)

    def update(self, request_def: APIPrimeDef, existing_model=None):
        data = self.request_processor.get_rest_json_data(request_def)
        if not existing_model:
            existing_model = self.crud_helper.get_by_id(self.model, data['id'], exception=True)
        model = self.request_processor.populate_model(data, request_def, instance=existing_model)
        model.save()
        return model

    def rest_update_response(self, model, response_def: APIPrimeDef = None, response_message: str = "Successfully updated!"):
        if not response_def:
            return self.response_processor.success_message(response_message)
        return self.response_processor.data_response(model, response_def)

    def rest_update(self, request_def: APIPrimeDef, response_def: APIPrimeDef = None, response_message: str = "Successfully updated!", existing_model=None):
        model = self.update(request_def, existing_model)
        return self.rest_update_response(model, response_def, response_message)

    def rest_delete(self, model_id: int, response_message: str = "Successfully deleted!"):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, exception=True)
        existing_model.isDeleted = True
        existing_model.save()
        return self.response_processor.success_message(response_message)

    def rest_restore(self, model_id: int, response_message: str = "Successfully restored!"):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, is_deleted=True, exception=True)
        existing_model.isDeleted = False
        existing_model.save()
        return self.response_processor.success_message(response_message)

    def rest_details(self, model_id: int, response_def: APIPrimeDef):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, exception=True)
        return self.response_processor.data_response(existing_model, response_def)

    def rest_paginated_list(self,
                            response_def: APIPrimeDef, query=None, search_fields: list = None,
                            sort_default_field=PFFRConfig.sort_default_field,
                            sort_default_order=PFFRConfig.sort_default_order,
                            item_per_page=PFFRConfig.total_item_per_page,
                            ):
        data_list = self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields, sort_default_field=sort_default_field,
            sort_default_order=sort_default_order, item_per_page=item_per_page
        )
        return self.response_processor.paginate_response(data_list, response_def)

    def rest_list(self,
                  response_def: APIPrimeDef, query=None, search_fields: list = None,
                  sort_default_field=PFFRConfig.sort_default_field,
                  sort_default_order=PFFRConfig.sort_default_order
                  ):
        data_list = self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields, sort_default_field=sort_default_field,
            sort_default_order=sort_default_order, enable_pagination=False
        )
        return self.response_processor.list_response(data_list, response_def)

    def create_upload_single_file(self, request_def: APIPrimeDef, upload_path, response_def: APIPrimeDef = None, response_message: str = "Successfully created!", api_response: bool = True, form_data=None):
        model = self.rest_file_helper.create_upload_single_file(request_def, upload_path, form_data=form_data)
        if api_response:
            return self.rest_create_response(model, response_def, response_message)
        return model

    def update_upload_single_file(self, request_def: APIPrimeDef, upload_path, response_def: APIPrimeDef = None, response_message: str = "Successfully updated!", api_response: bool = True):
        model = self.rest_file_helper.update_upload_single_file(self.model, request_def, upload_path)
        if api_response:
            return self.rest_update_response(model, response_def, response_message)
        return model
