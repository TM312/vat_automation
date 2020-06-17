from typing import List
from flask import request
from flask_restx import Namespace, Resource
from flask.wrappers import Response

from . import Bundle
from . import bundle_dto
from .service import BundleService
from .interface import BundleInterface



ns = Namespace("Bundle", description="Bundle Related Operations")  # noqa
ns.add_model(bundle_dto.name, bundle_dto)



@ns.route("/")
class BundleResource(Resource):
    """Bundles"""
    @ns.marshal_list_with(bundle_dto, envelope='data')
    def get(self) -> List[Bundle]:
        """Get all Bundles"""
        return BundleService.get_all()

    @ns.expect(bundle_dto, validate=True)
    @ns.marshal_with(bundle_dto)
    def post(self) -> Bundle:
        """Create a Single Bundle"""
        return BundleService.create()


@ns.route("/<int:bundle_id>")
@ns.param("bundle_id", "Bundle database ID")
class BundleIdResource(Resource):
    def get(self, bundle_id: int) -> Bundle:
        """Get Single Bundle"""
        return BundleService.get_by_id(bundle_id)

    def delete(self, bundle_id: int) -> Response:
        """Delete Single Bundle"""
        from flask import jsonify

        id = BundleService.delete_by_id(bundle_id)
        return jsonify(dict(status="Success", id=id))

    @ns.expect(bundle_dto, validate=True)
    @ns.marshal_with(bundle_dto)
    def put(self, bundle_id: int) -> Bundle:
        """Update Single Bundle"""

        data_changes: BundleInterface = request.parsed_obj
        Bundle = BundleService.get_by_id(bundle_id)
        return BundleService.update(Bundle, data_changes)
