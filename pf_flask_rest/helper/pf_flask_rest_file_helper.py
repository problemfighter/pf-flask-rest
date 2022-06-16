from pf_flask_file.pfff_file_upload_man import PFFFFileUploadMan
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest.helper.pf_flask_crud_helper import CRUDHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest_com.api_def import FileField
from pf_py_common.py_common import PyCommon


class RestFileHelper:
    file_upload_man = PFFFFileUploadMan()
    request_processor = RequestProcessor()
    crud_helper = CRUDHelper()

    def get_file_override_names(self, uuid, request_def: APIPrimeDef):
        override_names = {}
        for field_name in request_def.fields:
            field = request_def.fields[field_name]
            if isinstance(field, FileField):
                prefix = ""
                if field.save_prefix:
                    prefix = field.save_prefix + "-"
                override_names[field.name] = (prefix + uuid).lower()
        return override_names

    def upload_file(self, form_data, upload_path, request_def: APIPrimeDef, override_names):
        file_names = self.file_upload_man.validate_and_upload_multiple(form_data, request_def, upload_path, override_name=override_names)
        return file_names

    def process_single_file_upload(self, uuid, upload_path, request_def: APIPrimeDef, existing_model=None):
        form_data = self.request_processor.get_form_data(request_def)
        model = self.request_processor.populate_model(form_data, request_def, instance=existing_model)
        if not model.uuid:
            model.uuid = uuid
        override_names = self.get_file_override_names(uuid, request_def)
        file_names = self.upload_file(form_data, upload_path, request_def, override_names)
        for name in override_names:
            if hasattr(model, name) and name in file_names:
                file_name = file_names[name][override_names[name]]
                setattr(model, name, file_name)
        model.save()
        return model

    def create_upload_single_file(self, request_def: APIPrimeDef, upload_path):
        uuid = PyCommon.uuid()
        return self.process_single_file_upload(uuid, upload_path, request_def)

    def update_upload_single_file(self, model_class, request_def: APIPrimeDef, upload_path):
        form_data = self.request_processor.get_form_data(request_def)
        existing_model = self.crud_helper.get_by_id(model_class, form_data['id'], exception=True)
        return self.process_single_file_upload(existing_model.uuid, upload_path, request_def, existing_model=existing_model)

    def create_upload_multiple_file(self, request_def: APIPrimeDef, upload_path):
        pass

    def update_upload_multiple_file(self, request_def: APIPrimeDef, upload_path):
        pass
