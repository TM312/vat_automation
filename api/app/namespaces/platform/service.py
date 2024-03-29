from typing import List
from app.extensions import db


from . import Platform
from .interface import PlatformInterface


class PlatformService:
    @staticmethod
    def get_all() -> List[Platform]:
        return Platform.query.all()

    @staticmethod
    def get_by_code(platform_code: int) -> Platform:
        return Platform.query.filter_by(code=platform_code).first()

    @staticmethod
    def update(platform_code: int, data_changes: PlatformInterface) -> Platform:
        platform = PlatformService.get_by_code(platform_code)
        if isinstance(platform, Platform):
            platform.update(data_changes)
            try:
                db.session.commit()
            except:
                db.session.rollback()
        return platform

    @staticmethod
    def delete_by_code(platform_code: str):
        platform = Platform.query.filter_by(code = platform_code).first()
        if platform:
            db.session.delete(platform)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Platform (code: {}) has been successfully deleted.'.format(platform_code)
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
