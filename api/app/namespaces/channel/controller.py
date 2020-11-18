from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Channel
from . import channel_dto, channel_sub_dto
from .service import ChannelService
from .interface import ChannelInterface

from app.namespaces.utils.decorators import login_required, accepted_u_types
from app.extensions import cache

ns = Namespace("Channel", description="Channel Related Operations")  # noqa
ns.add_model(channel_dto.name, channel_dto)
ns.add_model(channel_sub_dto.name, channel_sub_dto)


@ns.route("/")
class ChannelResource(Resource):
    """Channels"""
    # @login_required
    @ns.marshal_list_with(channel_sub_dto, envelope='data')
    @cache.cached(timeout=60)
    def get(self) -> List[Channel]:
        """Get all Channels"""
        return ChannelService.get_all()

    @login_required
    @accepted_u_types('admin')
    @ns.expect(channel_dto, validate=True)
    @ns.marshal_with(channel_dto)
    def post(self) -> Channel:
        """Create a Single Channel"""
        return ChannelService.create(request.json)


@ns.route("/<string:channel_code>")
@ns.param("channel_code", "Channel database code")
class ChannelIdResource(Resource):
    @login_required
    def get(self, channel_code: str) -> Channel:
        """Get Single Channel"""
        return ChannelService.get_by_code(channel_code)

    @login_required
    @accepted_u_types('admin')
    def delete(self, channel_code: str) -> Response:
        """Delete Single Channel"""
        from flask import jsonify

        code = ChannelService.delete_by_code(channel_code)
        return jsonify(dict(status="Success", code=code))

    @login_required
    @accepted_u_types('admin')
    @ns.expect(channel_dto, validate=True)
    @ns.marshal_with(channel_dto, envelope='data')
    def put(self, channel_code: str) -> Channel:
        """Update Single Channel"""
        data_changes: ChannelInterface = request.json
        return ChannelService.update(channel_code, data_changes)
