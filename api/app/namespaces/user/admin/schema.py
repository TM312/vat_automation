from flask_restx import Model, fields
from ..schema_parent import user_dto


admin_dto = user_dto.inherit('admin', {})
