from mypy_extensions import TypedDict


class TokenInterface(TypedDict, total=False):
    token_lifespan: int
    auth_token: str
    sub: str
