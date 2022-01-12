from examples.crud.dto.person_dto import PersonCreateDTO
from pf_flask_rest.helper.pf_flask_rest_crud_helper import RestCRUDHelper


class PersonService:

    rest_curd_helper = RestCRUDHelper()

    def create(self):
        return self.rest_curd_helper.rest_create(PersonCreateDTO())

    def update(self):
        pass

    def details(self, model_id: int):
        pass

    def delete(self, model_id: int):
        pass

    def restore(self, model_id: int):
        pass

    def list(self):
        search = []
        pass
