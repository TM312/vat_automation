from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import ItemTag
from . import item_tag_dto
from .service import ItemTagService

from ..utils.decorators import login_required


ns = Namespace("ItemTag", description="ItemTag Related Operations")  # noqa
ns.add_model(item_tag_dto.name, item_tag_dto)


@ns.route("/")
class ItemTagResource(Resource):
    """ItemTags"""
    @ns.marshal_list_with(item_tag_dto, envelope='data')
    @login_required
    def get(self) -> List[ItemTag]:
        """Get all ItemTags"""
        return ItemTagService.get_all()

    # @ns.expect(item_tag_dto, validate=True)
    # @ns.marshal_with(item_tag_dto)
    # def post(self) -> ItemTag:
    #     """Create a Single ItemTag"""
    #     return ItemTagService.create(request.parsed_obj)


# @ns.route("/<string:tag_code>")
# @ns.param("tag_code", "ItemTag database code")
# @login_required
# class ItemTagIdResource(Resource):
#     def get(self, tag_code: str) -> ItemTag:
#         """Get Single ItemTag"""
#         return ItemTagService.get_by_code(tag_code)

#     def delete(self, tag_code: str) -> Response:
#         """Delete Single ItemTag"""
#         from flask import jsonify

#         code = ItemTagService.delete_by_code(tag_code)
#         return jsonify(dict(status="Success", code=code))

#     @ns.expect(item_tag_dto, validate=True)
#     @ns.marshal_with(item_tag_dto)
#     def put(self, tag_code: str) -> ItemTag:
#         """Update Single ItemTag"""

#         data_changes: ItemTagInterface = request.parsed_obj
#         return ItemTagService.update(tag_code, data_changes)
