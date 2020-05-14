from typing import List

from flask import request, g

from flask.wrappers import Response
from werkzeug.utils import secure_filename
from flask_restx import Namespace, Resource


from .schema import transaction_dto
from .service import TransactionService
from .model import Transaction


from ..utils import login_required, accepted_u_types, confirmation_required, employer_required



ns = Namespace("transactions", description="Transaction Related Operations")  # noqa
ns.add_model(transaction_dto.name, transaction_dto)


@ns.route("/")
class AdminTransactionListResource(Resource):

    # @ns.route("/")
    # class AdminTransactionListResource(Resource):
    #     """Get all Tax Datas"""
    #     @login_required
    #     @accepted_u_types('admin')
    #     @ns.marshal_list_with(transaction_dto, envelope='data')
    #     def get(self) -> List[Transaction]:
    #         """List Of Registered Transactions"""
    #         return TransactionService.get_all()

    # @ns.route("/<string:file_name>")
    # @ns.param("file_name", "File name")
    # class AdminTransactionIdResource(Resource):
    #     @login_required
    #     @accepted_u_types('admin')
    #     @ns.marshal_with(transaction_dto)
    #     def get(self, public_id: str) -> Transaction:
    #         """Get One Transaction"""
    #         return TransactionService.get_by_id(public_id)

    #     @login_required
    #     @accepted_u_types('admin')
    #     def delete(self, public_id: str) -> Response:
    #         """Delete A Single Transaction"""
    #         return TransactionService.delete_by_id(public_id)


@ns.route("/own")
class UserResource(Resource):
    """Get owned available Tax Records"""
    @login_required
    @ns.marshal_with(transaction_dto, envelope='data')
    def get(self) -> List[Transaction]:
        """ List of owned Tax Records """
        user = g.user
        return TransactionService.get_own(user)
#     @login_required
#     @accepted_u_types('admin')
#     @ns.marshal_list_with(transaction_dto, envelope='data')
#     def get(self) -> List[Transaction]:
#         """List Of Registered Transactions"""
#         return TransactionService.get_all()
