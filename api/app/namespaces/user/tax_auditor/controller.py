from typing import List

from flask import request, g
from flask import current_app
from flask.wrappers import Response

from flask_restx import Namespace, Resource


from app.extensions import mail
from .schema import tax_auditor_dto, action_dto
from .service import TaxAuditorService
from .model import TaxAuditor
from .interface import TaxAuditorInterface

from ...auth.interface import TokenInterface
from ...utils.decorators.auth import login_required, accepted_u_types, confirmation_required

SellerFirmInterface



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


@ns.route("/upload")
class TaxRecordResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    # @ns.expect(tax_record_dto, validate=True)
    def post(self):
        """Create A Tax Data Entry And Store The Corresponding File"""
        tax_auditor = g.user  # "f997f796-a605-4175-8fae-3de2d0c773a6"
        uploaded_files = request.files.getlist("files")
        print("POST file received")
        print('uploaded_files')
        print(uploaded_files)
        return TaxRecordService.upload_input(tax_auditor, uploaded_files)





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
