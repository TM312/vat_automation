from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from .service import ItemService
from . import Item
from . import item_dto, item_sub_dto, item_admin_dto, item_history_dto

from app.namespaces.utils.decorators import login_required, employer_required


ns = Namespace("Item", description="Item Related Operations")  # noqa
ns.add_model(item_sub_dto.name, item_sub_dto)
ns.add_model(item_dto.name, item_dto)
ns.add_model(item_admin_dto.name, item_admin_dto)
ns.add_model(item_history_dto.name, item_history_dto)


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


@ns.route("/<string:item_public_id>")
@ns.param("item_public_id", "Item database ID")
class ItemIdResource(Resource):
    def get(self, item_public_id: str) -> Item:
        """Get Single Item"""
        return ItemService.get_by_public_id(item_public_id)

    def delete(self, item_public_id: str) -> Response:
        """Delete Single Item"""
        from flask import jsonify

        id = ItemService.delete_by_public_id(item_public_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(item_dto, validate=True)
    @ns.marshal_with(item_dto)
    def put(self, item_public_id: str) -> Item:
        """Update Single Item"""

        data_changes: ItemInterface = request.parsed_obj
        return ItemService.update_by_public_id(item_public_id, data_changes)


@ns.route("/seller_firm/<string:seller_firm_public_id>")
class ItemSellerFirmPublicIdResource(Resource):
    """ Create Item for a Specific Seller Firm based on its Public ID"""

    # @ns.expect(distance_sale_dto, validate=True)
    @login_required
    @ns.marshal_with(item_sub_dto, envelope='data')
    def post(self, seller_firm_public_id: str) -> Item:
        return ItemService.process_single_submit(seller_firm_public_id, item_data=request.json)
