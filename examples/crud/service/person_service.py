from examples.crud.dto.person_dto import PersonCreateDTO, PersonDetailsDTO, PersonTableDTO, PersonUpdateDTO
from examples.crud.model.person import Person
from pf_flask_rest.helper.pf_flask_rest_crud_helper import RestCRUDHelper


class PersonService:
    rest_curd_helper = RestCRUDHelper(Person)

    def create(self):
        return self.rest_curd_helper.rest_create(PersonCreateDTO())

    def details_response_create(self):
        return self.rest_curd_helper.rest_create(PersonCreateDTO(), response_def=PersonDetailsDTO())

    def update(self):
        return self.rest_curd_helper.rest_update(PersonUpdateDTO())

    def details(self, model_id: int):
        return self.rest_curd_helper.rest_details(model_id, PersonDetailsDTO())

    def delete(self, model_id: int):
        return self.rest_curd_helper.rest_delete(model_id)

    def restore(self, model_id: int):
        return self.rest_curd_helper.rest_restore(model_id)

    def list(self):
        search_fields = ['first_name', 'last_name', 'email']
        return self.rest_curd_helper.rest_paginated_list(PersonTableDTO(), search_fields=search_fields)
