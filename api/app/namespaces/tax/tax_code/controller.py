from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response


from . import TaxCode
from . import tax_code_dto
from .service import TaxCodeService

from app.namespaces.utils.decorators import login_required, accepted_u_types
from app.extensions import cache



ns = Namespace("TaxCode", description="TaxCode Related Operations")  # noqa
ns.add_model(tax_code_dto.name, tax_code_dto)


@ns.route("/")
class TaxCodeResource(Resource):
    """TaxCodes"""
    @login_required
    @ns.marshal_list_with(tax_code_dto, envelope='data')
    @cache.cached(timeout=60)
    def get(self) -> List[TaxCode]:
        """Get all TaxCodes"""
        return TaxCodeService.get_all()

    @login_required
    @accepted_u_types('admin')
    @ns.expect(tax_code_dto, validate=True)
    @ns.marshal_with(tax_code_dto)
    def post(self) -> TaxCode:
        """Create a Single TaxCode"""
        return TaxCodeService.create(request.json)


@ns.route("/<string:tax_code_code>")
@ns.param("tax_code_code", "TaxCode database code")
class TaxCodeIdResource(Resource):
    @login_required
    def get(self, tax_code_code: str) -> TaxCode:
        """Get Single TaxCode"""
        return TaxCodeService.get_by_code(tax_code_code)

    @login_required
    @accepted_u_types('admin')
    def delete(self, tax_code_code: str) -> Response:
        """Delete Single TaxCode"""
        from flask import jsonify

        id = TaxCodeService.delete_by_code(tax_code_code)
        return jsonify(dict(status="Success", id=id))

    @login_required
    @accepted_u_types('admin')
    @ns.expect(tax_code_dto, validate=True)
    @ns.marshal_with(tax_code_dto, envelope='data')
    def put(self, tax_code_code: str) -> TaxCode:
        """Update Single TaxCode"""

        data_changes: TaxCodeInterface = request.json
        return TaxCodeService.update(tax_code_code, data_changes)
