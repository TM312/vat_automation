from typing import List
from . import Bundle

class BundleService:

    @staticmethod
    def get_or_create(account: 'app.namespaces.account.Account', item: 'app.namespaces.item.Item', transaction_input_given_id: str) -> Bundle:
        bundle = Bundle.query.join(Bundle.transaction_inputs, aliased=True).filter_by(account_id=account.id, item_id=item.id, given_id=transaction_input_given_id).first()
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
    def update(bundle: Bundle, data_changes: BundleInterface) -> Bundle:
        bundle.update(data_changes)
        db.session.commit()
        return bundle

    @staticmethod
    def delete_by_id(bundle_id: int) -> List[int]:
        bundle = Bundle.query.filter(Bundle.bundle_id == bundle_id).first()
        if not bundle:
            return []
        db.session.delete(bundle)
        db.session.commit()
        return [bundle_id]

    @staticmethod
    def create() -> Bundle:
        bundle = Bundle()

        db.session.add(bundle)
        db.session.commit()

        return bundle
