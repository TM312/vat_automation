from typing import List
from app.extensions import db

from . import Bundle
from .interface import BundleInterface

class BundleService:

    @staticmethod
    def get_or_create(account_id: int, item_id: int, transaction_input_given_id: str) -> Bundle:
        bundle = Bundle.query.join(Bundle.transaction_inputs, aliased=True).filter_by(account_id=account_id, item_id=item_id, given_id=transaction_input_given_id).first()
        if bundle:
            return bundle

        else:
            new_bundle = BundleService.create()

            return new_bundle

    @staticmethod
    def get_all() -> List[Bundle]:
        return Bundle.query.all()

    @staticmethod
    def get_by_id(bundle_id: int) -> Bundle:
        return Bundle.query.get(bundle_id)

    @staticmethod
    def get_by_public_id(bundle_public_id: str) -> Bundle:
        return Bundle.query.filter_by(public_id=bundle_public_id).first()

    @staticmethod
    def update_by_id(bundle_id: int, data_changes: BundleInterface) -> Bundle:
        bundle = BundleService.get_by_id(bundle_id)
        if bundle:
            bundle.update(data_changes)
            db.session.commit()
            return bundle

    @staticmethod
    def update_by_public_id(bundle_public_id: str, data_changes: BundleInterface) -> Bundle:
        bundle = BundleService.get_by_public_id(bundle_public_id)
        if bundle:
            bundle.update(data_changes)
            db.session.commit()
            return bundle

    @staticmethod
    def delete_by_id(bundle_id: int) -> List[int]:
        bundle = BundleService.get_by_id(bundle_id)
        if not bundle:
            return []
        db.session.delete(bundle)
        db.session.commit()
        return [bundle_id]

    @staticmethod
    def delete_by_public_id(bundle_public_id: str) -> List[int]:
        bundle = BundleService.get_by_public_id(bundle_public_id)
        if not bundle:
            return []
        db.session.delete(bundle)
        db.session.commit()
        return [bundle_public_id]

    @staticmethod
    def create() -> Bundle:
        bundle = Bundle()

        db.session.add(bundle)
        db.session.commit()

        return bundle
