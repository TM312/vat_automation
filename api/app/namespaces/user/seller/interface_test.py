from pytest import fixture
from .model import User
from .interface import UserInterface


@fixture
def interface() -> UserInterface:
    return UserInterface(email='testuser@testemail.com', password='testpassword')


def test_UserInterface_create(interface: UserInterface):
    assert interface

#currently fails : "RuntimeError: Working outside of application context."
# def test_UserInterface_works(interface: UserInterface):
#     user = User(**interface)
#     assert user
