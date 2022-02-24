

class FieldData(object):
    name: str = None
    label: str = None
    inputType: str = None
    dataType: str = None
    value = ""
    default = None
    placeholder = None
    errors: str = None
    required: bool = False
    has_error: bool = False
    helpText: str = None
    topAttr: str = ""
    inputAttr: str = ""
    topAttrClass: str = ""
    inputAttrClass: str = ""

    def process_data(self, field, data_type):
        self._process_metadata(field.metadata)
        self._process_attr(["topAttr", "inputAttr"])

    def _process_metadata(self, metadata: dict):
        for data in metadata:
            if hasattr(self, data):
                setattr(self, data, metadata[data])
            elif data == 'type':
                self.inputType = metadata[data]

    def _process_attr(self, attrs: list):
        for field in attrs:
            field_data = getattr(self, field)
            if field_data and isinstance(field_data, dict):
                html_attr = ""
                for attr in field_data:
                    if attr == 'class':
                        setattr(self, field + "Class", str(field_data[attr]))
                    else:
                        html_attr += "" + attr + '="' + str(field_data[attr]) + '" '
                setattr(self, field, html_attr.strip())

