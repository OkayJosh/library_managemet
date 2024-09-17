"""
Broker
"""
import logging

from core.domain.models import BorrowRecord
from infrastructure.repositories.book_repository import BookRepository
from infrastructure.repositories.borrow_repository import BorrowRepository
from infrastructure.repositories.user_repository import UserRepository
from library_managemet.celery import app

LOG = logging.getLogger(__name__)

class DataBaseBroker:
    """
     DataBase broker to handle publishing and subscribing to events.
    """

    def __init__(self, source):
        """
        Initialize the broker.
        :param source:
        """
        self.source = source
        self.book_repository = BookRepository(databases=[source])
        self.user_repository = UserRepository(databases=[source])
        self.borrow_repository = BorrowRepository(databases=[source])

    def publish(self, topic, event):
        """
        Publish an event to a specific topic.
        :param topic: Event topic.
        :param event: Event payload.
        """
        app.send_task('library.tasks.process_event', args=[topic, event])
        LOG.info(f"application.tasks.process_event with: {topic}, {event}")

    def list_available_books(self):
        """
        List all available books.
        :return:
        """
        return self.book_repository.list_available_books()

    def list_unavailable_books(self):
        """
        List all unavailable books.
        :return:
        """
        return self.book_repository.list_unavailable_books()

    def get_book_by_id(self, book_uuid):
        """
        Fetch a single book by its ID.
        :param book_uuid:
        :return:
        """
        return self.book_repository.get_book_by_id(book_uuid)

    def filter_books(self, publisher=None, category=None):
        """
        Filter books by publisher or category.
        :param publisher:
        :param category:
        :return:
        """
        return self.book_repository.filter_books(publisher, category)

    def list_users(self):
        """
        List all users enrolled in the library.
        :return:
        """
        return self.user_repository.list_users()

    def get_user_by_id(self, user_uuid):
        """
        Fetch a user by their ID.
        :param user_uuid:
        :return:
        """
        return self.user_repository.get_user_by_id(user_uuid)

    def create_borrow_record(self, borrow_record: BorrowRecord):
        """
        Create a new borrow record.
        :param borrow_record:
        :return:
        """
        borrow =  self.borrow_repository.create_borrow_record(borrow_record)
        LOG.info(f"Book added to {self.source} database: {borrow_record}")
        return borrow

    def get_borrow_record(self, user_uuid, book_uuid):
        """
        Fetch a borrow record for a user and book.
        :param user_uuid:
        :param book_uuid:
        :return:
        """
        return self.borrow_repository.get_borrow_record(user_uuid, book_uuid)

    def list_borrow_records(self):
        """
        Fetch all borrow_record.
        :return:
        """
        return self.borrow_repository.list_borrow_records()
