from typing import List
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Vat
from . import vat_dto
from .service import VatService

from ...utils.decorators import login_required, employer_required


ns = Namespace("Vat", description="Vat Related Operations")  # noqa
ns.add_model(vat_dto.name, vat_dto)


@ns.route("/")
class VatResource(Resource):
    """Vats"""
    @ns.marshal_list_with(vat_dto, envelope='data')
    def get(self) -> List[Vat]:
        """Get all Vats"""
        return VatService.get_all()

    @ns.expect(vat_dto, validate=True)
    @ns.marshal_with(vat_dto)
    def post(self) -> Vat:
        """Create a Single Vat"""
        return VatService.create(request.parsed_obj)


@ns.route("/<int:vat_id>")
@ns.param("vat_id", "Vat database ID")
class VatIdResource(Resource):
    def get(self, vat_id: int) -> Vat:
        """Get Single Vat"""
        return VatService.get_by_id(vat_id)

    def delete(self, vat_id: int) -> Response:
        """Delete Single Vat"""
        from flask import jsonify

        id = VatService.delete_by_id(vat_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(vat_dto, validate=True)
    @ns.marshal_with(vat_dto)
    def put(self, vat_id: int) -> Vat:
        """Update Single Vat"""

        data_changes: VatInterface = request.parsed_obj
        return VatService.update(vat_id, data_changes)
