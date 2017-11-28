"""Model tests."""
from Blog2017.models.user import User
from Blog2017.models.blog_record import BlogRecord
from pyramid_sqlalchemy.testing import DatabaseTestCase
from pyramid import testing
import unittest
import transaction


def dummy_request(dbsession):
    """Return a dummy request object."""
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    """Basic db config for tests. Consider DatabaseTestCase instead."""

    def setUp(self):
        """Initialize sqlite database for testing."""
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('Blog2017.models')
        self.config.include('Blog2017.routes')
        settings = self.config.get_settings()

        from Blog2017.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

    def init_database(self):
        """Use meta file to configure test db."""
        from Blog2017.models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        """Kill test database."""
        from Blog2017.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestModels(BaseTest):
    """Class for testing user and blog_record models."""

    def setUp(self):
        """Add user models to db setup."""
        super(TestModels, self).setUp()
        self.init_database()

        bill = User(name='bill', password='billpass')
        self.session.add(bill)

    def test_bill(self):
        """Test if bill made it through setup."""
        request = dummy_request(self.session)
        response = request.dbsession.query(User).filter(User.name == 'bill').first()
        self.assertEqual(response.id, 1)

    def test_teardown(self):
        """Check for repeats by raising error if more than one bill."""
        request = dummy_request(self.session)
        request.dbsession.query(User).filter(User.name == 'bill').one()

    def test_model_sets_id(self):
        """Check to make sure bill has an id."""
        request = dummy_request(self.session)
        response = request.dbsession.query(User).filter(User.name == 'bill').first()
        self.assertTrue(response.id)


# def test_model_sets_id_automatically(sql_session):
#     obj = User(name='mary', password='marypass')
#     sql_session.add(obj)
#     sql_session.flush()
#     assert obj.id is not None


def test_can_tests_load():
    """Make sure pytest finds this test."""
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
