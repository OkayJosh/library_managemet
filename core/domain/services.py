"""
Core service of the Library Management
"""
import uuid
from datetime import timedelta, date
from core.domain.models import Book, User, BorrowRecord

class LibraryService:
    """
    Service for managing library operations.
    """

    def borrow_book(self, user: User, book: Book, days: int) -> BorrowRecord:
        """
        Borrow a book for a specified number of days.
        :param user:
        :param book:
        :param days:
        :return BorrowRecord:
        """
        if not book.availability_status:
            raise ValueError("Book is currently unavailable for borrowing.")

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=days)

        # Create and return the borrow record
        book.lend_out()
        return BorrowRecord(
            record_uuid=uuid.uuid4(),  # This will be replaced by a persistent record ID from the repository
            user=user,
            book=book,
            borrow_date=borrow_date,
            due_date=due_date
        )

    def return_book(self, borrow_record: BorrowRecord):
        """
        Return a borrowed book.
        :param borrow_record:
        :return:
        """
        borrow_record.book.return_book()

    def is_book_available(self, book: Book) -> bool:
        """
        Check if a book is available for borrowing.
        :param book:
        :return bool:
        """
        return book.availability_status
