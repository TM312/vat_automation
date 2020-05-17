from .decorators.asyncd import asyncd
from .decorators.auth import login_required, accepted_u_types, confirmation_required, employer_required

BASE_ROUTE = "utils"


def attach_utils(api, app):
    from .controller import ns as utils_ns

    api.add_namespace(utils_ns, path=f"/{BASE_ROUTE}")
