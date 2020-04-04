BASE_ROUTE = "media"

#def attach_auth(api, app, root):
def attach_media(api, app):
    #from profile_image.controller import ns as profile_image_ns
    from .tax_data.controller import ns as tax_data_ns

    #api.add_namespace(profile_image_ns, path=f"/{BASE_ROUTE}")
    api.add_namespace(tax_data_ns, path=f"/{BASE_ROUTE}/tax_data")
