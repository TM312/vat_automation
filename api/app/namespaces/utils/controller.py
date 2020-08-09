from flask_restx import Namespace, Resource, reqparse

from .service import TemplateService, NotificationService
from . import transaction_notification_dto, notification_dto, transaction_notification_admin_dto, seller_firm_notification_dto
from .decorators import login_required

parser = reqparse.RequestParser()
parser.add_argument('page', type=int)



ns = Namespace("utils", description="Utilities Related Operations")  # noqa
ns.add_model(notification_dto.name, notification_dto)
ns.add_model(transaction_notification_dto.name, transaction_notification_dto)
ns.add_model(transaction_notification_admin_dto.name, transaction_notification_admin_dto)
ns.add_model(seller_firm_notification_dto.name, seller_firm_notification_dto)



@ns.route("/template/<string:name>")
class TemplateResource(Resource):
    @login_required
    # @confirmation_required
    # @ns.expect(transaction_dto, validate=True)
    def get(self, name):
        """Download A Template"""
        filename = name.split('.')[0] + '.csv'
        return TemplateService.download_file(filename)


@ns.route("/notifications/key_accounts")
class SellerFirmNotificationResource(Resource):
    @login_required
    @ns.marshal_list_with(seller_firm_notification_dto, envelope='data')
    def get(self) -> TransactionInput:
        """Get Single TransactionInput"""
        args = parser.parse_args()
        return NotificationService.get_all_key_account_notifications(paginate=True, page=args.get('page'))
