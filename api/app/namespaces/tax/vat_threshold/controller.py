from typing import List
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import VatThreshold
from . import vat_threshold_dto
from .service import VatThresholdService

from app.namespaces.utils.decorators import login_required, employer_required


ns = Namespace("VatThreshold", description="Vat Threshold Related Operations")  # noqa
ns.add_model(vat_threshold_dto.name, vat_threshold_dto)


@ns.route("/")
class VatThresholdResource(Resource):
    """VatThresholds"""
    @ns.marshal_list_with(vat_threshold_dto, envelope='data')
    def get(self) -> List[VatThreshold]:
        """Get all VatThresholds"""
        return VatThresholdService.get_all()

    @ns.expect(vat_threshold_dto, validate=True)
    @ns.marshal_with(vat_threshold_dto)
    def post(self) -> VatThreshold:
        """Create a Single VatThreshold"""
        return VatThresholdService.create(request.parsed_obj)


@ns.route("/<int:vat_threshold_id>")
@ns.param("vat_threshold_id", "VatThreshold database ID")
class VatThresholdIdResource(Resource):
    def get(self, vat_threshold_id: int) -> VatThreshold:
        """Get Single VatThreshold"""
        return VatThresholdService.get_by_id(vat_threshold_id)

    def delete(self, vat_threshold_id: int) -> Response:
        """Delete Single VatThreshold"""
        from flask import jsonify

        id = VatThresholdService.delete_by_id(vat_threshold_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(vat_threshold_dto, validate=True)
    @ns.marshal_with(vat_threshold_dto)
    def put(self, vat_threshold_id: int) -> VatThreshold:
        """Update Single VatThreshold"""

        data_changes: VatThresholdInterface = request.parsed_obj
        return VatThresholdService.update(vat_threshold_id, data_changes)
