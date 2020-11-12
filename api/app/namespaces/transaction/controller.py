
from typing import List
from flask import request

from flask_restx import Namespace, Resource, reqparse

from app.extensions import limiter


from . import Transaction
from .service import TransactionService
from .schema import transaction_dto, transaction_admin_dto, transaction_sub_dto

from app.namespaces.utils.decorators import login_required, accepted_roles

ns = Namespace("Transaction", description="Transaction Related Operations")  # noqa
ns.add_model(transaction_dto.name, transaction_dto)
ns.add_model(transaction_sub_dto.name, transaction_sub_dto)
ns.add_model(transaction_admin_dto.name, transaction_admin_dto)

parser = reqparse.RequestParser()
parser.add_argument('tax_record_public_id', type=str)
parser.add_argument('tax_treatment_code', type=str)
parser.add_argument('page', type=int)


@ns.route("/")
class TransactionResource(Resource):
    """Transactions"""
    @login_required
    @accepted_roles('admin')
    @ns.marshal_list_with(transaction_dto, envelope='data')
    def get(self) -> List[Transaction]:
        """Get all Transactions"""
        return TransactionService.get_all()


@ns.route("/<string:transaction_public_id>")
@ns.param("transaction_id", "Transaction database ID")
class TransactionIdResource(Resource):
    @login_required
    @ns.marshal_with(transaction_dto, envelope='data')
    def get(self, transaction_public_id: str) -> Transaction:
        """Get Single Transaction"""
        return TransactionService.get_by_public_id(transaction_public_id)


    @login_required
    @ns.expect(transaction_dto, validate=True)
    @ns.marshal_with(transaction_dto)
    def put(self, transaction_public_id: int) -> Transaction:
        """Update Single Transaction"""

        data_changes: TransactionInterface = request.json
        return TransactionService.update_by_public_id(transaction_public_id, data_changes)


@ns.route("/tax_record/init")  # <string:tax_record_public_id><int:page>")
@ns.param("tax_record_public_id", "Tax Record Public ID")
class TransactionSellerFirmTaxRecordResource(Resource):
    decorators = [limiter.limit("5/second")]
    @login_required
    @ns.marshal_list_with(transaction_dto, envelope='data')
    def get(self) -> List[Transaction]:
        """Get Single Transaction"""
        args = parser.parse_args()
        return TransactionService.get_by_tax_record(args.get('tax_record_public_id'), paginate=True, page=args.get('page'))


@ns.route("/tax_record/")  # <string:tax_record_public_id><int:page>")
@ns.param("tax_record_public_id", "Tax Record Public ID")
@ns.param("tax_treatment_code", "Tax Treatment Code")
class TransactionSellerFirmTaxRecordTaxTreamtnetResource(Resource):
    decorators = [limiter.limit("5/second")]
    @login_required
    @ns.marshal_list_with(transaction_dto, envelope='data')
    def get(self) -> List[Transaction]:
        """Get Single Transaction"""
        args = parser.parse_args()
        return TransactionService.get_by_tax_record_tax_treatment(args.get('tax_record_public_id'), args.get('tax_treatment_code'), paginate=True, page=args.get('page'))
