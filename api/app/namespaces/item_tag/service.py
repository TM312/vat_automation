from typing import List
from app.extensions import db


from . import ItemTag
from .interface import ItemTagInterface

class ItemTagService:
    @staticmethod
    def get_all() -> List[ItemTag]:
        return ItemTag.query.all()

    @staticmethod
    def get_by_id(item_id: int) -> ItemTag:
        return ItemTag.query.filter_by(id=item_id).first()


    @staticmethod
    def delete_by_id(item_id: int):
        item_tag = ItemTag.query.filter_by(id=item_id).first()
        if item_tag:
            db.session.delete(item_tag)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'ItemTag (name: {}) has been successfully deleted.'.format(item_tag.name)
            }
            return response_object
        else:
            raise NotFound('This item_tag does not exist.')

    @staticmethod
    def create(item_tag_data: ItemTagInterface) -> ItemTag:

        new_item_tag = ItemTag(
            name = item_tag_data.get('name')
        )

        #add seller firm to db
        db.session.add(new_item_tag)
        db.session.commit()

        return new_item_tag
