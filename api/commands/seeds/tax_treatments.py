tax_treatments = [
    {
        'code':'LOCAL_SALE',
        'name': 'Local Sale'
        'description': 'Transaction taxable in the country of departure. Domestic Sale (Departure = Arrival Country). Tax Treatment limited to Transaction Types SALE and REFUND.'
    },
    {
        'code': 'LOCAL_SALE_REVERSE_CHARGE',
        'name': 'Local Sale Reverse Charge',
        'description': 'Transaction taxable with the Reverse Charge Mechanism. Domestic Sale (Departure = Arrival Country). Tax Treatment limited to B2B Transactions (valid Customer VAT Number), to Transaction Types SALE and REFUND, and to certain Item Types, or to the country of establishment of the Seller and the Customer.'
    },
    {
        'code': 'DISTANCE_SALE',
        'name': 'Distance Sale',
        'description': 'Transaction taxable in the country of arrival. EU Cross-border Sale (Departure != Arrival Country). Limited to B2C Transactions, and to Transaction Types SALE and REFUND.'
    },
    {
        'code': 'INTRA_COMMUNITY_SALE',
        'name': 'Intra Community Sale',
        'description': 'Transaction taxable with the Reverse Charge Mechanism. EU Cross-border Sale (Departure != Arrival Country). Tax Treatment limited to B2B Transactions (valid Customer VAT Number).'
    },
    {
        'code': 'EXPORT',
        'name': 'Export',
        'description': 'Sale of good(s) leaving the Single European Economic Area. Limited to Transaction Types SALE (and REFUND).'
    },
    {
        'code': 'LOCAL_ACQUISITION',
        'name': 'Local Acquisition',
        'description': 'Transaction taxable in the country of departure. Domestic Sale (Departure = Arrival Country). Tax Treatment limited to Transaction Types SALE and REFUND.'
    },
    {
        'code': 'INTRA_COMMUNITY_ACQUISITION',
        'name': 'Intra Community Acquisition',
        'description': 'Transaction taxable with the Reverse Charge Mechanism. EU Cross-border Acquisition (Departure != Arrival Country). Tax Treatment limited to B2B Transactions (valid Customer VAT Number).'
    },
    {
        'code': 'IMPORT',
        'name': 'Import',
        'description': 'Import of good(s) entering the Single European Economic Area.'
    }
]






class TaxTreatmentSeedService:
    @staticmethod
    def append_transaction_types_to_tax_treatments():
        transaction_type_tax_treatment_dict = [
            {'SALE': ['LOCAL_SALE', 'LOCAL_SALE_REVERSE_CHARGE', 'DISTANCE_SALE', 'INTRA_COMMUNITY_SALE', 'EXPORT']},
            {'REFUND': ['LOCAL_SALE', 'LOCAL_SALE_REVERSE_CHARGE', 'DISTANCE_SALE', 'INTRA_COMMUNITY_SALE', 'EXPORT']},
            {'ACQUISITION': ['LOCAL_ACQUISITION', 'INTRA_COMMUNITY_ACQUISITION', 'IMPORT']},
            {'MOVEMENT': ['INTRA_COMMUNITY_SALE', 'EXPORT', 'INTRA_COMMUNITY_ACQUISITION', 'IMPORT']}
        ]

        try:
            for key, val in transaction_type_tax_treatment_dict.items():
            transaction_type = TransactionType.query.filter_by(code=key).first()
            for tax_treatment_code in val:
                tax_treatment = TransactionType.query.filter_by(code=tax_treatment_code).first()
                transaction_type.tax_treatments.append(tax_treatment)


            response_object = {
                'status': 'success',
                'message': 'Successfully attached tax treatments to transaction types.'
            }

        except:
            response_object = {
                'status': 'error',
                'message': 'Failed attach tax treatments to transaction types.'
            }

        return response_object
