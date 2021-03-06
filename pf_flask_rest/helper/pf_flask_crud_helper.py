from sqlalchemy import or_, and_

from pf_flask_db.pf_app_model import BaseModel
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest.common.pf_flask_rest_config import PFFRConfig
from pf_flask_rest_com.common.pffr_exception import pffrc_exception
from pf_flask_rest_com.pf_flask_request_helper import RequestHelper


class CRUDHelper:

    request_helper: RequestHelper = RequestHelper()

    def get_by_id(self, model: BaseModel, id: int, is_deleted: bool = False, exception: bool = False, message: str = "Entry Not Found!"):
        result = model.query.filter(and_(model.id == id, model.isDeleted == is_deleted)).first()
        if result:
            return result
        if not result and exception:
            raise pffrc_exception.error_message_exception(message)
        return None

    def list(self,
             model: BaseModel, query=None, search_fields: list = None, enable_pagination: bool = True, enable_sort: bool = True,
             is_deleted=False, sort_default_field=PFFRConfig.sort_default_field, sort_default_order=PFFRConfig.sort_default_order,
             item_per_page=PFFRConfig.total_item_per_page, search_text: str = None
             ):
        if not query:
            query = model.query
        query = query.filter(getattr(model, "isDeleted") == is_deleted)

        if enable_sort:
            query = self.set_order_by_from_params(model, query=query, default_field=sort_default_field, default_order=sort_default_order)

        if search_fields:
            query = self.set_search_from_params(model, query=query, search_fields=search_fields, search_text=search_text)

        if enable_pagination:
            return self.set_pagination_from_params(query, item_per_page=item_per_page)

        return query.all()

    def set_order_by_from_params(self, model, query, default_field=PFFRConfig.sort_default_field, default_order=PFFRConfig.sort_default_order):
        sort_field = self.request_helper.get_query_params_value(PFFRConfig.sort_field_param, default=default_field)
        sort_order = self.request_helper.get_query_params_value(PFFRConfig.sort_order_param, default=default_order)
        if sort_order and (sort_order != "asc" and sort_order != "desc"):
            sort_order = default_order

        if sort_order == "asc":
            return query.order_by(getattr(model, sort_field).asc())
        return query.order_by(getattr(model, sort_field).desc())

    def set_pagination_from_params(self, query, item_per_page=PFFRConfig.total_item_per_page):
        page: int = self.request_helper.get_query_params_value(PFFRConfig.get_page_param, default=0, type=int)
        per_page: int = self.request_helper.get_query_params_value(PFFRConfig.item_per_page_param, default=item_per_page, type=int)
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def set_search_from_params(self, model, search_fields: list, query, search_text: str = None):
        like = []
        search = search_text
        if not search:
            search = self.request_helper.get_query_params_value(PFFRConfig.search_field_param)
        if search:
            for field in search_fields:
                like.append(getattr(model, field).ilike("%{}%".format(search)))
            if like:
                return query.filter(or_(*like))
        return query


