from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import TransactionTypePublic
from . import transaction_type_public_dto
from .service import TransactionTypePublicService

from app.namespaces.utils.decorators import login_required


ns = Namespace("TransactionTypePublic", description="Transaction Type Related Operations")  # noqa
ns.add_model(transaction_type_public_dto.name, transaction_type_public_dto)


@ns.route("/")
class TransactionTypePublicResource(Resource):
    """TransactionTypePublics"""
    @ns.marshal_list_with(transaction_type_public_dto, envelope='data')
    @login_required
    def get(self) -> List[TransactionTypePublic]:
        """Get all TransactionTypePublics"""
        return TransactionTypePublicService.get_all()

    # @ns.expect(transaction_type_public_dto, validate=True)
    # @ns.marshal_with(transaction_type_public_dto)
    # def post(self) -> TransactionTypePublic:
    #     """Create a Single TransactionTypePublic"""
    #     return TransactionTypePublicService.create(request.json)


# @ns.route("/<string:tag_code>")
# @ns.param("tag_code", "TransactionTypePublic database code")
# @login_required
# class TransactionTypePublicIdResource(Resource):
#     def get(self, tag_code: str) -> TransactionTypePublic:
#         """Get Single TransactionTypePublic"""
#         return TransactionTypePublicService.get_by_code(tag_code)

#     def delete(self, tag_code: str) -> Response:
#         """Delete Single TransactionTypePublic"""
#         from flask import jsonify

#         code = TransactionTypePublicService.delete_by_code(tag_code)
#         return jsonify(dict(status="Success", code=code))

#     @ns.expect(transaction_type_public_dto, validate=True)
#     @ns.marshal_with(transaction_type_public_dto)
#     def put(self, tag_code: str) -> TransactionTypePublic:
#         """Update Single TransactionTypePublic"""

#         data_changes: TransactionTypePublicInterface = request.json
#         return TransactionTypePublicService.update(tag_code, data_changes)
