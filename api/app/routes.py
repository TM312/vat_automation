#def register_routes(api, app, root):
def register_routes(api, app):
    from app.user import attach_user
    from app.auth import attach_auth
    from app.email import attach_email

    # # Add routes
    # attach_user(api, app, root)
    # attach_auth(api, app, root)
    # attach_email(api, app, root)

    # Add routes
    attach_user(api, app)
    attach_auth(api, app)
    attach_email(api, app)
