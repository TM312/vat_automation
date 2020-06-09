
from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource

from .service import TaxRecordService
from .schema import tax_record_dto
from .model import TaxRecord

from ..utils.decorators import login_required, employer_required, accepted_u_types

ns = Namespace("TaxRecord", description="Tax Record Related Operations")  # noqa
ns.add_model(tax_record_dto.name, tax_record_dto)


@api.route("/")
class VatResource(Resource):
    """Vats"""
    @accepted_u_types('admin')
    @ns.marshal_list_with(tax_record_dto, envelope='data')
    def get(self) -> List[Vat]:
        """Get all Vats"""
        return VatService.get_all()



@ns.route("/<string:public_id>")
class TaxRecordResource(Resource):
    @login_required
    @employer_required
    def get(self, public_id):
        return TaxRecordService.download_tax_record(public_id)

    @login_required
    @employer_required
    @ns.expect(tax_record_dto, validate=True)
    def post(self):
        """Create A Single Tax Record """
        start_date_str = request.args.get('start_date_str')
        end_date_str = request.args.get('end_date_str')
        seller_firm_public_id = request.args.get('seller_firm_public_id')
        tax_jurisdiction_code = request.args.get('tax_jurisdiction_code')
        return generate_tax_record(start_date_str, end_date_str, seller_firm_public_id, tax_jurisdiction_code)


@ns.route("/seller_firm/<string:seller_firm_public_id>")
class TaxRecordSellerFirmResource(Resource):
    @login_required
    @ns.marshal_list_with(tax_record_dto, envelope='data')
    def get(self) -> List[TaxRecord]:
        """Get own Tax Records """
        return TaxRecordService.get_all_by_seller_firm_public_id(seller_firm_public_id)
