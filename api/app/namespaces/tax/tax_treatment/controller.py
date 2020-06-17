from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import TaxTreatment
from . import tax_treatment_dto
from .service import TaxTreatmentService

from ...utils.decorators import login_required, employer_required


ns = Namespace("TaxTreatment", description="TaxTreatment Related Operations")  # noqa
ns.add_model(tax_treatment_dto.name, tax_treatment_dto)


@ns.route("/")
class TaxTreatmentResource(Resource):
    """TaxTreatments"""
    @ns.marshal_list_with(tax_treatment_dto, envelope='data')
    def get(self) -> List[TaxTreatment]:
        """Get all TaxTreatments"""
        return TaxTreatmentService.get_all()

    @ns.expect(tax_treatment_dto, validate=True)
    @ns.marshal_with(tax_treatment_dto)
    def post(self) -> TaxTreatment:
        """Create a Single TaxTreatment"""
        return TaxTreatmentService.create(request.parsed_obj)


@ns.route("/<string:tax_treatment_code>")
@ns.param("tax_treatment_code", "TaxTreatment database code")
class TaxTreatmentIdResource(Resource):
    def get(self, tax_treatment_code: str) -> TaxTreatment:
        """Get Single TaxTreatment"""
        return TaxTreatmentService.get_by_code(tax_treatment_code)

    def delete(self, tax_treatment_code: str) -> Response:
        """Delete Single TaxTreatment"""
        from flask import jsonify

        id = TaxTreatmentService.delete_by_code(tax_treatment_code)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(tax_treatment_dto, validate=True)
    @ns.marshal_with(tax_treatment_dto)
    def put(self, tax_treatment_code: str) -> TaxTreatment:
        """Update Single TaxTreatment"""

        data_changes: TaxTreatmentInterface = request.parsed_obj
        return TaxTreatmentService.update(tax_treatment_code, data_changes)
