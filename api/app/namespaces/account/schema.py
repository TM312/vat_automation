# import json
from flask_restx import Model, fields
# from app.extensions import ma

from . import Account
from ..transaction import transaction_sub_dto
from ..transaction_input import transaction_input_sub_dto

account_sub_dto = Model('account_sub', {
    'public_id': fields.String(readonly=True),
    'given_id': fields.String,
    'channel_code': fields.String,

})


account_dto = account_sub_dto.clone('account', {
    'created_by': fields.String(attribute=lambda x: x.creator.name, readonly=True),
    'created_on': fields.Date(readonly=True),
    'modified_at': fields.DateTime(readonly=True),
    'seller_firm': fields.String(attribute=lambda x: x.seller_firm.name, readonly=True),
    'transaction_inputs': fields.List(fields.Nested(transaction_input_sub_dto)),
    # 'transactions': fields.List(fields.Nested(transaction_sub_dto))
})


account_admin_dto = account_dto.clone('account_admin', {
    'id': fields.Integer(readonly=True),
    'seller_firm_id': fields.Integer(readonly=True)
})


class AccountSubSchema:  #(ma.SQLAlchemySchema):

    @staticmethod
    def get_account_sub(account):

        #added cfeated on
        account_as_dict = {
            'public_id': str(account.public_id),
            'given_id': account.given_id,
            'channel_code': account.channel_code
        }
        return account_as_dict


    #     class Meta:
    #         model = Account

    #     public_id = ma.auto_field()
    #     given_id = ma.auto_field()
    #     channel_code = ma.auto_field()
    #     created_on = ma.auto_field()
