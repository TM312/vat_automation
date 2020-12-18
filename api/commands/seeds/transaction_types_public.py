from app.extensions import db



transaction_types_public = [
    {
        'code': 'SALE',
        'description': 'Buyer purchases good(s) from a seller.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'SALE',
    },
    {
        'code': 'REFUND',
        'description': 'A monetary change to a previously completed order. There may not be movement of goods. Address information may be blank for Refunds if the Refund occurred prior to the Return being completed. For example, MFN Refunds will not have a Return associated with them as Amazon is not aware of the movement details between buyer and seller.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'REFUND',
    },
    {
        'code': 'RETURN',
        'description': 'Physical return of goods sent back to an Amazon Fulfillment Centre.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'RETURN',
    },
    {
        'code': 'COMMINGLING_SELL',
        'description': 'The disposal of a product to another FBA seller (or Amazon Retail), participating in the Commingling Programme.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'SALE',
    },
    {
        'code': 'COMMINGLING_BUY',
        'description': 'The acquisition of a product from another FBA seller (or Amazon Retail), participating in the Commingling Programme.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'ACQUISITION',
    },
    {
        'code': 'FC_TRANSFER',
        'description': 'Seller’s inventory is transferred between Amazon’s EU cross border Fulfillment Centers.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'MOVEMENT',
    },
    {
        'code': 'INBOUND',
        'description': 'Seller sends inventory to an Amazon Fulfillment Center.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'INBOUND',
    },
    {
        'code': 'LIQUIDATION_SALE',
        'description': 'Selling excess inventory in bulk at a significant discount.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'SALE',
    },
    {
        'code': 'LIQUIDATION_REFUND',
        'description': 'A reversal/refund of a liquidation sale transaction. In case of disputes, a partial or full refund will be issued to the liquidator.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'REFUND',
    },
    {
        'code': 'DONATION',
        'description': 'Giving away excess inventory to a charitable organisation.',
        'platform_code': 'AMZ',
        'transaction_type_code': 'DONATION',
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
