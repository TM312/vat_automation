from typing import List
from app.extensions import db


from . import UserTag
from .interface import UserTagInterface

class UserTagService:
    @staticmethod
    def get_all() -> List[UserTag]:
        user_tags = UserTag.query.all()
        return user_tags

    @staticmethod
    def get_by_id(id: str) -> UserTag:
        return UserTag.query.filter_by(id=id).first()


    @staticmethod
    def delete_by_id(id: str):
        user_tag = UserTag.query.filter(UserTag.id == id).first()
        if user_tag:
            db.session.delete(user_tag)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'UserTag (name: {}) has been successfully deleted.'.format(user_tag.name)
            }
            return response_object
        else:
            raise NotFound('This user_tag does not exist.')

    @staticmethod
    def create(user_tag_data: UserTagInterface) -> UserTag:

        new_user_tag = UserTag(
            name = user_tag_data.get('name')
        )

        #add seller firm to db
        db.session.add(new_user_tag)
        db.session.commit()

        return new_user_tag
