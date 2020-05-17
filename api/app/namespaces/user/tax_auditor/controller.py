from typing import List

from flask import request, g, current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from app.extensions import mail
from .schema import tax_auditor_dto
from .service import TaxAuditorService
from .model import TaxAuditor
from .interface import TaxAuditorInterface

from ...utils import login_required, accepted_u_types, confirmation_required
from ...utils.service import TemplateService


from ...business.seller_firm.service import SellerFirmService
from ...item.service import ItemService
from ...transaction_input.service import TransactionInputService
from ...platform.amazon.service import DistanceSaleService
from ...account.service import AccountService
from ...tax.vatin.service import VATINService




ns = Namespace("TaxAuditor", description="TaxAuditor Related Operations")  # noqa
ns.add_model(tax_auditor_dto.name, tax_auditor_dto)
#ns.add_model(tax_auditor_dto_admin.name, tax_auditor_dto_admin)
# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route("/")
class TaxAuditorResource(Resource):
    # @ns.param("public_id", "Public tax_auditor ID")
    @login_required
    @ns.marshal_with(tax_auditor_dto, envelope='data')
    def get(self) -> TaxAuditor:
        """ Current TaxAuditor TaxAuditor """
        return g.user

    @ns.expect(tax_auditor_dto, validate=True)
    def post(self):
        """Create A Single TaxAuditor"""
        tax_auditor_data: TaxAuditorInterface = request.json
        return TaxAuditorService.create_tax_auditor(tax_auditor_data)

    @login_required
    def delete(self) -> Response:
        """Delete self"""
        return TaxAuditorService.delete_by_id(g.user.public_id)

    @login_required
    @ns.expect(tax_auditor_dto, validate=True)
    @ns.marshal_with(tax_auditor_dto)
    def put(self) -> TaxAuditor:
        """Update self"""
        data_changes: TaxAuditorInterface = request.json  # JSON body of a request
        tax_auditor = g.user
        return TaxAuditorService.update(tax_auditor, data_changes)



@ns.route("/upload/seller_firm_information")
class SellerFirmInformationTAResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    # !!! @ns.expect(tax_record_dto, validate=True)
    def post(self):
        """Create an unclaimed seller firm as a client"""
        seller_firm_information_files: list = request.files.getlist("files")
        print("POST file received")
        print('uploaded_files')
        print(seller_firm_information_files)
        claimed = False
        return SellerFirmService.process_seller_firm_information_files_upload(seller_firm_information_files, claimed)


@ns.route("/upload/item_information")
class ItemInformationTAResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    @ns.expect(tax_record_dto, validate=True)
    def post(self):
        item_information_files: list = request.files.getlist("files")
        return ItemService.process_item_files_upload(item_information_files)



@ns.route("/upload/account_information")
class AccountInformationTAResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    @ns.expect(tax_record_dto, validate=True)
    def post(self):
        account_information_files: list = request.files.getlist("files")
        return AccountService.process_account_files_upload(account_information_files)



@ns.route("/upload/distance_sales")
class DistanceSalesTAResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    @ns.expect(tax_record_dto, validate=True)
    def post(self):
        distance_sale_information_files: list = request.files.getlist("files")
        return DistanceSaleService.process_distance_sale_files_upload(distance_sale_information_files)



@ns.route("/upload/vat_numbers")
class VATNumbersTAResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    @ns.expect(tax_record_dto, validate=True)
    def post(self):
        vat_numbers_files: list = request.files.getlist("files")
        return VATINService.process_vat_numbers_files_upload(vat_numbers_files)



@ns.route("/upload/transaction_reports")
class TransactionReportsTAResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    @ns.expect(tax_record_dto, validate=True)
    def post(self):
        transaction_input_files: list = request.files.getlist("files")
        return TransactionInputService.process_transaction_input_files_upload(transaction_input_files)






# @ns.route("/clients")
# # class TaxAuditorClientListResource(Resource):
# #     """Get all Company Clients"""
# #     @login_required
# #     @accepted_u_types('admin', 'tax_auditor')
# #     #@confirmation_required
# #     @ns.marshal_list_with(tax_auditor_dto, envelope='data')
# #     def get(self) -> List[TaxAuditor]:
# #         """List Of Registered TaxAuditors"""
# #         return TaxAuditorService.get_company_clients()

# @login_required
# @accepted_u_types('admin', 'tax_auditor')
# @ns.expect(seller_dto, validate=True)
# def post(self):
#     """Create An Unclaimed Seller Firm by Amazon ID"""
#     seller_firm_data: SellerFirmInterface = request.json
#     tax_auditor = g.user
#     return TaxAuditor_Service.create_unclaimed_seller_firm(tax_auditor, seller_firm_data)






# @ns.route("/follow/<string:public_id>")
# @ns.param("public_id", "Public tax_auditor ID")
# class FollowResource(Resource):
#     @login_required
#     @accepted_u_types('admin', 'tax_auditor')
#     #@confirmation_required
#     def get(self, public_id: str) -> TaxAuditor:
#         """Follow One TaxAuditor, i.e. client"""
#         tax_auditor = g.user
#         client_public_id = public_id
#         return TaxAuditorService.follow(tax_auditor, client_public_id)


# @ns.route("/unfollow/<string:public_id>")
# @ns.param("public_id", "Public tax_auditor ID")
# class UnfollowResource(Resource):
#     @login_required
#     @accepted_u_types('admin', 'tax_auditor')
#     #@confirmation_required
#     def get(self, public_id: str) -> TaxAuditor:
#         """Unfollow One TaxAuditor, i.e. client"""
#         tax_auditor = g.user
#         client_public_id = public_id
#         return TaxAuditorService.unfollow(tax_auditor, client_public_id)


# @ns.route("/download/<string:activity_period>/<string:filename>")
# class TransactionResource(Resource):
#     @login_required
#     # @confirmation_required
#     # @ns.expect(transaction_dto, validate=True)
#     def get(self, activity_period, filename):
#         """Download A Tax Data File"""
#         #user = "f997f796-a605-4175-8fae-3de2d0c773a6"
#         user = g.user
#         return TransactionService.download_file(user, activity_period, filename)
