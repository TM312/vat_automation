from typing import List
from .model import Channel
from app.extensions import db

class ChannelService:
    @staticmethod
    def get_all() -> List[Channel]:
        channels = Channel.query.all()
        return channels

    @staticmethod
    def get_by_code(code: str) -> Channel:
        channel = Channel.query.filter(Channel.code == code).first()
        if channel:
            return channel


    @staticmethod
    def update(code: str, data_changes: dict) -> Channel:
        channel = ChannelService.get_by_id(code)
        channel.update(data_changes)
        db.session.commit()
        return channel

    @staticmethod
    def delete_by_id(code: str):
        channel = Channel.query.filter(Channel.code == code).first()
        if channel:
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
    def create_channel(channel_data) -> Channel:

        new_channel = Channel(
            code = channel_data.get('code')
            name = channel_data.get('name')
            platform_code = channel_data.get('platform_code')
            description = channel_data.get('description')
        )

        #add seller firm to db
        db.session.add(new_channel)
        db.session.commit()

        return new_channel
