from mypy_extensions import TypedDict
from datetime import date
from typing import List


class TaxCodeInterface(TypedDict, total=False):
    code: str
    description: str
    channels: List['app.namespaces.channel.Channel']
    items: List['app.namespaces.item.Item']
    vats: List['app.namespaces.tax.vat.Vat']
