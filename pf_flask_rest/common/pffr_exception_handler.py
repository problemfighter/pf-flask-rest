class PFFRExceptionHandler:

    def process_validation_error(self, errors: dict):
        message_dict: dict = {}
        for message in errors:
            error_text = ""
            for text in errors[message]:
                error_text += text + " "
            message_dict[message] = error_text
        return message_dict


pffr_exception_handler = PFFRExceptionHandler()
