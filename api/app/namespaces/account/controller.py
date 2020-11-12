from typing import List, BinaryIO
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Account
from . import account_dto, account_sub_dto, account_admin_dto
from .service import AccountService

from app.namespaces.utils.decorators import login_required, accepted_roles


ns = Namespace("Account", description="Account Related Operations")  # noqa
ns.add_model(account_dto.name, account_dto)
ns.add_model(account_sub_dto.name, account_sub_dto)
ns.add_model(account_admin_dto.name, account_admin_dto)



@ns.route("/")
class AccountResource(Resource):
    """Accounts"""
    @login_required
    @accepted_roles('admin')
    @ns.marshal_list_with(account_dto, envelope='data')
    def get(self) -> List[Account]:
        """Get all Accounts"""
        return AccountService.get_all()

    @login_required
    @accepted_roles('admin')
    @ns.expect(account_dto, validate=True)
    @ns.marshal_with(account_dto)
    def post(self) -> Account:
        """Create a Single Account For Any Firm. For Specific Firms"""
        return AccountService.create(request.json)


@ns.route("/<string:account_public_id>")
@ns.param("account_public_id", "Account database ID")
class AccountIdResource(Resource):
    @login_required
    @ns.marshal_with(account_dto, envelope='data')
    def get(self, account_public_id: int) -> Account:
        """Get Single Account"""
        return AccountService.get_by_public_id(account_public_id)

    @login_required
    def delete(self, account_public_id: int) -> Response:
        """Delete Single Account"""
        from flask import jsonify

        id = AccountService.delete_by_public_id(account_public_id)
        return jsonify(dict(status="Success", id=id))

    @login_required
    @ns.expect(account_dto, validate=True)
    @ns.marshal_with(account_dto)
    def put(self, account_public_id: int) -> Account:
        """Update Single Account"""

        data_changes: AccountInterface = request.json
        return AccountService.update_by_public_id(account_public_id, data_changes)


@ns.route("/seller_firm/<string:seller_firm_public_id>")
class SellerFirmAccountResource(Resource):
    """ Create Account for a Specific Seller Firm based on its Public ID"""

    # @ns.expect(distance_sale_dto, validate=True)
    @login_required
    @ns.marshal_with(account_sub_dto, envelope='data')
    def post(self, seller_firm_public_id: str) -> Account:
        return AccountService.process_single_submit(seller_firm_public_id, account_data=request.json)
