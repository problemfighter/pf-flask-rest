from pf_py_text.pfpt_string_util import PFPTStringUtil


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
    selectOptions: dict = {}
    selectOptionHTML: str = None
    selectDefault: str = None
    isMultiSelect: bool = False
    isIgnoreLabel: bool = False

    def process_data(self, field):
        self._process_metadata(field.metadata)
        self._process_attr(["topAttr", "inputAttr"])
        self._post_process(field)

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

    def _post_process(self, field):
        self._set_label()
        self._process_enum_to_option(field)

    def _set_label(self):
        if not self.label and self.name and not self.isIgnoreLabel:
            self.label = PFPTStringUtil.human_readable(self.name)

    def _process_enum_to_option(self, field):
        if not self.selectOptions and hasattr(field, "enumType"):
            for enumItem in field.enumType:
                self.selectOptions[enumItem.value] = enumItem.name

    def is_checked(self, value):
        if self.value == value:
            return "checked"
        return ""

    def is_selected(self, value):
        if self.value == value:
            return "selected"
        return ""
