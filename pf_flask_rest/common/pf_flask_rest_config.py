class PFFRMessageConfig:
    invalid_request_data = "Invalid Request Data"
    validation_error = "Validation Error!"
    unknown_error = "Unknown Error Occurred!"


class PFFRConfig:
    auth_redirect_url = "/login"
    forbidden_redirect_url = "/not-allowed"
    api_url_start_with = "api"
    json_root_node = "data"

    # API Config
    get_page_param: str = "page"
    item_per_page_param: str = "per-page"
    sort_field_param: str = "sort-field"
    sort_order_param: str = "sort-order"
    search_field_param: str = "search"
    sort_default_order: str = "desc"
    sort_default_field: str = "id"
    total_item_per_page: int = 25
