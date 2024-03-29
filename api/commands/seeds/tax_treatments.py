from app.namespaces.transaction_type.model import TransactionType
from app.namespaces.tax.tax_treatment.model import TaxTreatment


tax_treatments = [
    {
        'code': 'LOCAL_SALE',
        'name': 'Local Sale',
        'description': 'Local Sales indicate that departure and arrival country are the same. They only apply to Sales and Refunds and are taxable in the country of departure.'
    },
    {
        'code': 'LOCAL_SALE_REVERSE_CHARGE',
        'name': 'Local Sale Reverse Charge',
        'description': 'In the case of B2B transactions Local Sales may under certain conditions be taxable with the Reverse Charge Mechanism. This for instance, depends on the item type or to the country of establishment of the transacting businesses.'
    },
    {
        'code': 'DISTANCE_SALE',
        'name': 'Distance Sale',
        'description': 'Distance Sales indicate the case of cross-border sales or refunds within the EU. These transactions are taxable in the country of arrival and only apply to B2C transactions.'
    },
    {
        'code': 'NON_TAXABLE_DISTANCE_SALE',
        'name': 'Non-taxable Distance Sale',
        'description': 'Distance Sales commonly require non-taxable but additional reporting in the departure country.'
    },
    {
        'code': 'INTRA_COMMUNITY_SALE',
        'name': 'Intra Community Sale',
        'description': 'Intra Community Sales are B2B EU cross-border transactions to which the Reverse Charge Mechanism applies.'
    },
    {
        'code': 'EXPORT',
        'name': 'Export',
        'description': 'Exports refer to the sale (or refund) of goods leaving the Single European Economic Area.'
    },
    {
        'code': 'LOCAL_ACQUISITION',
        'name': 'Local Acquisition',
        'description': 'Local Acquisitions apply to transactions not outside the scope of sales and refunds.'
    },
    {
        'code': 'INTRA_COMMUNITY_ACQUISITION',
        'name': 'Intra Community Acquisition',
        'description': 'Intra Community Acquisitions are transaction to which the Reverse Charge taxation mechhanism applies. They are limited to B2B transactions across EU borders.'
    }  # ,
    # {
    #     'code': 'IMPORT',
    #     'name': 'Import',
    #     'description': 'Import of good(s) entering the Single European Economic Area.'
    # }
]


class TaxTreatmentSeedService:
    @staticmethod
    def append_transaction_types_to_tax_treatments():
        transaction_type_tax_treatment_dict = [
            {'SALE': ['LOCAL_SALE', 'LOCAL_SALE_REVERSE_CHARGE',
                      'DISTANCE_SALE', 'INTRA_COMMUNITY_SALE', 'EXPORT']},
            {'REFUND': ['LOCAL_SALE', 'LOCAL_SALE_REVERSE_CHARGE',
                        'DISTANCE_SALE', 'INTRA_COMMUNITY_SALE', 'EXPORT']},
            {'ACQUISITION': ['LOCAL_ACQUISITION']},
            {'MOVEMENT': ['INTRA_COMMUNITY_SALE',
                          'INTRA_COMMUNITY_ACQUISITION']},
            # !!! recheck if the two cases below are correct
            {'RETURN': ['INTRA_COMMUNITY_SALE',
                        'INTRA_COMMUNITY_ACQUISITION']},
            {'INBOUND': ['INTRA_COMMUNITY_SALE',
                         'INTRA_COMMUNITY_ACQUISITION']}

        ]

        try:
            for key, val in transaction_type_tax_treatment_dict.items():
                transaction_type = TransactionType.query.filter_by(
                    code=key).first()
                for tax_treatment_code in val:  # --> 'LOCAL_SALE'
                    tax_treatment = TaxTreatment.query.filter_by(
                        code=tax_treatment_code).first()
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
