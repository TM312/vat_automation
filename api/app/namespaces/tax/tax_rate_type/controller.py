from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response


from . import TaxRateType
from . import tax_rate_type_dto, tax_rate_type_sub_dto
from .service import TaxRateTypeService

from app.namespaces.utils.decorators import login_required, accepted_u_types


ns = Namespace("TaxRateType", description="TaxRateType Related Operations")  # noqa
ns.add_model(tax_rate_type_dto.name, tax_rate_type_dto)
ns.add_model(tax_rate_type_sub_dto.name, tax_rate_type_sub_dto)



@ns.route("/")
class TaxRateTypeResource(Resource):
    """TaxRateTypes"""
    @login_required
    @ns.marshal_list_with(tax_rate_type_sub_dto, envelope='data')
    def get(self) -> List[TaxRateType]:
        """Get all TaxRateTypes"""
        return TaxRateTypeService.get_all()

    @login_required
    @accepted_u_types('admin')
    @ns.expect(tax_rate_type_dto, validate=True)
    @ns.marshal_with(tax_rate_type_dto)
    def post(self) -> TaxRateType:
        """Create a Single TaxRateType"""
        return TaxRateTypeService.create(request.parsed_obj)


@ns.route("/<string:tax_rate_type_code>")
@ns.param("tax_rate_type_code", "TaxRateType database code")
class TaxRateTypeIdResource(Resource):
    @login_required
    def get(self, tax_rate_type_code: str) -> TaxRateType:
        """Get Single TaxRateType"""
        return TaxRateTypeService.get_by_code(tax_rate_type_code)

    @login_required
    @accepted_u_types('admin')
    def delete(self, tax_rate_type_code: str) -> Response:
        """Delete Single TaxRateType"""
        from flask import jsonify

        id = TaxRateTypeService.delete_by_code(tax_rate_type_code)
        return jsonify(dict(status="Success", id=id))

    @login_required
    @accepted_u_types('admin')
    @ns.expect(tax_rate_type_dto, validate=True)
    @ns.marshal_with(tax_rate_type_dto)
    def put(self, tax_rate_type_code: str) -> TaxRateType:
        """Update Single TaxRateType"""

        data_changes: TaxRateTypeInterface = request.parsed_obj
        return TaxRateTypeService.update(tax_rate_type_code, data_changes)
