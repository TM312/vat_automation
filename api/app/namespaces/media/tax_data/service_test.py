# from app.test.fixtures import app, db # noqa
# from typing import List
# from .model import User
# from .service import UserService  # noqa
# from .interface import UserInterface


# def test_get_all(db):  # noqa
#     yin: User = User(email='yin@email.com', role="admin", password="1234")
#     yang: User = User(email='yang@email.com', password="4321")
#     db.session.add(yin)
#     db.session.add(yang)
#     db.session.commit()

#     results: List[User] = UserService.get_all()

#     assert len(results) == 2
#     assert yin in results and yang in results


# def test_update(db):  # noqa
#     yin: User = User(email='yin@email.com', password="1234")

#     db.session.add(yin)
#     db.session.commit()
#     data_changes: UserInterface = dict(email='yin2@email.com', role="admin")

#     UserService.update(yin, data_changes)

#     result: User = User.query.get(yin.id)
#     assert result.email == "yin2@email.com"
#     assert result.role == "admin"


# def test_delete_by_id(db):  # noqa
#     yin: User = User(email='yin@email.com', role="admin", password="1234")
#     yang: User = User(email='yang@email.com', password="4321")
#     db.session.add(yin)
#     db.session.add(yang)
#     db.session.commit()


#     UserService.delete_by_id(yin.public_id)
#     db.session.commit()

#     results: List[User] = User.query.all()

#     assert len(results) == 1
#     assert yin not in results and yang in results


# def test_create(db):  # noqa

#     yin3: UserInterface = dict(
#         email='yin3@email.com', password="1234")
#     UserService.create_user(yin3)
#     results: List[User] = User.query.all()

#     assert len(results) == 1
