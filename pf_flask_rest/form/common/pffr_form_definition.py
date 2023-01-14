from pf_flask_rest.form.common.pffr_field_data import FieldData


class FormDefinition:
    is_validation_error: bool = False
    _field_datatype_dict: dict = {}
    filtered_field_dict: dict = {}
    field_dict: dict = {}
    validation_errors: list = []

    def init_fields(self, declared_fields: dict = None):
        self.init_all()
        for field_name in declared_fields:
            field_def = declared_fields[field_name]
            if not field_def.dump_only:
                self._set_field_definition(field_def)

    def init_all(self):
        self._field_datatype_dict = {}
        self.filtered_field_dict = {}
        self.field_dict = {}
        self.is_validation_error = False
        self.validation_errors = []

    def set_field_errors(self, errors: dict):
        self.is_validation_error = True
        for field_name in errors:
            if hasattr(self, field_name):
                field_definition = getattr(self, field_name)
                field_definition.errors = errors[field_name]
                field_definition.has_error = True

    def set_model_value(self, model):
        for field_name in self._field_datatype_dict:
            if hasattr(self, field_name) and hasattr(model, field_name):
                model_data = getattr(model, field_name)
                field_definition = getattr(self, field_name)
                field_definition.value = model_data

    def set_dict_value(self, values: dict):
        for field_name in self._field_datatype_dict:
            if field_name in values:
                model_data = values[field_name]
                field_definition = getattr(self, field_name)
                field_definition.value = model_data

    def cast_set_request_value(self, values: dict):
        for field_name in self._field_datatype_dict:
            if field_name in values and hasattr(self, field_name):
                datatype = self._field_datatype_dict[field_name]
                self._cast_value(datatype, values[field_name], field_name)

    def add_validation_error(self, error: str):
        self.is_validation_error = True
        self.validation_errors.append(error)
        return self

    def _set_field_definition(self, field):
        if field.name:
            setattr(self, field.name, self._init_field_definition(field))

    def _init_field_definition(self, field):
        definition = FieldData()
        definition.name = field.name
        definition.required = field.required
        definition = self._set_field_value(field, definition)
        data_type = field.__class__.__name__
        definition.dataType = data_type
        self._field_datatype_dict[definition.name] = data_type
        definition.process_data(field)
        return definition

    def _set_field_value(self, field, definition: FieldData):
        if field.default:
            definition.value = field.default
        return definition

    def _cast_value(self, datatype, value, field_name):
        definition = getattr(self, field_name)
        if datatype == "Integer":
            value = self._cast_int(value, field_name)
        elif datatype == "Float":
            value = self._cast_float(value, field_name)
        elif datatype == "Boolean":
            value = self._cast_boolean(value, field_name)
        elif datatype == "DateTime" or datatype == "Date":
            if not value:
                value = None
        elif not definition.required:
            self.filtered_field_dict[field_name] = value
        elif definition.required and value != "":
            self.filtered_field_dict[field_name] = value

        self.field_dict[field_name] = value
        definition.value = value

    def _cast_int(self, value, field_name):
        if value != "":
            value = int(value)
            self.filtered_field_dict[field_name] = value
        return value

    def _cast_float(self, value, field_name):
        if value != "":
            value = float(value)
            self.filtered_field_dict[field_name] = value
        return value

    def _cast_boolean(self, value, field_name):
        value = bool(value)
        self.filtered_field_dict[field_name] = value
        return value


