# from typing import List

# from flask import request
# from flask import current_app
# from flask.wrappers import Response

# from flask_restx import Namespace, Resource

# from .schema import seller_firm_dto
# from .service import SellerFirmService
# from .model import SellerFirm
# from .interface import SellerFirmInterface

# from ...auth.interface import TokenInterface
# from ...utils.decorators.auth import login_required, accepted_u_types, confirmation_required


# ns = Namespace("SellerFirm", description="Seller Firm Related Operations")  # noqa
# ns.add_model(seller_firm_dto.name, seller_firm_dto)


# @ns.route("/")
# class SellerFirmResource(Resource):
#     @login_required
#     @ns.marshal_with(seller_firm_dto)
#     def get(self) -> SellerFirm:
#         """Get own Accounting Firm"""
#         seller = g.user
#         return SellerFirmService.get_own(seller)

#     @ns.expect(seller_firm_dto, validate=True)
#     def post(self):
#         """Create A Single Accounting Firm"""
#         seller_firm_data: SellerFirmInterface = request.json
#         return SellerFirmService.create_seller_firm(seller_firm_data)

#     @login_required
#     def delete(self) -> Response:
#         """Delete A Single Accounting Business"""
#         seller = g.user
#         return SellerFirmService.delete_own(seller)

#     @login_required
#     @ns.expect(seller_firm_dto, validate=True)
#     @ns.marshal_with(seller_firm_dto)
#     #@accepted_u_types('admin', 'seller')
#     def put(self) -> SellerFirm:
#         """Update A own accounting firm"""
#         seller = g.user
#         data_changes: SellerFirmInterface = request.json  # JSON body of a request
#         return SellerFirmService.update_own(seller, data_changes)
