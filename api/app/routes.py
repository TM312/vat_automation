def register_routes(api, app, root):
    from app.user import attach_user
    from app.auth import attach_auth
    from app.email import attach_email

    # Add routes
    attach_user(api, app, root)
    attach_auth(api, app, root)
    attach_email(api, app, root)
