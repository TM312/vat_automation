from typing import List
from flask import request, current_app
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Currency
from . import currency_dto
from .service import CurrencyService

from app.namespaces.utils.decorators import login_required, accepted_u_types
from app.extensions import cache


ns = Namespace("Currency", description="Currency Related Operations")  # noqa
ns.add_model(currency_dto.name, currency_dto)


@ns.route("/")
class CurrencyResource(Resource):
    """Currencies"""
    @login_required
    @ns.marshal_list_with(currency_dto, envelope='data')
    @cache.cached(timeout=60)
    def get(self) -> List[Currency]:
        """Get all Currencies"""
        return CurrencyService.get_all()

    @login_required
    @accepted_u_types('admin')
    @ns.expect(currency_dto, validate=True)
    @ns.marshal_with(currency_dto)
    def post(self) -> Currency:
        """Create a Single Currency"""
        return CurrencyService.create(request.parsed_obj)


@ns.route("/<string:currency_code>")
@ns.param("currency_code", "Currency database code")
class CurrencyIdResource(Resource):
    @login_required
    def get(self, currency_code: str) -> Currency:
        """Get Single Currency"""
        return CurrencyService.get_by_code(currency_code)

    @login_required
    @accepted_u_types('admin')
    def delete(self, currency_code: str) -> Response:
        """Delete Single Currency"""
        from flask import jsonify

        code = CurrencyService.delete_by_code(currency_code)
        return jsonify(dict(status="Success", code=code))

    @login_required
    @accepted_u_types('admin')
    @ns.expect(currency_dto, validate=True)
    @ns.marshal_with(currency_dto, envelope="data")
    def put(self, currency_code: str) -> Currency:
        """Update Single Currency"""

        current_app.logger.info('currency_code:', currency_code)

        data_changes: CurrencyInterface = request.json
        current_app.logger.info('data_changes:', data_changes)
        return CurrencyService.update(currency_code, data_changes)
