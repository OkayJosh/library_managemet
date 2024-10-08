"""
Data classes for the Base Entities
"""
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class User:
    """
    Domain model for a library user.
    """
    email: str
    firstname: str
    lastname: str
    user_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """
        Post-initialization method to validate user creation logic.
        """
        if not self.email or not self.firstname or not self.lastname:
            raise ValueError("User must have a valid email, firstname, and lastname")

@dataclass
class Book:
    """
    Domain model for a book in the library.
    """
    title: str
    publisher: str
    category: str
    availability_status: bool = True
    book_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

    def lend_out(self):
        """
        Mark the book as lent out.
        """
        if not self.availability_status:
            raise ValueError("Book is already lent out.")
        self.availability_status = False

    def return_book(self):
        """
        Mark the book as returned.
        """
        if self.availability_status:
            raise ValueError("Book is already available.")
        self.availability_status = True

@dataclass
class BorrowRecord:
    """
    Domain model for a record of a book borrowed by a user.
    """
    # user: User
    # book: Book
    borrow_date: datetime
    due_date: datetime
    record_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    book_uuid: uuid.UUID = None
    user_uuid: uuid.UUID = None

    def is_overdue(self) -> bool:
        """
        Check if the borrowed book is overdue.
        """
        return date.today() > self.due_date
