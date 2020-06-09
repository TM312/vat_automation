from flask_restx import Namespace, Resource

from .service import TemplateService
from .decorators import login_required



ns = Namespace("utils", description="Utilities Related Operations")  # noqa


@ns.route("/template/<string:name>")
class TemplateResource(Resource):
    @login_required
    # @confirmation_required
    # @ns.expect(transaction_dto, validate=True)
    def get(self, name):
        """Download A Template"""
        filename = name.split('.')[0] + '.csv'
        return TemplateService.download_file(filename)
