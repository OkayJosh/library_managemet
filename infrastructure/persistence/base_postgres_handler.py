"""
Persistence base class.
"""

from core.domain.models import Book, User, BorrowRecord
from shared.brokers.database_broker import DataBaseBroker


class BasePostgresHandler:
    """
    Base class for PostgreSQL database handlers.
    """

    def __init__(self, database):
        """
        Initialize the PostgresHandler with a database and an optional message broker.
        :param database: Database connection or identifier.
        """
        self.database_broker = DataBaseBroker(source=database)

    def add_book(self, book: Book):
        """
        Add a new book to the catalogue.
        :param book:
        :return:
        """
        result = self.database_broker.publish("book_events", {"action": "add", "book": book.__dict__})
        return result

    def remove_book(self, book_uuid):
        """
        Remove a book from the catalogue.
        :param book_uuid:
        :return:
        """
        #NOTE: the two databases cannot maintain the same id, so you need to use a uuid that is not auto generated
        self.database_broker.publish("book_events", {"action": "remove", "book_uuid": book_uuid})
        return True

    def list_available_books(self):
        """
        List all available books.
        :return:
        """
        return self.database_broker.list_available_books()

    def list_unavailable_books(self):
        """
        List all unavailable books.
        :return:
        """
        return self.database_broker.list_unavailable_books()

    def get_book_by_id(self, book_uuid):
        """
        Fetch a single book by its ID.
        :param book_uuid:
        :return:
        """
        return self.database_broker.get_book_by_id(book_uuid)

    def filter_books(self, publisher=None, category=None):
        """
        Filter books by publisher or category.
        :param publisher:
        :param category:
        :return:
        """
        return self.database_broker.filter_books(publisher, category)

    def enroll_user(self, user: User):
        """
        Enroll a user in the library.
        :param user:
        :return:
        """
        self.database_broker.publish("enroll_events", {"action": "add", "user": user.__dict__})
        return True

    def list_users(self):
        """
        List all users enrolled in the library.
        :return:
        """
        return self.database_broker.list_users()

    def get_user_by_id(self, user_uuid):
        """
        Fetch a user by their ID.
        :param user_uuid:
        :return:
        """
        return self.database_broker.get_user_by_id(user_uuid)

    def create_borrow_record(self, borrow_record: BorrowRecord):
        """
        Create a new borrow record.
        :param borrow_record:
        :return:
        """
        self.database_broker.publish("borrow_events", {"action": "add", **borrow_record.__dict__})
        return True

    def get_borrow_record(self, user_uuid, book_uuid):
        """
        Fetch a borrow record for a user and book.
        :param user_uuid:
        :param book_uuid:
        :return:
        """
        return self.database_broker.get_borrow_record(user_uuid, book_uuid)

    def list_borrow_records(self):
        """
        List all borrow records.
        :return:
        """
        return self.database_broker.list_borrow_records()


class PostgresHandlerFrontend(BasePostgresHandler):
    """
    Frontend class for PostgreSQL database handlers.
    """
    def __init__(self, database="default"):
        """
        PostgreSQLFrontend database handler.
        :param database:
        """
        super().__init__(database)


class PostgresHandlerAdmin(BasePostgresHandler):
    """
    Admin class for PostgreSQL database handlers.
    """
    def __init__(self, database="admin"):
        """
        PostgreSQLAdmin database handler.
        :param database:
        """
        super().__init__(database)

