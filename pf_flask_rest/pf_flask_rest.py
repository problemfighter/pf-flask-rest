from pf_flask_rest.common.pffr_exception_handler import pffr_exception_handler
from pf_flask_rest_com.common.pffr_exception import PFFRCException


class PFFlaskRest:

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        if app:
            app.register_error_handler(PFFRCException, pffr_exception_handler.response_global_exception)


pf_flask_rest = PFFlaskRest()
