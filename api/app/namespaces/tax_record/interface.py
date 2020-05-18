from mypy_extensions import TypedDict
from typing import List, Dict


class TaxRecordDictInterface(TypedDict, total=True):
    LOCAL_SALES: List[Dict]
    LOCAL_SALE_REVERSE_CHARGES: List[Dict]
    DISTANCE_SALES: List[Dict]
    NON_TAXABLE_DISTANCE_SALES: List[Dict]
    INTRA_COMMUNITY_SALES: List[Dict]
    EXPORTS: List[Dict]
    DOMESTIC_ACQUISITIONS: List[Dict]
    INTRA_COMMUNITY_ACQUISITIONS: List[Dict]
