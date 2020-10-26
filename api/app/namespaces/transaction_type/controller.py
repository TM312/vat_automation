from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import TransactionType
from . import transaction_type_dto
from .service import TransactionTypeService

from app.namespaces.utils.decorators import login_required


ns = Namespace("TransactionType", description="Transaction Type Related Operations")  # noqa
ns.add_model(transaction_type_dto.name, transaction_type_dto)


@ns.route("/")
class TransactionTypeResource(Resource):
    """TransactionTypes"""
    @ns.marshal_list_with(transaction_type_dto, envelope='data')
    @login_required
    def get(self) -> List[TransactionType]:
        """Get all TransactionTypes"""
        return TransactionTypeService.get_all()

    # @ns.expect(transaction_type_dto, validate=True)
    # @ns.marshal_with(transaction_type_dto)
    # def post(self) -> TransactionType:
    #     """Create a Single TransactionType"""
    #     return TransactionTypeService.create(request.parsed_obj)


# @ns.route("/<string:tag_code>")
# @ns.param("tag_code", "TransactionType database code")
# @login_required
# class TransactionTypeIdResource(Resource):
#     def get(self, tag_code: str) -> TransactionType:
#         """Get Single TransactionType"""
#         return TransactionTypeService.get_by_code(tag_code)

#     def delete(self, tag_code: str) -> Response:
#         """Delete Single TransactionType"""
#         from flask import jsonify

#         code = TransactionTypeService.delete_by_code(tag_code)
#         return jsonify(dict(status="Success", code=code))

#     @ns.expect(transaction_type_dto, validate=True)
#     @ns.marshal_with(transaction_type_dto)
#     def put(self, tag_code: str) -> TransactionType:
#         """Update Single TransactionType"""

#         data_changes: TransactionTypeInterface = request.parsed_obj
#         return TransactionTypeService.update(tag_code, data_changes)
