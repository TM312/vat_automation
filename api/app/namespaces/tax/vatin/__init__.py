import re

import logging


logger = logging.getLogger("vatin")


def dk_format(v):
    return "{} {} {} {}".format(v[:4], v[4:6], v[6:8], v[8:10])


def gb_format(v):
    if len(v) == 11:
        return "{} {} {}".format(v[:5], v[5:9], v[9:11])
    if len(v) == 14:
        return "{} {}".format(gb_format(v[:11]), v[11:14])
    return v


def fr_format(v):
    return "{} {}".format(v[:4], v[4:])




VIES_WSDL_URL = (
    "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"  # NoQA
)
VATIN_MAX_LENGTH = 14


VIES_OPTIONS = {
    "AT": ("Austria", re.compile(r"^ATU\d{8}$")),
    "BE": ("Belgium", re.compile(r"^BE0?\d{9}$")),
    "BG": ("Bulgaria", re.compile(r"^BG\d{9,10}$")),
    "HR": ("Croatia", re.compile(r"^HR\d{11}$")),
    "CY": ("Cyprus", re.compile(r"^CY\d{8}[A-Z]$")),
    "CZ": ("Czech Republic", re.compile(r"^CZ\d{8,10}$")),
    "DE": ("Germany", re.compile(r"^DE\d{9}$")),
    "DK": ("Denmark", re.compile(r"^DK\d{8}$"), dk_format),
    "EE": ("Estonia", re.compile(r"^EE\d{9}$")),
    "EL": ("Greece", re.compile(r"^EL\d{9}$")),
    "ES": ("Spain", re.compile(r"^ES[A-Z0-9]\d{7}[A-Z0-9]$")),
    "FI": ("Finland", re.compile(r"^FI\d{8}$")),
    "FR": ("France", re.compile(r"^FR[A-HJ-NP-Z0-9][A-HJ-NP-Z0-9]\d{9}$"), fr_format),
    "GB": (
        "United Kingdom",
        re.compile(r"^(GB(GD|HA)\d{3}|GB\d{9}|GB\d{12})$"),
        gb_format,
    ),
    "HU": ("Hungary", re.compile(r"^HU\d{8}$")),
    "IE": ("Ireland", re.compile(r"^IE\d[A-Z0-9\+\*]\d{5}[A-Z]{1,2}$")),
    "IT": ("Italy", re.compile(r"^IT\d{11}$")),
    "LT": ("Lithuania", re.compile(r"^LT(\d{9}|\d{12})$")),
    "LU": ("Luxembourg", re.compile(r"^LU\d{8}$")),
    "LV": ("Latvia", re.compile(r"^LV\d{11}$")),
    "MT": ("Malta", re.compile(r"^MT\d{8}$")),
    "NL": ("The Netherlands", re.compile(r"^NL\d{9}B\d{2}$")),
    "PL": ("Poland", re.compile(r"^PL\d{10}$")),
    "PT": ("Portugal", re.compile(r"^PT\d{9}$")),
    "RO": ("Romania", re.compile(r"^RO\d{2,10}$")),
    "SE": ("Sweden", re.compile(r"^SE\d{10}01$")),
    "SI": ("Slovenia", re.compile(r"^SI\d{8}$")),
    "SK": ("Slovakia", re.compile(r"^SK\d{10}$")),
}

VIES_COUNTRY_CHOICES = sorted(
    (("", "--"),) + tuple((key, key) for key, value in VIES_OPTIONS.items())
)

MEMBER_COUNTRY_CODES = VIES_OPTIONS.keys()
