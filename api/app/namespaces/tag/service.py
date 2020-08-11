from typing import List
from app.extensions import db


from . import Tag
from .interface import TagInterface

class TagService:
    @staticmethod
    def get_all() -> List[Tag]:
        tags = Tag.query.all()
        return tags

    @staticmethod
    def get_by_code(code: str) -> Tag:
        return Tag.query.filter_by(code=code).first()


    @staticmethod
    def delete_by_code(code: str):
        tag = Tag.query.filter(Tag.code == code).first()
        if tag:
            db.session.delete(tag)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Tag (code: {}) has been successfully deleted.'.format(code)
            }
            return response_object
        else:
            raise NotFound('This tag does not exist.')

    @staticmethod
    def create(tag_data: TagInterface) -> Tag:

        new_tag = Tag(
            code = tag_data.get('code')
        )

        #add seller firm to db
        db.session.add(new_tag)
        db.session.commit()

        return new_tag
