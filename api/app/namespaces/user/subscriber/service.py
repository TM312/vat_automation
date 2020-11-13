from typing import List
import pandas as pd

from app.extensions import db
from flask import current_app, g
from werkzeug.exceptions import NotFound, InternalServerError

from .model import Subscriber
from .interface import SubscriberInterface



class SubscriberService:

    @staticmethod
    def get_all() -> List[Subscriber]:
        subscribers = Subscriber.query.all()
        return subscribers


    @staticmethod
    def get_by_id(subscriber_id: int) -> Subscriber:
        return Subscriber.query.filter_by(id = subscriber_id).first()

    @staticmethod
    def get_by_public_id(subscriber_public_id: str) -> Subscriber:
        return Subscriber.query.filter_by(public_id=subscriber_public_id).first()



    @staticmethod
    def create(subscriber_data: SubscriberInterface) -> Subscriber:
        new_subscriber = Subscriber(
            name = subscriber_data.get('name'),
            email = subscriber_data.get('email'),
            u_type_indicated=subscriber_data.get('u_type_indicated')
        )
        db.session.add(new_subscriber)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()
            raise InternalServerError

        return new_subscriber

    @staticmethod
    def update(subscriber_id: int, data_changes) -> Subscriber:
        subscriber = SubscriberService.get_by_id(subscriber_id)
        subscriber.update(data_changes)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()
            raise InternalServerError

        return subscriber


    @staticmethod
    def delete_by_public_id(subscriber_public_id: str):
        #check if subscriber exists in db
        subscriber = SubscriberService.get_by_public_id(subscriber_public_id)
        if subscriber:
            db.session.delete(subscriber)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Tax auditor (Public ID: {}) has been successfully deleted.'.format(subscriber_public_id)
            }
            return response_object
        else:
            raise NotFound('This tax auditor does not exist.')
