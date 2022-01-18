from pf_flask_rest.form.pf_app_form_def import FormBaseDef
from pf_flask_rest.helper.pf_flask_crud_helper import CRUDHelper
from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.common.pf_flask_rest_config import PFFRConfig


class FormCRUDHelper:
    model: BaseModel = None
    crud_helper = CRUDHelper()

    def __init__(self, model: BaseModel):
        self.model = model

    def form_update(self, from_def: FormBaseDef):
        existing_model = self.crud_helper.get_by_id(self.model, from_def.id, exception=False)
        if not existing_model:
            return False

    def form_delete(self, model_id: int):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, exception=False)
        if not existing_model:
            return False
        existing_model.isDeleted = True
        existing_model.save()
        return True

    def form_restore(self, model_id: int):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, exception=False, is_deleted=True)
        if not existing_model:
            return False
        existing_model.isDeleted = False
        existing_model.save()
        return True

    def form_details(self, model_id: int):
        return self.crud_helper.get_by_id(self.model, model_id, exception=False)

    def form_paginated_list(self, query=None, search_fields: list = None,
                            sort_default_field=PFFRConfig.sort_default_field,
                            sort_default_order=PFFRConfig.sort_default_order,
                            item_per_page=PFFRConfig.total_item_per_page,
                            ):
        return self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields, sort_default_field=sort_default_field,
            sort_default_order=sort_default_order, item_per_page=item_per_page
        )

    def form_list(self, query=None, search_fields: list = None, search_text: str = None, sort_default_field=PFFRConfig.sort_default_field):
        return self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields,
            enable_sort=True, enable_pagination=False, search_text=search_text,
            sort_default_order=sort_default_field
        )
