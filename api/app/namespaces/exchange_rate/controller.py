from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from .service import ExchangeRateService
from . import ExchangeRate
from . import exchange_rate_dto

from app.namespaces.utils.decorators import login_required, employer_required


ns = Namespace("ExchangeRate", description="ExchangeRate Related Operations")  # noqa
ns.add_model(exchange_rate_dto.name, exchange_rate_dto)


@ns.route("/")
class ExchangeRateResource(Resource):
    """ExchangeRates"""
    @ns.marshal_list_with(exchange_rate_dto, envelope='data')
    def get(self) -> List[ExchangeRate]:
        """Get all ExchangeRates"""
        return ExchangeRateService.get_all()

    @ns.expect(exchange_rate_dto, validate=True)
    @ns.marshal_with(exchange_rate_dto)
    def post(self) -> ExchangeRate:
        """Create a Single ExchangeRate"""
        return ExchangeRateService.create(request.parsed_obj)


@ns.route("/<int:exchange_rate_id>")
@ns.param("exchange_rate_id", "ExchangeRate database ID")
class ExchangeRateIdResource(Resource):
    def get(self, exchange_rate_id: int) -> ExchangeRate:
        """Get Single ExchangeRate"""
        return ExchangeRateService.get_by_id(exchange_rate_id)

    def delete(self, exchange_rate_id: int) -> Response:
        """Delete Single ExchangeRate"""
        from flask import jsonify

        id = ExchangeRateService.delete_by_id(exchange_rate_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(exchange_rate_dto, validate=True)
    @ns.marshal_with(exchange_rate_dto)
    def put(self, exchange_rate_id: int) -> ExchangeRate:
        """Update Single ExchangeRate"""

        data_changes: ExchangeRateInterface = request.parsed_obj
        return ExchangeRateService.update(exchange_rate_id, data_changes)
