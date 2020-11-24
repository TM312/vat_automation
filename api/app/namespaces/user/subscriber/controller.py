from typing import List, BinaryIO

from flask import request, g
from flask.wrappers import Response

from flask_restx import Namespace, Resource

from . import Subscriber
from . import subscriber_dto, subscriber_dto_admin, subscriber_sub_dto
from .service import SubscriberService
from .interface import SubscriberInterface

from app.namespaces.utils.decorators import login_required, accepted_u_types, confirmation_required
from app.namespaces.utils.service import TemplateService



ns = Namespace("Subscriber", description="Subscriber Related Operations")  # noqa
ns.add_model(subscriber_dto.name, subscriber_dto)
ns.add_model(subscriber_dto_admin.name, subscriber_dto_admin)
ns.add_model(subscriber_sub_dto.name, subscriber_sub_dto)
# https://flask-restx.readthedocs.io/en/latest/api.html#flask_restx.Model
# https://github.com/python-restx/flask-restx/blob/014eb9591e61cd3adbbd29a38b76df6a688f067b/flask_restx/namespace.py


@ns.route('/')
class SubscriberResource(Resource):
    '''Get all Subscriber'''
    @login_required
    @accepted_u_types('admin')
    @ns.marshal_list_with(subscriber_dto, envelope='data')
    def get(self) -> List[Subscriber]:
        '''List Of Registered Subscriber Firms'''
        return SubscriberService.get_all()


    @ns.expect(subscriber_dto, validate=True)
    @ns.marshal_with(subscriber_dto, envelope='data')
    def post(self) -> Subscriber:
        """Create A Single Tax Auditor"""
        subscriber_data: SubscriberInterface = request.json
        print('request.json', request.json, flush=True)
        return SubscriberService.get_or_create(subscriber_data)
