from typing import List
from app.extensions import db


from . import TransactionTypePublic
from .interface import TransactionTypePublicInterface

class TransactionTypePublicService:
    @staticmethod
    def get_all() -> List[TransactionTypePublic]:
        return TransactionTypePublic.query.all()

    @staticmethod
    def get_by_id(transaction_type_public_id: int) -> TransactionTypePublic:
        return TransactionTypePublic.query.filter_by(id=transaction_type_public_id).first()

    @staticmethod
    def get_by_code_platform_code(code: str, platform_code: str) -> TransactionTypePublic:
        return TransactionTypePublic.query.filter(TransactionTypePublic.code == code, TransactionTypePublic.platform_code == platform_code).first()


    @staticmethod
    def delete_by_id(transaction_type_public_id: int):
        transaction_type_public = TransactionTypePublic.query.filter_by(id=transaction_type_public_id).first()
        if transaction_type_public:
            db.session.delete(transaction_type_public)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'TransactionTypePublic (name: {}) has been successfully deleted.'.format(transaction_type_public.name)
            }
            return response_object
        else:
            raise NotFound('This transaction_type_public does not exist.')

    @staticmethod
    def create(transaction_type_public_data: TransactionTypePublicInterface) -> TransactionTypePublic:

        new_transaction_type_public = TransactionTypePublic(
            code=transaction_type_public_data.get('code'),
            name=transaction_type_public_data.get('name'),
            description=transaction_type_public_data.get('description'),
            platform_code=transaction_type_public_data.get('platform_code'),
            transaction_type_code=transaction_type_public_data.get('transaction_type_code')
        )

        #add seller firm to db
        db.session.add(new_transaction_type_public)
        db.session.commit()

        return new_transaction_type_public
