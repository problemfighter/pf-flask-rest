from pf_flask_rest.api.pf_app_api_def import APIBaseDef, APIAppDef
from pf_flask_rest.form.common.pffr_form_action import FormAction
from pf_flask_rest.form.common.pffr_form_definition import FormDefinition


class FormBaseDef(FormAction):
    definition: FormDefinition = FormDefinition()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.definition.init_fields(self.declared_fields)


class FormAppDef(APIAppDef, FormBaseDef):
    pass
