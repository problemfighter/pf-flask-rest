from pf_flask_rest.common.pf_flask_rest_config import PFFRConfig
from pf_flask_rest.helper.pf_flask_crud_helper import CRUDHelper
from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.pf_flask_response_processor import ResponseProcessor
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef


class RestCRUDHelper:
    model: BaseModel = None
    request_processor = RequestProcessor()
    response_processor = ResponseProcessor()
    crud_helper = CRUDHelper()

    def __init__(self, model: BaseModel):
        self.model = model

    def rest_create(self, request_def: APIPrimeDef, response_def: APIPrimeDef = None, response_message: str = "Successfully Created!"):
        data = self.request_processor.get_rest_json_data(request_def)
        model = self.request_processor.populate_model(data, request_def)
        model.save()
        if not response_def:
            return self.response_processor.success_message(response_message)
        return self.response_processor.data_response(model, response_def)

    def rest_update(self, request_def: APIPrimeDef, response_def: APIPrimeDef = None, response_message: str = "Successfully Updated!"):
        data = self.request_processor.get_rest_json_data(request_def)
        existing_model = self.crud_helper.get_by_id(self.model, data.id)
        model = self.request_processor.populate_model(data, request_def, instance=existing_model)
        model.save()
        if not response_def:
            return self.response_processor.success_message(response_message)
        return self.response_processor.data_response(model, response_def)

    def rest_delete(self, id: int, response_message: str = "Successfully Deleted!"):
        existing_model = self.crud_helper.get_by_id(self.model, id)
        existing_model.isDeleted = True
        existing_model.save()
        return self.response_processor.success_message(response_message)

    def rest_restore(self, id: int, response_message: str = "Successfully Restored!"):
        existing_model = self.crud_helper.get_by_id(self.model, id, is_deleted=True)
        existing_model.isDeleted = False
        existing_model.save()
        return self.response_processor.success_message(response_message)

    def rest_details(self, id: int, response_def: APIPrimeDef):
        existing_model = self.crud_helper.get_by_id(self.model, id)
        return self.response_processor.data_response(existing_model, response_def)

    def rest_paginated_list(self,
                            api_def: APIPrimeDef, query=None, search_fields: list = None,
                            sort_default_field=PFFRConfig.sort_default_field,
                            sort_default_order=PFFRConfig.sort_default_order,
                            item_per_page=PFFRConfig.total_item_per_page,
                            ):
        data_list = self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields, sort_default_field=sort_default_field,
            sort_default_order=sort_default_order, item_per_page=item_per_page
        )
        return self.response_processor.paginate_response(data_list, api_def)
