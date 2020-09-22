from typing import List
from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Country, EU
from . import country_dto, country_sub_dto, eu_dto
from .service import CountryService

from app.namespaces.utils.decorators import login_required



ns = Namespace("Country", description="Country Related Operations")  # noqa
ns.add_model(country_dto.name, country_dto)
ns.add_model(country_sub_dto.name, country_sub_dto)
ns.add_model(eu_dto.name, eu_dto)


@ns.route("/")
class CountryResource(Resource):
    """Countrys"""
    @ns.marshal_list_with(country_dto, envelope='data')
    def get(self) -> List[Country]:
        """Get all Countrys"""
        return CountryService.get_all()

    @ns.expect(country_dto, validate=True)
    @ns.marshal_with(country_dto)
    def post(self) -> Country:
        """Create a Single Country"""
        return CountryService.create(request.parsed_obj)


@ns.route("/<string:country_code>")
@ns.param("country_code", "Country database code")
class CountryIdResource(Resource):
    def get(self, country_code: str) -> Country:
        """Get Single Country"""
        return CountryService.get_by_code(country_code)

    def delete(self, country_code: str) -> Response:
        """Delete Single Country"""
        from flask import jsonify

        id = CountryService.delete_by_code(country_code)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(country_dto, validate=True)
    @ns.marshal_with(country_dto)
    def put(self, country_code: str) -> Country:
        """Update Single Country"""

        data_changes: CountryInterface = request.parsed_obj
        return CountryService.update(country_code, data_changes)


@ns.route("/eu/<string:date_string>")
class CountryEUResource(Resource):
    """EU Countrys"""
    @login_required
    @ns.marshal_with(eu_dto, envelope='data')
    def get(self, date_string) -> EU:
        """Get all Countrys"""
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return CountryService.get_eu_by_date(date)
