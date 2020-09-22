from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Channel
from . import channel_dto
from .service import ChannelService

from app.namespaces.utils.decorators import login_required, employer_required


ns = Namespace("Channel", description="Channel Related Operations")  # noqa
ns.add_model(channel_dto.name, channel_dto)


@ns.route("/")
class ChannelResource(Resource):
    """Channels"""
    @ns.marshal_list_with(channel_dto, envelope='data')
    def get(self) -> List[Channel]:
        """Get all Channels"""
        return ChannelService.get_all()

    @ns.expect(channel_dto, validate=True)
    @ns.marshal_with(channel_dto)
    def post(self) -> Channel:
        """Create a Single Channel"""
        return ChannelService.create(request.parsed_obj)


@ns.route("/<string:channel_code>")
@ns.param("channel_code", "Channel database code")
class ChannelIdResource(Resource):
    def get(self, channel_code: str) -> Channel:
        """Get Single Channel"""
        return ChannelService.get_by_code(channel_code)

    def delete(self, channel_code: str) -> Response:
        """Delete Single Channel"""
        from flask import jsonify

        code = ChannelService.delete_by_code(channel_code)
        return jsonify(dict(status="Success", code=code))

    @ns.expect(channel_dto, validate=True)
    @ns.marshal_with(channel_dto)
    def put(self, channel_code: str) -> Channel:
        """Update Single Channel"""

        data_changes: ChannelInterface = request.parsed_obj
        return ChannelService.update(channel_code, data_changes)
