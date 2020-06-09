from flask_restx import Model, fields
from ..schema_parent import platform_dto

amazon_dto = platform_dto.clone('amazon', {})
