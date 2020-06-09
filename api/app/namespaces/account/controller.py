from typing import List, BinaryIO
from flask import request
from flask_restx import Namespace, Resource

from . import Account
from . import account_dto
from .service import AccountService

from ..utils.decorators import login_required, employer_required


ns = Namespace("Account", description="Account Related Operations")  # noqa
ns.add_model(account_dto.name, account_dto)



@api.route("/")
class AccountResource(Resource):
    """Accounts"""
    @ns.marshal_list_with(account_dto, envelope='data')
    def get(self) -> List[Account]:
        """Get all Accounts"""
        return AccountService.get_all()

    @ns.expect(account_dto, validate=True)
    @ns.marshal_with(account_dto)
    def post(self) -> Account:
        """Create a Single Account"""
        return AccountService.create(request.parsed_obj)


@api.route("/<int:account_id>")
@api.param("account_id", "Account database ID")
class AccountIdResource(Resource):
    def get(self, account_id: int) -> Account:
        """Get Single Account"""
        return AccountService.get_by_id(account_id)

    def delete(self, account_id: int) -> Response:
        """Delete Single Account"""
        from flask import jsonify

        id = AccountService.delete_by_id(account_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(account_dto, validate=True)
    @ns.marshal_with(account_dto)
    def put(self, account_id: int) -> Account:
        """Update Single Account"""

        data_changes: AccountInterface = request.parsed_obj
        Account = AccountService.get_by_id(account_id)
        return AccountService.update(Account, data_changes)


@ns.route("/csv")
class AccountInformationResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        account_information_files: List[BinaryIO] = request.files.getlist("files")
        return AccountService.process_account_files_upload(account_information_files)
