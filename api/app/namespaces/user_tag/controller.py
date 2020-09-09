from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import UserTag
from . import user_tag_dto
from .service import UserTagService

from ..utils.decorators import login_required


ns = Namespace("UserTag", description="UserTag Related Operations")  # noqa
ns.add_model(user_tag_dto.name, user_tag_dto)


@ns.route("/")
class UserTagResource(Resource):
    """UserTags"""
    @ns.marshal_list_with(user_tag_dto, envelope='data')
    @login_required
    def get(self) -> List[UserTag]:
        """Get all UserTags"""
        return UserTagService.get_all()

    # @ns.expect(user_tag_dto, validate=True)
    # @ns.marshal_with(user_tag_dto)
    # def post(self) -> UserTag:
    #     """Create a Single UserTag"""
    #     return UserTagService.create(request.parsed_obj)


# @ns.route("/<string:tag_code>")
# @ns.param("tag_code", "UserTag database code")
# @login_required
# class UserTagIdResource(Resource):
#     def get(self, tag_code: str) -> UserTag:
#         """Get Single UserTag"""
#         return UserTagService.get_by_code(tag_code)

#     def delete(self, tag_code: str) -> Response:
#         """Delete Single UserTag"""
#         from flask import jsonify

#         code = UserTagService.delete_by_code(tag_code)
#         return jsonify(dict(status="Success", code=code))

#     @ns.expect(user_tag_dto, validate=True)
#     @ns.marshal_with(user_tag_dto)
#     def put(self, tag_code: str) -> UserTag:
#         """Update Single UserTag"""

#         data_changes: UserTagInterface = request.parsed_obj
#         return UserTagService.update(tag_code, data_changes)
