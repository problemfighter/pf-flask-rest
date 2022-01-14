from examples.crud.dto.person_dto import PersonCreateDTO, PersonDetailsDTO, PersonTableDTO
from examples.crud.model.person import Person
from pf_flask_rest.helper.pf_flask_rest_crud_helper import RestCRUDHelper


class PersonService:

    rest_curd_helper = RestCRUDHelper(Person)

    def create(self):
        return self.rest_curd_helper.rest_create(PersonCreateDTO())

    def details_response_create(self):
        return self.rest_curd_helper.rest_create(PersonCreateDTO(), response_def=PersonDetailsDTO())

    def update(self):
        pass

    def details(self, model_id: int):
        pass

    def delete(self, model_id: int):
        pass

    def restore(self, model_id: int):
        pass

    def list(self):
        search_fields = ['first_name', 'last_name', 'email']
        return self.rest_curd_helper.rest_paginated_list(PersonTableDTO(), search_fields=search_fields)
