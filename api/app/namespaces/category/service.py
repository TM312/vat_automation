from typing import List, BinaryIO, Dict

from app.extensions import db

from . import Category
from .interface import CategoryInterface


class CategoryService:
    @staticmethod
    def get_all() -> List[Category]:
        categorys = Category.query.all()
        return categorys

    @staticmethod
    def get_by_id(category_id: int) -> Category:
        return Category.query.filter_by(id = category_id).first()

    @staticmethod
    def get_by_public_id(category_public_id: str) -> Category:
        return Category.query.filter_by(public_id = category_public_id).first()

    @staticmethod
    def update(category_id: int, data_changes: CategoryInterface) -> Category:
        category = CategoryService.get_by_id(category_id)
        if category:
            category.update(data_changes)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            return category

    @staticmethod
    def update_by_public_id(category_public_id: str, data_changes: CategoryInterface) -> Category:
        category = CategoryService.get_by_public_id(category_public_id)
        if category:
            category.update(data_changes)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            return category

    @staticmethod
    def delete_by_id(category_id: int):
        category = Category.query.filter_by(id = category_id).first()
        if category:
            db.session.delete(category)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

            response_object = {
                'status': 'success',
                'message': 'Category (code: {}) has been successfully deleted.'.format(category_id)
            }
            return response_object
        else:
            raise NotFound('This category does not exist.')

    @staticmethod
    def delete_by_public_id(category_public_id: str):
        category = CategoryService.get_by_public_id(category_public_id)
        if category:
            db.session.delete(category)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Category (code: {}) has been successfully deleted.'.format(category_public_id)
            }
            return response_object
        else:
            raise NotFound('This category does not exist.')



    @staticmethod
    def create(category_data: CategoryInterface) -> Category:
        new_category = Category(
            created_by = category_data.get('created_by'),
            level = category_data.get('level'),
            business_id = category_data.get('business_id'),
            parent_id = category_data.get('parent_id')
        )

        db.session.add(new_category)
        db.session.commit()

        return new_category
