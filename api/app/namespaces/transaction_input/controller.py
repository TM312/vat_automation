from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource

from .service import TransactionInputService

from ..utils.decorators import login_required, employer_required


ns = Namespace("TransactionInput", description="Transaction Input Related Operations")  # noqa
#ns.add_model(user_dto.name, user_dto) !!!


@ns.route("/csv")
class TransactionInputResource(Resource):
    @login_required
    @employer_required
    # @confirmation_required
    #@ns.expect(tax_record_dto, validate=True)
    def post(self):
        transaction_input_files: List[BinaryIO] = request.files.getlist("files")
        return TransactionInputService.process_transaction_input_files_upload(transaction_input_files)
