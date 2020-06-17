from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response


from . import TaxCode
from . import tax_code_dto
from .service import TaxCodeService

from ...utils.decorators import login_required, employer_required


ns = Namespace("TaxCode", description="TaxCode Related Operations")  # noqa
ns.add_model(tax_code_dto.name, tax_code_dto)


@ns.route("/")
class TaxCodeResource(Resource):
    """TaxCodes"""
    @ns.marshal_list_with(tax_code_dto, envelope='data')
    def get(self) -> List[TaxCode]:
        """Get all TaxCodes"""
        return TaxCodeService.get_all()

    @ns.expect(tax_code_dto, validate=True)
    @ns.marshal_with(tax_code_dto)
    def post(self) -> TaxCode:
        """Create a Single TaxCode"""
        return TaxCodeService.create(request.parsed_obj)


@ns.route("/<string:tax_code_code>")
@ns.param("tax_code_code", "TaxCode database code")
class TaxCodeIdResource(Resource):
    def get(self, tax_code_code: str) -> TaxCode:
        """Get Single TaxCode"""
        return TaxCodeService.get_by_code(tax_code_code)

    def delete(self, tax_code_code: str) -> Response:
        """Delete Single TaxCode"""
        from flask import jsonify

        id = TaxCodeService.delete_by_code(tax_code_code)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(tax_code_dto, validate=True)
    @ns.marshal_with(tax_code_dto)
    def put(self, tax_code_code: str) -> TaxCode:
        """Update Single TaxCode"""

        data_changes: TaxCodeInterface = request.parsed_obj
        return TaxCodeService.update(tax_code_code, data_changes)
