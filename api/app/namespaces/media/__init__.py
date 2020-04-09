BASE_ROUTE = "media"

# def attach_auth(api, app, root):


def attach_media(api, app):
    #from profile_image.controller import ns as profile_image_ns
    from .tax_record.controller import ns as tax_record_ns

    #api.add_namespace(profile_image_ns, path=f"/{BASE_ROUTE}")
    api.add_namespace(tax_record_ns, path=f"/{BASE_ROUTE}/tax_record")
