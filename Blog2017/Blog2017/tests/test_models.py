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

        entry = BlogRecord(title='test', body='test')
        self.session.add(entry)

    def test_bill(self):
        """Test if bill made it through setup."""
        request = dummy_request(self.session)
        response = request.dbsession.query(User).filter(User.name == 'bill').first()
        self.assertEqual(response.id, 1)
        self.assertEqual(response.name, "bill")
        self.assertEqual(response.password, "billpass")

    def test_teardown(self):
        """Check for repeats by raising error if more than one bill."""
        request = dummy_request(self.session)
        request.dbsession.query(User).filter(User.name == 'bill').one()

    def test_model_sets_id(self):
        """Check to make sure bill has an id."""
        request = dummy_request(self.session)
        response = request.dbsession.query(User).filter(User.name == 'bill').first()
        self.assertTrue(response.id)

    def test_set_password(self):
        """Check set_password method encrypts pws."""
        mary = User(name='mary', password='marypass')
        mary.set_password(mary.password)
        self.assertNotEqual(mary.password, 'marypass')

    def test_verify_password(self):
        """Check verify_password works."""
        mary = User(name='mary', password='marypass')
        mary.set_password(mary.password)
        self.session.add(mary)
        request = dummy_request(self.session)
        response = request.dbsession.query(User).filter(User.name == 'mary').first()
        check = response.verify_password('marypass')
        self.assertTrue(check)
        self.assertNotEqual(response.password, 'marypass')

    def test_verify_password_2(self):
        """Check auto-updating of unencrypted password."""
        mary = User(name='mary', password='marypass')
        self.session.add(mary)
        request = dummy_request(self.session)
        response = request.dbsession.query(User).filter(User.name == 'mary').first()
        check = response.verify_password('marypass')
        self.assertTrue(check)
        self.assertNotEqual(response.password, 'marypass')
        new_response = request.dbsession.query(User).filter(User.name == 'mary').first()
        self.assertNotEqual(new_response.password, 'marypass')

    def test_get_user(self):
        """Check functionality of get_user classmethod."""
        request = dummy_request(self.session)
        bill = User.get('bill', request)
        self.assertEqual(bill.name, 'bill')

    def test_entry(self):
        """Test if entry was properly created."""
        request = dummy_request(self.session)
        response = request.dbsession.query(BlogRecord).filter(BlogRecord.title == 'test').first()
        self.assertEqual(response.id, 1)
        self.assertEqual(response.title, 'test')
        self.assertEqual(response.body, 'test')
        self.assertTrue(response.created)


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

"""Below: tried to use sql_session fixture from pyramid.sqlalchemy.
Couldn't make it work."""
# def test_model_sets_id_automatically(sql_session):
#     obj = User(name='mary', password='marypass')
#     sql_session.add(obj)
#     sql_session.flush()
#     assert obj.id is not None
