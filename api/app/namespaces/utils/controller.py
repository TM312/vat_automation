from flask_restx import Namespace, Resource

from .service import TemplateService
from . import transaction_notification_dto, notification_dto, transaction_notification_admin_dto
from .decorators import login_required



ns = Namespace("utils", description="Utilities Related Operations")  # noqa
ns.add_model(notification_dto.name, notification_dto)
ns.add_model(transaction_notification_dto.name, transaction_notification_dto)
ns.add_model(transaction_notification_admin_dto.name, transaction_notification_admin_dto)



@ns.route("/template/<string:name>")
class TemplateResource(Resource):
    @login_required
    # @confirmation_required
    # @ns.expect(transaction_dto, validate=True)
    def get(self, name):
        """Download A Template"""
        filename = name.split('.')[0] + '.csv'
        return TemplateService.download_file(filename)
