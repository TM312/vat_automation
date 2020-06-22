from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response


from . import transaction_input_dto
from . import TransactionInput
from .service import TransactionInputService

from ..utils.decorators import login_required, employer_required


ns = Namespace("TransactionInput", description="Transaction Input Related Operations")  # noqa
ns.add_model(transaction_input_dto.name, transaction_input_dto)


@ns.route("/")
class TransactionInputResource(Resource):
    """TransactionInputs"""
    @ns.marshal_list_with(transaction_input_dto, envelope='data')
    def get(self) -> List[TransactionInput]:
        """Get all TransactionInputs"""
        return TransactionInputService.get_all()


@ns.route("/<int:transaction_input_id>")
@ns.param("transaction_input_id", "TransactionInput database ID")
class TransactionInputIdResource(Resource):
    def get(self, transaction_input_id: int) -> TransactionInput:
        """Get Single TransactionInput"""
        return TransactionInputService.get_by_id(transaction_input_id)

    def delete(self, transaction_input_id: int) -> Response:
        """Delete Single TransactionInput"""
        from flask import jsonify

        id = TransactionInputService.delete_by_id(transaction_input_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(transaction_input_dto, validate=True)
    @ns.marshal_with(transaction_input_dto)
    def put(self, transaction_input_id: int) -> TransactionInput:
        """Update Single TransactionInput"""

        data_changes: TransactionInputInterface = request.parsed_obj
        return TransactionInputService.update(transaction_input_id, data_changes)


@ns.route("/csv")
class TransactionInputResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        transaction_input_files: List[BinaryIO] = request.files.getlist("files")
        return TransactionInputService.process_transaction_input_files_upload(transaction_input_files)
