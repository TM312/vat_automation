from mypy_extensions import TypedDict

class AccountingInterface(TypedDict, total=False):
    company_name: str
    logo_image_name: str
