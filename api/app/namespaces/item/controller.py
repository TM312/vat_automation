from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from .service import ItemService
from . import Item
from . import item_dto

from ..utils.decorators import login_required, employer_required


ns = Namespace("Item", description="Item Related Operations")  # noqa
ns.add_model(item_dto.name, item_dto)


@ns.route("/")
class ItemResource(Resource):
    """Items"""
    @ns.marshal_list_with(item_dto, envelope='data')
    def get(self) -> List[Item]:
        """Get all Items"""
        return ItemService.get_all()

    @ns.expect(item_dto, validate=True)
    @ns.marshal_with(item_dto)
    def post(self) -> Item:
        """Create a Single Item"""
        return ItemService.create(request.parsed_obj)


@ns.route("/<int:item_id>")
@ns.param("item_id", "Item database ID")
class ItemIdResource(Resource):
    def get(self, item_id: int) -> Item:
        """Get Single Item"""
        return ItemService.get_by_id(item_id)

    def delete(self, item_id: int) -> Response:
        """Delete Single Item"""
        from flask import jsonify

        id = ItemService.delete_by_id(item_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(item_dto, validate=True)
    @ns.marshal_with(item_dto)
    def put(self, item_id: int) -> Item:
        """Update Single Item"""

        data_changes: ItemInterface = request.parsed_obj
        return ItemService.update(item_id, data_changes)



@ns.route("/csv")
class ItemInformationResource(Resource):
    @login_required
    #@employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        item_information_files: List[BinaryIO] = request.files.getlist("files")
        return ItemService.process_item_files_upload(item_information_files)
