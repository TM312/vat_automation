from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Tag
from . import tag_dto
from .service import TagService

from ..utils.decorators import login_required


ns = Namespace("Tag", description="Tag Related Operations")  # noqa
ns.add_model(tag_dto.name, tag_dto)


@ns.route("/")
class TagResource(Resource):
    """Tags"""
    @ns.marshal_list_with(tag_dto, envelope='data')
    @login_required
    def get(self) -> List[Tag]:
        """Get all Tags"""
        return TagService.get_all()

    # @ns.expect(tag_dto, validate=True)
    # @ns.marshal_with(tag_dto)
    # def post(self) -> Tag:
    #     """Create a Single Tag"""
    #     return TagService.create(request.parsed_obj)


# @ns.route("/<string:tag_code>")
# @ns.param("tag_code", "Tag database code")
# @login_required
# class TagIdResource(Resource):
#     def get(self, tag_code: str) -> Tag:
#         """Get Single Tag"""
#         return TagService.get_by_code(tag_code)

#     def delete(self, tag_code: str) -> Response:
#         """Delete Single Tag"""
#         from flask import jsonify

#         code = TagService.delete_by_code(tag_code)
#         return jsonify(dict(status="Success", code=code))

#     @ns.expect(tag_dto, validate=True)
#     @ns.marshal_with(tag_dto)
#     def put(self, tag_code: str) -> Tag:
#         """Update Single Tag"""

#         data_changes: TagInterface = request.parsed_obj
#         return TagService.update(tag_code, data_changes)
