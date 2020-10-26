from typing import List
from app.extensions import db


from . import TransactionType
from .interface import TransactionTypeInterface

class TransactionTypeService:
    @staticmethod
    def get_all() -> List[TransactionType]:
        return TransactionType.query.all()

    @staticmethod
    def get_by_code(transaction_type_code: str) -> TransactionType:
        return TransactionType.query.filter_by(code=transaction_type_code).first()


    @staticmethod
    def delete_by_code(transaction_type_code: str):
        transaction_type = TransactionType.query.filter_by(code=transaction_type_code).first()
        if transaction_type:
            db.session.delete(transaction_type)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'TransactionType (name: {}) has been successfully deleted.'.format(transaction_type.name)
            }
            return response_object
        else:
            raise NotFound('This transaction_type does not exist.')

    @staticmethod
    def create(transaction_type_data: TransactionTypeInterface) -> TransactionType:

        new_transaction_type = TransactionType(
            code = transaction_type_data.get('code'),
            name = transaction_type_data.get('name'),
            description = transaction_type_data.get('description')
        )

        #add seller firm to db
        db.session.add(new_transaction_type)
        db.session.commit()

        return new_transaction_type


    # @staticmethod
    # def get_transaction_type_by_platform_public_code(transaction_type_public_code: str, platform_code: str) -> TransactionType:
    #     if platform_code == 'AMZ':
    #         if transaction_type_public_code == 'SALE' or transaction_type_public_code == 'COMMINGLING_SELL':
    #             # transaction_type = TransactionTypeService.get_by_platform_public_type(platform_code, transaction_type_public_code)
    #             TransactionType.query.filter_by(code="SALE").first()

    #         elif transaction_type_public_code == 'REFUND':
    #             transaction_type = TransactionType.query.filter_by(code="REFUND").first()

    #         elif transaction_type_public_code == 'RETURN':
    #             transaction_type = TransactionType.query.filter_by(code="RETURN").first()

    #         elif transaction_type_public_code == 'COMMINGLING_BUY':
    #             transaction_type = TransactionType.query.filter_by(code="ACQUISITION").first()

    #         elif transaction_type_public_code == 'FC_TRANSFER':
    #             transaction_type = TransactionType.query.filter_by(code="MOVEMENT").first()

    #         elif transaction_type_public_code == 'INBOUND':
    #             transaction_type = TransactionType.query.filter_by(code="INBOUND").first()

    #         else:
    #             print("Function: TransactionService -> get_transaction_type_by_public_code_account", flush=True)
    #             raise NotFound('The indicated transaction type "{}" is not supported. Please get in touch with one of the administrators.'.format(transaction_type_public_code))
    #             current_app.logger.warning('Unrecognized public transaction type code: {}'.format(transaction_type_public_code))

    #     else:
    #         print("Function: TransactionService -> get_transaction_type_by_public_code_account -> platform not found", flush=True)
    #         raise NotFound('The platform for the transaction code "{}" is currently not supported. Please get in touch with one of the admins.'.format(transaction_type_public_code))

    #     return transaction_type
