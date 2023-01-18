from flask import redirect, flash
from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest.common.pf_flask_rest_config import PFFRConfig
from pf_flask_rest.form.pf_app_form_def import FormBaseDef
from pf_flask_rest.helper.pf_flask_crud_helper import CRUDHelper
from pf_flask_rest.helper.pf_flask_template_helper import TemplateHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor


class FormCRUDHelper:
    model: BaseModel = None
    crud_helper = CRUDHelper()
    request_processor = RequestProcessor()
    template_helper: TemplateHelper = None

    def __init__(self, model: BaseModel, template_helper: TemplateHelper = None):
        self.model = model
        if not template_helper:
            template_helper = TemplateHelper()
        self.template_helper = template_helper

    def save(self, form_def: FormBaseDef, data: dict = None):
        if data:
            model = self.request_processor.populate_model(data, form_def)
        else:
            model = form_def.get_model()
        if model:
            model.save()
        return model

    def form_create(self, view_name: str, form_def: FormBaseDef, redirect_url=None, data: dict = None, params={}, response_message: str = "Successfully created!"):
        if form_def.is_post_request() and form_def.is_valid_data():
            model = self.save(form_def=form_def, data=data)
            flash(response_message, "success")
            if model and redirect_url:
                return redirect(redirect_url)
            if model:
                return model
        return self.template_helper.render(view_name, form=form_def, params=params)

    def update(self, form_def: FormBaseDef, existing_model=None, data: dict = None, query=None):
        if not existing_model:
            existing_model = self.crud_helper.get_by_id(self.model, form_def.get_value("id"), exception=True, query=query)

        if data:
            model = self.request_processor.populate_model(data, form_def, instance=existing_model)
        else:
            model = form_def.get_model(existing_model=existing_model)

        model.save()
        return model

    def form_update(self, view_name: str, form_def: FormBaseDef, display_def: FormBaseDef = None, redirect_url=None, existing_model=None, form_model=None, model_id: int = None, data: dict = None, query=None, params={}, response_message: str = "Successfully updated!"):
        if form_def.is_post_request() and form_def.is_valid_data():
            model = self.update(form_def=form_def, existing_model=existing_model, data=data, query=query)
            flash(response_message, "success")
            if model and redirect_url:
                return redirect(redirect_url)
            if model:
                return model
        elif form_def.is_get_request():
            if not form_model and model_id:
                form_model = self.details(model_id=model_id)
            if not form_model:
                flash('Invalid data', 'error')
                if redirect_url:
                    return redirect(redirect_url)

            if display_def:
                form_def.set_dict_value(display_def.dump(form_model))
                if hasattr(form_model, "id"):
                    form_def.set_value("id", form_model.id)
            else:
                form_def.set_model_value(form_model)
        if isinstance(params, dict):
            params["isEdit"] = True
        return self.template_helper.render(view_name, form=form_def, params=params)

    def form_delete(self, model_id: int, redirect_url: str, response_message: str = "Successfully deleted!", query=None):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, exception=False, query=query)
        if not existing_model:
            flash('Invalid data', 'error')
            return redirect(redirect_url)
        existing_model.isDeleted = True
        existing_model.save()
        flash(response_message, 'success')
        return redirect(redirect_url)

    def form_restore(self, model_id: int):
        existing_model = self.crud_helper.get_by_id(self.model, model_id, exception=False, is_deleted=True)
        if not existing_model:
            return False
        existing_model.isDeleted = False
        existing_model.save()
        return True

    def details(self, model_id: int, query=None):
        return self.crud_helper.get_by_id(self.model, model_id, exception=False, query=query)

    def render_view(self, view_name, params: dict = {}):
        return self.template_helper.render(view_name, params=params)

    def form_details(self, view_name, model_id: int, redirect_url: str, display_def: FormBaseDef = None, params: dict = {}, query=None):
        data = self.details(model_id, query=query)
        if not data:
            return redirect(redirect_url)
        if display_def:
            data = display_def.dump(data)
        params.update({"data": data})
        return self.template_helper.render(view_name, params=params)

    def paginated_list(self, query=None, search_fields: list = None,
                       sort_default_field=PFFRConfig.sort_default_field,
                       sort_default_order=PFFRConfig.sort_default_order,
                       item_per_page=PFFRConfig.total_item_per_page,
                       ):
        return self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields, sort_default_field=sort_default_field,
            sort_default_order=sort_default_order, item_per_page=item_per_page
        )

    def form_paginated_list(self, view_name, query=None, search_fields: list = None,
                            sort_default_field=PFFRConfig.sort_default_field,
                            sort_default_order=PFFRConfig.sort_default_order,
                            item_per_page=PFFRConfig.total_item_per_page,
                            params: dict = {}
                            ):
        response = self.paginated_list(
            query=query,
            search_fields=search_fields,
            sort_default_field=sort_default_field,
            sort_default_order=sort_default_order,
            item_per_page=item_per_page,
        )
        params.update({"table": response})
        return self.template_helper.render(view_name, params=params)

    def form_list(self, query=None, search_fields: list = None, search_text: str = None, sort_default_field=PFFRConfig.sort_default_field, response_dto: APIPrimeDef = None):
        result = self.crud_helper.list(
            model=self.model, query=query, search_fields=search_fields,
            enable_sort=True, enable_pagination=False, search_text=search_text,
            sort_default_order=sort_default_field
        )
        if response_dto:
            return response_dto.dump(result, many=True)
        return result
