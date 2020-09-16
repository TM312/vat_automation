from typing import List
from app.extensions import db


from . import Channel
from .interface import ChannelInterface

class ChannelService:
    @staticmethod
    def get_all() -> List[Channel]:
        channels = Channel.query.all()
        return channels

    @staticmethod
    def get_by_code(code: str) -> Channel:
        return Channel.query.filter_by(code = code).first()


    @staticmethod
    def update(code: str, data_changes: ChannelInterface) -> Channel:
        channel = ChannelService.get_by_code(code)
        if isinstance(channel, Channel):
            channel.update(data_changes)
            db.session.commit()
            return channel

    @staticmethod
    def delete_by_code(code: str):
        channel = ChannelService.get_by_code(code)
        if isinstance(channel, Channel):
            db.session.delete(channel)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Channel (code: {}) has been successfully deleted.'.format(code)
            }
            return response_object
        else:
            raise NotFound('This channel does not exist.')

    @staticmethod
    def create(channel_data: ChannelInterface) -> Channel:

        new_channel = Channel(
            code = channel_data.get('code'),
            name = channel_data.get('name'),
            platform_code = channel_data.get('platform_code'),
            description = channel_data.get('description')
        )

        #add seller firm to db
        db.session.add(new_channel)
        db.session.commit()

        return new_channel
