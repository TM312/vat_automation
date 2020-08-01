
from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource

from . import tax_record_dto, tax_record_sub_dto, tax_record_dto_admin
from . import TaxRecord
from .service import TaxRecordService
from .interface import TaxRecordInterface

from ..utils.decorators import login_required, employer_required, accepted_u_types

ns = Namespace("TaxRecord", description="Tax Record Related Operations")  # noqa
ns.add_model(tax_record_dto.name, tax_record_dto)
ns.add_model(tax_record_dto_admin.name, tax_record_dto_admin)
ns.add_model(tax_record_sub_dto.name, tax_record_sub_dto)


@ns.route("/")
class TaxRecordResource(Resource):
    """TaxRecords"""
    @accepted_u_types('admin')
    @ns.marshal_list_with(tax_record_dto, envelope='data')
    def get(self) -> List[TaxRecord]:
        """Get all TaxRecords"""
        return TaxRecordService.get_all()

    # @login_required
    # @employer_required
    # @ns.expect(tax_record_dto, validate=True)
    # def post(self):
    #     """Create A Single Tax Record """
    #     start_date_str = request.args.get('start_date_str')
    #     end_date_str = request.args.get('end_date_str')
    #     seller_firm_public_id = request.args.get('seller_firm_public_id')
    #     tax_jurisdiction_code = request.args.get('tax_jurisdiction_code')
    #     return generate_tax_record(start_date_str, end_date_str, seller_firm_public_id, tax_jurisdiction_code)


@ns.route("/<string:public_id>")
class TaxRecordResource(Resource):
    @login_required
    @employer_required
    def get(self, public_id):
        return TaxRecordService.download_tax_record(public_id)


@ns.route("/seller_firm/<string:seller_firm_public_id>")
class TaxRecordSellerFirmResource(Resource):
    @login_required
    @ns.marshal_list_with(tax_record_dto, envelope='data')
    def get(self) -> List[TaxRecord]:
        """Get own Tax Records """
        return TaxRecordService.get_all_by_seller_firm_public_id(seller_firm_public_id)

    @login_required
    @ns.marshal_with(tax_record_dto, envelope='data')
    def post(self, seller_firm_public_id) -> TaxRecord:
        """Create for the indicated seller firm"""
        tax_record_data: TaxRecordInterface = request.json
        return TaxRecordService.create_by_seller_firm_public_id(seller_firm_public_id, tax_record_data)
