from mypy_extensions import TypedDict
from datetime import date, datetime


class CategoryInterface(TypedDict, total=False):
    created_by: int
    level: int
    business_id: int
    parent_id: int
