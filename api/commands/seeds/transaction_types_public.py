from app.extensions import db



transaction_types_public = [
    {
        'code': 'SALE',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'SALE',
    },
    {
        'code': 'COMMINGLING_SELL',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'SALE',
    },
    {
        'code': 'REFUND',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'REFUND',
    },
    {
        'code': 'RETURN',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'RETURN',
    },
    {
        'code': 'COMMINGLING_BUY',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'ACQUISITION',
    },
    {
        'code': 'FC_TRANSFER',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'MOVEMENT',
    },
    {
        'code': 'INBOUND',
        'description': '',
        'platform_code': 'AMZ',
        'transaction_type_code': 'INBOUND',
    },
]


class TransactionTypePublicSeedService:
    @staticmethod
    def seed_transaction_types_public():
        from app.namespaces.transaction_type_public.service import TransactionTypePublicService
        for i, transaction_types_public_data in enumerate(transaction_types_public):
            try:
                TransactionTypePublicService.create(transaction_types_public_data)
            except:
                db.session.rollback()
                raise

        response_object = {
            'status': 'success',
            'message': 'Successfully created public transaction types ({} objects)'.format(str(i+1))
        }

        return response_object
