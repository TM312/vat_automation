from typing import List, BinaryIO
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from flask import request

from . import VATIN
from . import vatin_dto
from .service import VATINService


from ...utils.decorators import login_required, employer_required


ns = Namespace("VATIN", description="VATIN Related Operations")  # noqa
ns.add_model(vatin_dto.name, vatin_dto)


@ns.route("/")
class VATINResource(Resource):
    """VATINs"""
    @ns.marshal_list_with(vatin_dto, envelope='data')
    def get(self) -> List[VATIN]:
        """Get all VATINs"""
        return VATINService.get_all()

    @ns.expect(vatin_dto, validate=True)
    @ns.marshal_with(vatin_dto)
    def post(self) -> VATIN:
        """Create a Single VATIN"""
        return VATINService.create(request.parsed_obj)


@ns.route("/<int:vatin_id>")
@ns.param("vatin_id", "VATIN database ID")
class VATINIdResource(Resource):
    def get(self, vatin_id: int) -> VATIN:
        """Get Single VATIN"""
        return VATINService.get_by_id(vatin_id)

    def delete(self, vatin_id: int) -> Response:
        """Delete Single VATIN"""
        from flask import jsonify

        id = VATINService.delete_by_id(vatin_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(vatin_dto, validate=True)
    @ns.marshal_with(vatin_dto)
    def put(self, vatin_id: int) -> VATIN:
        """Update Single VATIN"""

        data_changes: VATINInterface = request.parsed_obj
        return VATINService.update(vatin_id, data_changes)



@ns.route("/csv")
class VATNumbersResource(Resource):
    @login_required
    # @employer_required
    # @confirmation_required
    def post(self):
        vat_numbers_files: List[BinaryIO] = request.files.getlist("files")
        print(vat_numbers_files, flush=True)
        return VATINService.process_vat_numbers_files_upload(vat_numbers_files)
