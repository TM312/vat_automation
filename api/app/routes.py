def register_routes(api, app):
    from app.namespaces.account import attach_account
    from app.namespaces.auth import attach_auth
    from app.namespaces.bundle import attach_bundle
    from app.namespaces.business import attach_business
    from app.namespaces.channel import attach_channel
    from app.namespaces.country import attach_country
    from app.namespaces.currency import attach_currency
    from app.namespaces.distance_sale import attach_distance_sale
    from app.namespaces.email import attach_email
    from app.namespaces.exchange_rate import attach_exchange_rate
    from app.namespaces.item import attach_item
    from app.namespaces.platform import attach_platform
    from app.namespaces.tax import attach_tax
    from app.namespaces.tax_record import attach_tax_record
    from app.namespaces.transaction import attach_transaction
    from app.namespaces.transaction_input import attach_transaction_input
    from app.namespaces.user import attach_user
    from app.namespaces.utils import attach_utils



    # Add routes
    attach_account(api, app)
    attach_auth(api, app)
    attach_bundle(api, app)
    attach_business(api, app)
    attach_channel(api, app)
    attach_country(api, app)
    attach_currency(api, app)
    attach_distance_sale(api, app)
    attach_email(api, app)
    attach_exchange_rate(api, app)
    attach_item(api, app)
    attach_platform(api, app)
    attach_tax(api, app)
    attach_tax_record(api, app)
    attach_transaction(api, app)
    attach_transaction_input(api, app)
    attach_user(api, app)
    attach_utils(api, app)
