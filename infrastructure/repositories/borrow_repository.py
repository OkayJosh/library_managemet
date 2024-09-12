"""
Borrow Repository
"""
from infrastructure.repositories.base_repository import BaseRepository
from library.models import BorrowRecord


class BorrowRepository(BaseRepository):
    """
    Repository for handling BorrowRecord-related database operations.
    """

    def __init__(self, databases=None):
        super().__init__(model_class=BorrowRecord, databases=databases)

    def create_borrow_record(self, borrow_record: BorrowRecord):
        """
        Create a new borrow record in all specified databases.
        :param borrow_record: BorrowRecord instance to create.
        :return: List of results for each database operation.
        """
        return self.add(borrow_record)

    def get_borrow_record(self, user_uuid, book_uuid):
        """
        Fetch a borrow record for a user and book from the first available database.
        :param user_uuid: User ID.
        :param book_uuid: Book ID.
        :return: BorrowRecord instance or None if not found.
        """
        return self.get(user_uuid=user_uuid, book_uuid=book_uuid)

    def list_borrow_records(self):
        """
        List all borrow records from all specified databases.
        :return: List of all borrow records from all databases.
        """
        return self.list()
