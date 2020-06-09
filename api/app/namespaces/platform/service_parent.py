from typing import List
from app.extensions import db


from . import Platform
from .interface_parent import PlatformInterface


class PlatformService:
    @staticmethod
    def get_all() -> List[Platform]:
        platforms = Platform.query.all()
        return platforms

    @staticmethod
    def get_by_id(platform_id: int) -> Platform:
        return Platform.query.filter(Platform.code == code).first()

    @staticmethod
    def update(platform_id: int, data_changes: PlatformInterface) -> Platform:
        platform = PlatformService.get_by_id(codplatform_ide)
        platform.update(data_changes)
        db.session.commit()
        return platform

    @staticmethod
    def delete_by_id(platform_id: str):
        platform = Platform.query.filter(Platform.id == platform_id).first()
        if platform:
            db.session.delete(platform)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Platform (code: {}) has been successfully deleted.'.format(platform_id)
            }
            return response_object
        else:
            raise NotFound('This platform does not exist.')

    @staticmethod
    def create(platform_data: PlatformInterface) -> Platform:
        new_platform = Platform(
            code=platform_data.get('code'),
            name=platform_data.get('name')
        )

        db.session.add(new_platform)
        db.session.commit()

        return new_platform
