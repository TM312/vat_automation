
class AMZHandler:

    @staticmethod
    def get_sale_transaction_input_by_bundle_id(bundle_id: int):
        from app.namespaces.transaction_input import TransactionInput

        return TransactionInput.query.filter(
            TransactionInput.bundle_id == bundle_id,
            or_(
                TransactionInput.transaction_type_public_code == 'SALE',
                TransactionInput.transaction_type_public_code == 'COMMINGLING_SELL'
            )
            ).first()
