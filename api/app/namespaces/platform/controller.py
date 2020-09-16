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


@ns.route("/<string:platform_code>")
@ns.param("platform_code", "Platform database code")
class PlatformIdResource(Resource):
    def get(self, platform_code: str) -> Platform:
        """Get Single Platform"""
        return PlatformService.get_by_code(platform_code)

    def delete(self, platform_code: str) -> Response:
        """Delete Single Platform"""
        from flask import jsonify

        id = PlatformService.delete_by_code(platform_code)
        return jsonify(dict(status="Success", code=code))

    @ns.expect(platform_dto, validate=True)
    @ns.marshal_with(platform_dto)
    def put(self, platform_code: str) -> Platform:
        """Update Single Platform"""

        data_changes: PlatformInterface = request.parsed_obj
        return PlatformService.update(platform_code, data_changes)
