def register_routes(api, app):
    from app.namespaces.user import attach_user
    from app.namespaces.auth import attach_auth
    from app.namespaces.email import attach_email
    from app.namespaces.utils import attach_utils

    # Add routes
    attach_user(api, app)
    attach_auth(api, app)
    attach_email(api, app)
    attach_media(api, app)
