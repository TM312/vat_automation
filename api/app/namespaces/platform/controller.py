from typing import List
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Platform
from . import platform_dto
from .service import PlatformService


from ..utils.decorators import login_required, employer_required


ns = Namespace("Platform", description="Platform Related Operations")  # noqa
ns.add_model(platform_dto.name, platform_dto)


@ns.route("/")
class PlatformResource(Resource):
    """Platforms"""
    @ns.marshal_list_with(platform_dto, envelope='data')
    def get(self) -> List[Platform]:
        """Get all Platforms"""
        return PlatformService.get_all()

    @ns.expect(platform_dto, validate=True)
    @ns.marshal_with(platform_dto)
    def post(self) -> Platform:
        """Create a Single Platform"""
        return PlatformService.create(request.parsed_obj)


@ns.route("/<int:platform_id>")
@ns.param("platform_id", "Platform database code")
class PlatformIdResource(Resource):
    def get(self, platform_id: int) -> Platform:
        """Get Single Platform"""
        return PlatformService.get_by_id(platform_id)

    def delete(self, platform_id: int) -> Response:
        """Delete Single Platform"""
        from flask import jsonify

        id = PlatformService.delete_by_id(platform_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(platform_dto, validate=True)
    @ns.marshal_with(platform_dto)
    def put(self, platform_id: int) -> Platform:
        """Update Single Platform"""

        data_changes: PlatformInterface = request.parsed_obj
        return PlatformService.update(platform_id, data_changes)
