from typing import List
from flask import current_app

from app.extensions import db

from . import Admin
from .interface import AdminInterface

class AdminService:

    @staticmethod
    def get_all() -> List[Admin]:
        admins = Admin.query.all()
        return admins

    @staticmethod
    def get_by_id(admin_id: int) -> Admin:
        return Admin.query.filter(Admin.id == admin_id).first()


    @staticmethod
    def update(admin_id: int, data_changes: AdminInterface) -> Admin:
        admin = AdminService.get_by_id(admin_id)
        admin.update(data_changes)
        db.session.commit()
        return admin

    @staticmethod
    def delete_by_id(admin_id: str):
        admin = AdminService.get_by_id(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Admin (code: {}) has been successfully deleted.'.format(admin_id)
            }
            return response_object
        else:
            raise NotFound('This admin does not exist.')

    @staticmethod
    def create(admin_data: AdminInterface) -> Admin:
        admin = Admin.query.filter_by(email=admin_data.get('email')).first()
        if not admin:
            #create new admin based on Admin model
            admin = Admin(
                email=admin_data.get('email'),
                password=admin_data.get('password'),
                role='employee'
            )
            #add admin to db
            db.session.add(admin)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }


            return response_object
        else:
            response_object = {
                'status': 'error',
                'message': 'A admin with the this email address already exists. Try logging in instead.'
            }
            return response_object
