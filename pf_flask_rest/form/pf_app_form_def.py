from pf_flask_rest.api.pf_app_api_def import APIAppDef
from pf_flask_rest.form.common.pffr_form_action import FormAction
from pf_flask_rest.form.common.pffr_form_definition import FormDefinition


class FormBaseDef(FormAction):
    definition: FormDefinition = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.definition = FormDefinition()
        self.definition.init_fields(self.declared_fields)

    def set_dict_value(self, values: dict):
        self.definition.set_dict_value(values)

    def set_model_value(self, model):
        self.definition.set_model_value(model)

    def get_value(self, key):
        if self.definition and self.definition.filtered_field_dict and key in self.definition.filtered_field_dict:
            return self.definition.filtered_field_dict[key]
        return None

    def set_value(self, field_name, value):
        if self.definition:
            self.definition.set_value(field_name, value)

    def set_field_error(self, field_name, error):
        if self.definition:
            self.definition.set_field_errors({field_name: error})

    def set_select_option(self, field_name, options: list, key_name: str, value_name: str, first_opt: str = "Select"):
        if self.definition:
            self.definition.process_and_set_option(field_name, options, key_name, value_name, first_opt)


class FormAppDef(APIAppDef, FormBaseDef):
    pass
