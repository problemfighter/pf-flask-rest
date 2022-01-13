from flask import Blueprint
from examples.crud.service.person_service import PersonService

person_controller = Blueprint("person_controller", __name__, url_prefix="/api/v1/person")
person_service = PersonService()


@person_controller.route("/create", methods=['POST'])
def create():
    return person_service.create()


@person_controller.route("/details-response-create", methods=['POST'])
def details_response_create():
    return person_service.details_response_create()


@person_controller.route("/details/<int:id>", methods=['GET'])
def details(id: int):
    return person_service.details(id)


@person_controller.route("/update", methods=['POST'])
def update():
    return person_service.update()


@person_controller.route("/delete/<int:id>", methods=['DELETE'])
def delete(id: int):
    return person_service.delete(id)


@person_controller.route("/restore/<int:id>", methods=['GET'])
def restore(id: int):
    return person_service.restore(id)


@person_controller.route("/list", methods=['GET'])
def list():
    return person_service.list()
