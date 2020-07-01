from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import DistanceSale
from . import distance_sale_dto, distance_sale_sub_dto
from .service import DistanceSaleService


from ..utils.decorators import login_required, employer_required


ns = Namespace("DistanceSale", description="DistanceSale Related Operations")  # noqa
ns.add_model(distance_sale_dto.name, distance_sale_dto)
ns.add_model(distance_sale_sub_dto.name, distance_sale_sub_dto)


@ns.route("/")
class DistanceSaleResource(Resource):
    """DistanceSales"""
    @ns.marshal_list_with(distance_sale_dto, envelope='data')
    def get(self) -> List[DistanceSale]:
        """Get all DistanceSales"""
        return DistanceSaleService.get_all()

    @ns.expect(distance_sale_dto, validate=True)
    @ns.marshal_with(distance_sale_dto)
    def post(self) -> DistanceSale:
        """Create a Single DistanceSale"""
        return DistanceSaleService.create(request.parsed_obj)


@ns.route("/<string:distance_sale_public_id>")
@ns.param("distance_sale_public_id", "DistanceSale database ID")
class DistanceSaleIdResource(Resource):
    def get(self, distance_sale_public_id: str) -> DistanceSale:
        """Get Single DistanceSale"""
        return DistanceSaleService.get_by_id(distance_sale_public_id)

    def delete(self, distance_sale_public_id: str) -> Response:
        """Delete Single DistanceSale"""
        from flask import jsonify

        id = DistanceSaleService.delete_by_id(distance_sale_public_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(distance_sale_dto, validate=True)
    @ns.marshal_with(distance_sale_dto)
    def put(self, distance_sale_public_id: str) -> DistanceSale:
        """Update Single DistanceSale"""
        data_changes: DistanceSaleInterface = request.parsed_obj
        return DistanceSaleService.update_by_public_id(distance_sale_public_id, data_changes)




@ns.route("/csv")
class DistanceSaleInformationResource(Resource):
    @login_required
    #@employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        distance_sale_information_files: List[BinaryIO] = request.files.getlist("files")
        return DistanceSaleService.process_distance_sale_files_upload(distance_sale_information_files)
