BASE_ROUTE = "email"

def attach_email(api, app, root):
    from .controller import ns as email_ns

    api.add_namespace(email_ns, path=f"/{root}/{BASE_ROUTE}")
