from typing import List
from flask import request
from flask_restx import Namespace, Resource

from . import Country
from . import country_dto
from .service import CountryService



ns = Namespace("Country", description="Country Related Operations")  # noqa
ns.add_model(country_dto.name, country_dto)


@api.route("/")
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


@api.route("/<str:country_code>")
@api.param("country_code", "Country database code")
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
