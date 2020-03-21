BASE_ROUTE = "auth"


def attach_auth(api, app, root):
    from .controller import ns as auth_ns

    api.add_namespace(auth_ns, path=f"/{root}/{BASE_ROUTE}")
