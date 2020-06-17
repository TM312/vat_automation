from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Currency
from . import currency_dto
from .service import CurrencyService


ns = Namespace("Currency", description="Currency Related Operations")  # noqa
ns.add_model(currency_dto.name, currency_dto)


@ns.route("/")
class CurrencyResource(Resource):
    """Currencys"""
    @ns.marshal_list_with(currency_dto, envelope='data')
    def get(self) -> List[Currency]:
        """Get all Currencys"""
        return CurrencyService.get_all()

    @ns.expect(currency_dto, validate=True)
    @ns.marshal_with(currency_dto)
    def post(self) -> Currency:
        """Create a Single Currency"""
        return CurrencyService.create(request.parsed_obj)


@ns.route("/<string:currency_code>")
@ns.param("currency_code", "Currency database code")
class CurrencyIdResource(Resource):
    def get(self, currency_code: str) -> Currency:
        """Get Single Currency"""
        return CurrencyService.get_by_code(currency_code)

    def delete(self, currency_code: str) -> Response:
        """Delete Single Currency"""
        from flask import jsonify

        id = CurrencyService.delete_by_code(currency_code)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(currency_dto, validate=True)
    @ns.marshal_with(currency_dto)
    def put(self, currency_code: str) -> Currency:
        """Update Single Currency"""

        data_changes: CurrencyInterface = request.parsed_obj
        return CurrencyService.update(currency_code, data_changes)
