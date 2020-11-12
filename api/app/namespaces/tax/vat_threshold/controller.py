from typing import List
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import VatThreshold
from . import vat_threshold_sub_dto, vat_threshold_dto, vat_threshold_admin_dto, vat_threshold_history_dto
from .service import VatThresholdService

from app.namespaces.utils.decorators import login_required, accepted_u_types


ns = Namespace("VatThreshold", description="Vat Threshold Related Operations")  # noqa
ns.add_model(vat_threshold_sub_dto.name, vat_threshold_sub_dto)
ns.add_model(vat_threshold_dto.name, vat_threshold_dto)
ns.add_model(vat_threshold_dto.name, vat_threshold_dto)
ns.add_model(vat_threshold_admin_dto.name, vat_threshold_admin_dto)
ns.add_model(vat_threshold_history_dto.name, vat_threshold_history_dto)


@ns.route("/")
class VatThresholdResource(Resource):
    """VatThresholds"""
    @login_required
    @ns.marshal_list_with(vat_threshold_sub_dto, envelope='data')
    def get(self) -> List[VatThreshold]:
        """Get all VatThresholds"""
        return VatThresholdService.get_all()

    @login_required
    @accepted_u_types('admin')
    @ns.expect(vat_threshold_dto, validate=True)
    @ns.marshal_with(vat_threshold_admin_dto)
    def post(self) -> VatThreshold:
        """Create a Single VatThreshold"""
        return VatThresholdService.create(request.json)


@ns.route("/<int:vat_threshold_id>")
@ns.param("vat_threshold_id", "VatThreshold database ID")
class VatThresholdIdResource(Resource):
    @login_required
    @ns.marshal_with(vat_threshold_dto)
    def get(self, vat_threshold_id: int) -> VatThreshold:
        """Get Single VatThreshold"""
        return VatThresholdService.get_by_id(vat_threshold_id)

    @login_required
    @accepted_u_types('admin')
    def delete(self, vat_threshold_id: int) -> Response:
        """Delete Single VatThreshold"""
        from flask import jsonify

        id = VatThresholdService.delete_by_id(vat_threshold_id)
        return jsonify(dict(status="Success", id=id))

    @login_required
    @accepted_u_types('admin')
    @ns.expect(vat_threshold_dto, validate=True)
    @ns.marshal_with(vat_threshold_dto, envelope='data')
    def put(self, vat_threshold_id: int) -> VatThreshold:
        """Update Single VatThreshold"""

        data_changes: VatThresholdInterface = request.json
        return VatThresholdService.update(vat_threshold_id, data_changes)
