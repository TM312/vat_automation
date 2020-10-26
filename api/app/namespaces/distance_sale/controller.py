from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import DistanceSale
from . import distance_sale_dto, distance_sale_sub_dto, distance_sale_admin_dto, distance_sale_history_dto
from .service import DistanceSaleService


from app.namespaces.utils.decorators import login_required, accepted_u_types


ns = Namespace("DistanceSale", description="DistanceSale Related Operations")  # noqa
ns.add_model(distance_sale_sub_dto.name, distance_sale_sub_dto)
ns.add_model(distance_sale_dto.name, distance_sale_dto)
ns.add_model(distance_sale_admin_dto.name, distance_sale_admin_dto)
ns.add_model(distance_sale_history_dto.name, distance_sale_history_dto)


@ns.route("/")
class DistanceSaleResource(Resource):
    """DistanceSales"""
    @login_required
    @ns.marshal_list_with(distance_sale_dto, envelope='data')
    def get(self) -> List[DistanceSale]:
        """Get all DistanceSales"""
        return DistanceSaleService.get_all()

    @login_required
    @ns.expect(distance_sale_dto, validate=True)
    @ns.marshal_with(distance_sale_dto)
    def post(self) -> DistanceSale:
        """Create a Single DistanceSale"""
        return DistanceSaleService.create(request.parsed_obj)


@ns.route("/<string:distance_sale_public_id>")
@ns.param("distance_sale_public_id", "DistanceSale database ID")
class DistanceSaleIdResource(Resource):
    @login_required
    @ns.marshal_with(distance_sale_dto, envelope='data')
    def get(self, distance_sale_public_id: str) -> DistanceSale:
        """Get Single DistanceSale"""
        return DistanceSaleService.get_by_public_id(distance_sale_public_id)


    @login_required
    def delete(self, distance_sale_public_id: str) -> Response:
        """Delete Single DistanceSale"""
        from flask import jsonify

        public_id = DistanceSaleService.delete_by_public_id(distance_sale_public_id)
        return jsonify(dict(status="Success", public_id=public_id))

    @login_required
    @ns.expect(distance_sale_dto, validate=True)
    @ns.marshal_with(distance_sale_dto)
    def put(self, distance_sale_public_id: str) -> DistanceSale:
        """Update Single DistanceSale"""
        data_changes: DistanceSaleInterface = request.json
        return DistanceSaleService.update_by_public_id(distance_sale_public_id, data_changes)


@ns.route("/seller_firm/<string:seller_firm_public_id>")
class DistanceSaleSellerFirmPublicIdResource(Resource):
    """ Create Distance Sale for a Specific Seller Firm based on its Public ID"""

    # @ns.expect(distance_sale_dto, validate=True)
    @login_required
    @ns.marshal_with(distance_sale_sub_dto, envelope='data')
    def post(self, seller_firm_public_id: str) -> DistanceSale:
        return DistanceSaleService.process_single_submit(seller_firm_public_id, distance_sale_data=request.json)
