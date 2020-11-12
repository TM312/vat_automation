from typing import List, BinaryIO
from flask import request

from flask_restx import Namespace, Resource
from flask.wrappers import Response

from .service import CategoryService
from . import Category
from . import category_dto

from app.namespaces.utils.decorators import login_required, employer_required


ns = Namespace("Category", description="Item Hierarchy Related Operations")  # noqa
ns.add_model(category_dto.name, category_dto)


@ns.route("/")
class CategoryResource(Resource):
    """Item Hierarchy"""
    @ns.marshal_list_with(category_dto, envelope='data')
    def get(self) -> List[Category]:
        """Get all Categorys"""
        return CategoryService.get_all()

    @ns.expect(category_dto, validate=True)
    @ns.marshal_with(category_dto)
    def post(self) -> Category:
        """Create a Single Category"""
        return CategoryService.create(request.json)
