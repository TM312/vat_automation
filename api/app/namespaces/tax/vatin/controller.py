from typing import List, BinaryIO
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from flask import request

from . import VATIN
from . import vatin_dto, vatin_sub_dto, vatin_verify_dto, vatin_validate_dto
from .service import VATINService


from ...utils.decorators import login_required, employer_required


ns = Namespace("VATIN", description="VATIN Related Operations")  # noqa
ns.add_model(vatin_dto.name, vatin_dto)
ns.add_model(vatin_sub_dto.name, vatin_sub_dto)
ns.add_model(vatin_verify_dto.name, vatin_verify_dto)
ns.add_model(vatin_validate_dto.name, vatin_validate_dto)



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


@ns.route("/<string:vatin_public_id>")
@ns.param("vatin_public_id", "VATIN database ID")
class VATINIdResource(Resource):
    def get(self, vatin_public_id: str) -> VATIN:
        """Get Single VATIN"""
        return VATINService.get_by_public_id(vatin_public_id)

    def delete(self, vatin_public_id: str) -> Response:
        """Delete Single VATIN"""
        from flask import jsonify

        id = VATINService.delete_by_public_id(vatin_public_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(vatin_dto, validate=True)
    @ns.marshal_with(vatin_dto)
    def put(self, vatin_public_id: str) -> VATIN:
        """Update Single VATIN"""

        data_changes: VATINInterface = request.parsed_obj
        return VATINService.update_by_public_id(vatin_public_id, data_changes)


@ns.route("/verify")
class VATINVerifyResource(Resource):
    #@login_required
    @ns.expect(vatin_verify_dto, validate=False)
    @ns.marshal_with(vatin_verify_dto)
    def post(self) -> bool:
        """Verify VATIN"""
        return VATINService.process_verification_request(request.json)


@ns.route("/validate")
class VATINValidateResource(Resource):
    #@login_required
    @ns.expect(vatin_verify_dto, validate=True)
    @ns.marshal_with(vatin_validate_dto)

    def post(self) -> bool:
        """Validate VATIN"""
        print('request.json: ', request.json, flush=True)
        return VATINService.process_validation_request(request.json)


@ns.route("/seller_firm/<string:seller_firm_public_id>")
class DistanceSaleResource(Resource):
    """ Create VATIN for a Specific Seller Firm based on its Public ID"""

    # @ns.expect(vatin_dto, validate=True)
    @login_required
    @ns.marshal_with(vatin_sub_dto, envelope='data')
    def post(self, seller_firm_public_id: str) -> VATIN:
        return VATINService.process_single_submit(seller_firm_public_id, vatin_data_raw=request.json)


@ns.route("/csv")
class VATNumbersResource(Resource):
    @login_required
    # @employer_required
    # @confirmation_required
    def post(self):
        vat_numbers_files: List[BinaryIO] = request.files.getlist("files")
        print(vat_numbers_files, flush=True)
        return VATINService.process_vat_numbers_files_upload(vat_numbers_files)
