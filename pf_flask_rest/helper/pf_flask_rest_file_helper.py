import os.path
from werkzeug.datastructures import FileStorage
from pf_flask_file.pfff_file_upload_man import PFFFFileUploadMan
from pf_flask_rest.api.pf_app_api_def import APIPrimeDef
from pf_flask_rest.helper.pf_flask_crud_helper import CRUDHelper
from pf_flask_rest.pf_flask_request_processor import RequestProcessor
from pf_flask_rest_com.api_def import FileField
from pf_py_common.py_common import PyCommon
from pf_py_file.pfpf_file_util import PFPFFileUtil


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

    def deal_single_file_deleted(self, override_names: dict, form_data, model, upload_path):
        for name in override_names:
            if "deletedItem" in form_data and name in form_data["deletedItem"]:
                if hasattr(model, name) and (name not in form_data or not isinstance(form_data[name], FileStorage)):
                    file_path = os.path.join(upload_path, getattr(model, name))
                    setattr(model, name, None)
                    PFPFFileUtil.delete_file(file_path)
        return model

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
        model = self.deal_single_file_deleted(override_names=override_names, form_data=form_data, model=model, upload_path=upload_path)
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
