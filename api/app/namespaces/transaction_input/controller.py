from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource, reqparse
from flask.wrappers import Response

from app.extensions import limiter

from . import transaction_input_dto, transaction_input_sub_dto, transaction_input_admin_dto
from . import TransactionInput
from .service import TransactionInputService

from ..utils.decorators import login_required, employer_required



ns = Namespace("TransactionInput", description="Transaction Input Related Operations")  # noqa
ns.add_model(transaction_input_dto.name, transaction_input_dto)
ns.add_model(transaction_input_admin_dto.name, transaction_input_admin_dto)
ns.add_model(transaction_input_sub_dto.name, transaction_input_sub_dto)

parser = reqparse.RequestParser()
parser.add_argument('seller_firm_public_id', type=str)
parser.add_argument('page', type=int)


@ns.route("/")
class TransactionInputResource(Resource):
    """TransactionInputs"""
    @login_required
    @ns.marshal_list_with(transaction_input_dto, envelope='data')
    def get(self) -> List[TransactionInput]:
        """Get all TransactionInputs"""
        return TransactionInputService.get_all()

    # !!!! DELETE ALL NEEDS TOO BE REMOVED ASAP !!!!!
    @login_required
    def delete(self) -> Response:
        """Delete Single TransactionInput"""
        from flask import jsonify

        return TransactionInputService.delete_all()


@ns.route("/<string:transaction_input_public_id>")
@ns.param("transaction_input_public_id", "TransactionInput database ID")
class TransactionInputIdResource(Resource):
    @login_required
    @ns.marshal_with(transaction_input_dto, envelope='data')
    def get(self, transaction_input_public_id: str) -> TransactionInput:
        """Get Single TransactionInput"""
        return TransactionInputService.get_by_public_id(transaction_input_public_id)

    @login_required
    def delete(self, transaction_input_public_id: str) -> Response:
        """Delete Single TransactionInput"""
        from flask import jsonify

        public_id = TransactionInputService.delete_by_public_id(transaction_input_public_id)
        return jsonify(dict(status="Success", id=public_id))

    @login_required
    @ns.expect(transaction_input_dto, validate=True)
    @ns.marshal_with(transaction_input_dto, envelope='data')
    def put(self, transaction_input_public_id: str) -> TransactionInput:
        """Update Single TransactionInput"""

        data_changes: TransactionInputInterface = request.parsed_obj
        return TransactionInputService.update_by_public_id(transaction_input_public_id, data_changes)


@ns.route("/seller_firm/") #<string:seller_firm_public_id><int:page>")
@ns.param("seller_firm_public_id", "TransactionInput database ID")
class TransactionInputSellerFirmIdResource(Resource):
    decorators = [limiter.limit("5/second")]
    @login_required
    @ns.marshal_list_with(transaction_input_sub_dto, envelope='data')
    def get(self) -> List[TransactionInput]:
        """Get Single TransactionInput"""
        args = parser.parse_args()
        print('args:', args, flush=True)
        return TransactionInputService.get_by_seller_firm_public_id(args.get('seller_firm_public_id'), paginate=True, page=args.get('page'))



@ns.route("/csv")
class TransactionInputResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        transaction_input_files: List[BinaryIO] = request.files.getlist("files")
        return TransactionInputService.process_transaction_input_files_upload(transaction_input_files)
