"""
Application services
"""
import uuid

from rest_framework.exceptions import ValidationError

from core.domain.models import Book
from core.domain.services import LibraryService
from library.serializers import BookSerializer
from library.validators import BorrowSerializer
from infrastructure.persistence.base_postgres_handler import PostgresHandlerFrontend, PostgresHandlerAdmin

class BookService:
    """
    Service layer for book-related use cases.
    """
    active_db = {'default': PostgresHandlerFrontend, 'admin': PostgresHandlerAdmin}

    def __init__(self, default_db='default'):
        """
        Initialization
        """
        self.default_db = self.active_db[default_db]()
        self.library_service = LibraryService()

    def list_available_books(self):
        """
        List all available books from the frontend database.
        :return: Serialized data of available books.
        """
        books = self.default_db.list_available_books()
        serializer = BookSerializer(books, many=True)
        return serializer.data

    def borrow_book(self, user_uuid: uuid, book_uuid: uuid, days: int):
        """
        Borrow a book for a specific user.
        :param user_uuid:
        :param book_uuid:
        :param days:
        :return: Serialized borrow record.
        """
        serializer = BorrowSerializer(
            default_db=self.default_db,
            data={"user_uuid": user_uuid, "book_uuid": book_uuid, "days": days}
        )
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        validated_data = serializer.validated_data
        borrow_record = self.default_db.create_borrow_record(**validated_data)
        return borrow_record  # If needed, serialize this record as well.

    def add_new_book(self, book: Book):
        """
        Add a new book to the catalogue in both the frontend and admin databases.
        :param book:
        :return: Serialized new book.
        """
        self.default_db.add_book(book)
        return "book was successfully added."

    def remove_book(self, book_uuid: uuid):
        """
        Remove book from catalogue in both the frontend and admin databases.
        :param book_uuid:
        :return: Serialized removed book.
        """
        removed_book = self.default_db.remove_book(book_uuid)
        serializer = BookSerializer(removed_book)
        return serializer.data

    def list_borrowed_books(self):
        """
        List all books that have been borrowed from the frontend database.
        :return: Serialized data of borrowed books.
        """
        borrowed_books = self.default_db.list_borrow_records()
        serializer = BookSerializer(borrowed_books, many=True)
        return serializer.data

    def get_book_availability(self, book_uuid: uuid) -> bool:
        """
        Check if a book is available for borrowing.
        :param book_uuid:
        :return bool:
        """
        book = self.default_db.get_book_by_id(book_uuid)
        return self.library_service.is_book_available(book)

    def filter_book(self, publisher: str, category: str) -> bool:
        """
        Check if a book is available for borrowing based on publisher and category.
        :param publisher:
        :param category:
        :return bool:
        """
        book = self.default_db.filter_book(publisher, category)
        return self.library_service.is_book_available(book)

    def get_book_by_id(self, book_uuid: uuid):
        """
        Fetch a single book by its UUID.
        :param book_uuid:
        :return: Serialized book data.
        """
        book = self.default_db.get_book_by_id(book_uuid)
        serializer = BookSerializer(book)
        return serializer.data

    def list_unavailable_books(self):
        """
        List all books that are not available for borrowing.
        :return: Serialized data of unavailable books.
        """
        unavailable_books = self.default_db.list_unavailable_books()
        serializer = BookSerializer(unavailable_books, many=True)
        return serializer.data
