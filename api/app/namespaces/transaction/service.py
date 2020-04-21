import os
import shutil
from pathlib import Path
from typing import List
from datetime import datetime

from flask import current_app
from flask import send_from_directory

from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound, RequestEntityTooLarge, UnsupportedMediaType, Abort


from app.extensions import db
from .model import Transaction, TransactionInput
# from .schema import transaction_dto

from ...user.service_parent import UserService


class TransactionService:
    # @staticmethod
    # def get_all() -> List[Transaction]:
    #     transaction = Transaction.query.all()
    #     return transactions

    # @staticmethod
    # def get_by_id(public_id: str) -> Transaction:
    #     transaction = Transaction.query.filter(Transaction.public_id == public_id).first()
    #     if transaction:
    #         return transaction
    #     else:
    #         raise NotFound('This tax record does not exist.')

    @staticmethod
    def delete_by_id(public_id: str):
        #check if transaction exists in db
        transaction = Transaction.query.filter(
            Transaction.public_id == public_id).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Transaction (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This transaction does not exist.')

    @staticmethod
    def get_own(user):
        transactions = Transaction.query.filter_by(owner_id=user.id).all().order_by(
            Transaction.created_on.desc())
        return transactions

    @staticmethod
    def download_file(transaction, filename):
        dirpath = os.path.join(
            current_app.config['BASE_PATH_MEDIA'],
            str(transaction.owner.public_id),
            'transaction',
            transaction.activity_period)
        #filename = '202004_transaction_input_55462838340018328.csv'
        return send_from_directory(dirpath, filename=filename, as_attachment=True)

    # @staticmethod
    # def followed_transactions(tax_auditor):
    #     return Transaction.query.join(
    #         clients, (clients.c.client_id == Transaction.owner_id)).filter(
    #             clients.c.tax_auditor_id == tax_auditor.id).order_by(
    #                 Transaction.created_on.desc())


    @staticmethod
    def create(
            user,
            seller_firm,
            platform,
            final_dirpath,
            activity_period) -> Transaction:

        ## A tax record is created by uploading a platform specific input file

        # check if tax record already exists in db
        transaction = Transaction.query.filter_by(
            owner=seller_firm.id
            activity_period=activity_period,
        ).first()

        if not transaction:
            # create new tax record
            new_transaction = Transaction(
                creator_id=user.id,
                accounting_firm_id=user.employer_id,
                activity_period=activity_period,
                owner_id=seller_firm.id,
                storage_dir=final_dirpath,
            )
            # add new_transaction to db
            db.session.add(new_transaction)

         else:
            transaction.update(
                creator_id=user.id,
                accounting_firm_id=user.employer_id
            )

        db.session.commit()

        return new_transaction

    @staticmethod
    def create_input(
        platform,
        original_input_name,
        formatted_input_name,
        transaction) -> TransactionInput:

        # check if tax record input already exists in db
        transaction_input = Transaction.query.filter_by(
            platform=platform,
            transaction_id=transaction.id
        ).first()


        if not transaction_input:
            # create new tax record input
            new_transaction_input = TransactionInput(
                platform=platform,
                transaction_id=transaction.id,
                original_input_name=original_input_name,
                formatted_input_name=formatted_input_name
            )

            # add new_transaction to db
            db.session.add(new_transaction_input)

        else:
            transaction_input.update(
                original_input_name=original_input_name,
                formatted_input_name=formatted_input_name
            )

            transaction.update()

        db.session.commit()
