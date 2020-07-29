from .model import DistanceSale
from .schema import distance_sale_dto, distance_sale_sub_dto, distance_sale_admin_dto


BASE_ROUTE = "distance_sale"


def attach_distance_sale(api, app):

    from .controller import ns as distance_sale_ns
    api.add_namespace(distance_sale_ns, path=f"/{BASE_ROUTE}")
