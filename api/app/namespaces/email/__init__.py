
BASE_ROUTE = "email"

#def attach_auth(api, app, root):
def attach_email(api, app):
    from .controller import ns as email_ns

    #api.add_namespace(email_ns, path=f"/{root}/{BASE_ROUTE}")
    api.add_namespace(email_ns, path=f"/{BASE_ROUTE}")
