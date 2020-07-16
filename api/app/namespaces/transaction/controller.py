
from typing import List
from flask import request

from flask_restx import Namespace, Resource

from . import Transaction
from .service import TransactionService
from .schema import transaction_dto, transaction_admin_dto, transaction_sub_dto, transaction_type_dto

from ..utils.decorators import login_required

ns = Namespace("Transaction", description="Transaction Related Operations")  # noqa
ns.add_model(transaction_dto.name, transaction_dto)
ns.add_model(transaction_sub_dto.name, transaction_sub_dto)
ns.add_model(transaction_admin_dto.name, transaction_admin_dto)
ns.add_model(transaction_type_dto.name, transaction_type_dto)


@ns.route("/")
class TransactionResource(Resource):
    """Transactions"""
    @ns.marshal_list_with(transaction_dto, envelope='data')
    @login_required
    def get(self) -> List[Transaction]:
        """Get all Transactions"""
        return TransactionService.get_all()


@ns.route("/<string:transaction_public_id>")
@ns.param("transaction_id", "Transaction database ID")
class TransactionIdResource(Resource):
    def get(self, transaction_public_id: str) -> Transaction:
        """Get Single Transaction"""
        return TransactionService.get_by_public_id(transaction_public_id)
