from ..schema_parent import business_dto
from flask_restx import Model, fields

accounting_firm_dto = business_dto.clone('accounting_firm', {})
