from typing import List
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Platform
from . import platform_dto
from .service import PlatformService
from .interface import PlatformInterface

from app.namespaces.utils.decorators import login_required, accepted_u_types
from app.extensions import cache

ns = Namespace("Platform", description="Platform Related Operations")  # noqa
ns.add_model(platform_dto.name, platform_dto)


@ns.route("/")
class PlatformResource(Resource):
    """Platforms"""
    @login_required
    @ns.marshal_list_with(platform_dto, envelope='data')
    @cache.cached(timeout=60)
    def get(self) -> List[Platform]:
        """Get all Platforms"""
        return PlatformService.get_all()

    @login_required
    @accepted_u_types('admin')
    @ns.expect(platform_dto, validate=True)
    @ns.marshal_with(platform_dto)
    def post(self) -> Platform:
        """Create a Single Platform"""
        return PlatformService.create(request.json)


@ns.route("/<string:platform_code>")
@ns.param("platform_code", "Platform database code")
class PlatformIdResource(Resource):
    @login_required
    def get(self, platform_code: str) -> Platform:
        """Get Single Platform"""
        return PlatformService.get_by_code(platform_code)

    @login_required
    @accepted_u_types('admin')
    def delete(self, platform_code: str) -> Response:
        """Delete Single Platform"""
        from flask import jsonify

        id = PlatformService.delete_by_code(platform_code)
        return jsonify(dict(status="Success", code=code))

    @login_required
    @accepted_u_types('admin')
    @ns.expect(platform_dto, validate=True)
    @ns.marshal_with(platform_dto, envelope='data')
    def put(self, platform_code: str) -> Platform:
        """Update Single Platform"""

        data_changes: PlatformInterface = request.json
        return PlatformService.update(platform_code, data_changes)
