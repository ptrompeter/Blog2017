"""Model tests."""
from Blog2017.models.user import User
from Blog2017.models.blog_record import BlogRecord
from pyramid_sqlalchemy.testing import DatabaseTestCase
from pyramid import testing
import unittest
import transaction


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('Blog2017.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


# def test_model_sets_id_automatically(sql_session):
#     obj = User(name='bill', password='testpass')
#     sql_session.add(obj)
#     sql_session.flush()
#     assert obj.id is not None


def test_can_tests_load():
    print("I am a test.")
    assert 1 == 1


def test_user_creation(db):
    """Insert a user into test db manually - bad test."""
    query = ("INSERT INTO users "
             "(id, name, password)"
             "VALUES (?, ?, ?)")
    values = (1,
              'bill',
              'testpass')

    db.execute(query, values)


def test_entry_creation(db):
    """Insert an entry into test db manually - bad test."""
    query = ("INSERT INTO entries "
             "(id, title, body)"
             "VALUES (?, ?, ?)")
    values = (1,
              'test',
              'body')

    db.execute(query, values)

