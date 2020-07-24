from .model import Bundle
from .schema import bundle_dto, bundle_admin_dto, bundle_sub_dto

BASE_ROUTE = "bundle"


def attach_bundle(api, app):
    from .controller import ns as bundle_ns
    api.add_namespace(bundle_ns, path=f"/{BASE_ROUTE}")
