from flask_restx import Model, fields
from ..schema_parent import user_dto, user_dto_admin


seller_dto = user_dto.clone('seller', {})

seller_dto_admin = user_dto_admin.clone('seller_admin', {})
