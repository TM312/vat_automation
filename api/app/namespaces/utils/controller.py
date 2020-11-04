from typing import List
from flask import current_app, request
from flask_restx import Namespace, Resource, reqparse

from . import Notification, SellerFirmNotification
from . import (
    transaction_notification_dto,
    notification_dto,
    transaction_notification_admin_dto,
    seller_firm_notification_dto
    )
from .service import TemplateService, NotificationService

from .decorators import login_required

parser = reqparse.RequestParser()
parser.add_argument('page', type=int)

#

ns = Namespace("utils", description="Utilities Related Operations")  # noqa
ns.add_model(notification_dto.name, notification_dto)
ns.add_model(transaction_notification_dto.name, transaction_notification_dto)
ns.add_model(transaction_notification_admin_dto.name, transaction_notification_admin_dto)
ns.add_model(seller_firm_notification_dto.name, seller_firm_notification_dto)



@ns.route("/template/<string:name>")
class TemplateResource(Resource):
    @login_required
    def get(self, name):
        """Download A Template"""
        filename = name.split('.')[0] + '.csv'
        return TemplateService.download_file(filename)


@ns.route("/notifications/key_accounts")
class SellerFirmNotificationResource(Resource):
    @login_required
    @ns.marshal_list_with(seller_firm_notification_dto, envelope='data')
    def get(self) -> List[SellerFirmNotification]:
        """Get Single TransactionInput"""
        return NotificationService.get_all_key_account_notifications()


@ns.route("/tasks")
class AsyncTask(Resource):
    def get(self):
        from app.tasks.asyncr import long_task
        room = request.args.get('room')

        result = long_task.apply_async(retry=True, kwargs={"room": room})
        return {
            "task_id": result.id,
        }


@ns.route("/status/<string:task_id>")
class AsyncTaskStatus(Resource):
    def get(self, task_id):
        from app.tasks.asyncr import long_task
        current_app.logger.debug("{} {}".format(
            request.method, request.url_rule))
        result = long_task.AsyncResult(task_id)
        current_app.logger.info(
            "Task (id: {}, state: {}, queue: {}) is retrieved from backend {}."
            .format(result.task_id, result.state, result.queue, result.backend))

        if result.ready():
            return {
                "state": result.state,
                "ready": result.ready(),
                'result': result.get()
            }
        else:
            return {
                "state": result.state,
                "ready": result.ready(),
            }
