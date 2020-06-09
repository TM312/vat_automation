from app.namespaces.channel.model import Channel
from app.namespaces.platform.amazon.model import Amazon

platforms = [
    {
        'code': 'AMZ',
        'name': 'Amazon'
    }
]


class PlatformSeedService:
    @staticmethod
    def append_channels_to_platform():
        mfn = Channel.query.filter_by(code='MFN').first()
        afn = Channel.query.filter_by(code='AFN').first()
        amazon = Amazon.query.filter_by(code='AMZ').first()
        if not isinstance(afn, Channel) or not isinstance(mfn, Channel) or not isinstance(amazon, Amazon):
            raise

        else:
            amazon.channels.append(mfn)
            amazon.channels.append(afn)
