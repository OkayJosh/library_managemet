"""
Data classes for the Base Entities
"""
import uuid
from dataclasses import dataclass
from datetime import date
from typing import Union


@dataclass
class User:
    """
    Domain model for a library user.
    """
    user_id: Union[int, None]
    user_uuid: uuid
    email: str
    firstname: str
    lastname: str

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
    book_id: Union[int, None]
    book_uuid: uuid
    title: str
    publisher: str
    category: str
    availability_status: bool = True

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
    record_id: Union[int, None]
    record_uuid: uuid
    user: User
    book: Book
    borrow_date: date
    due_date: date

    def is_overdue(self) -> bool:
        """
        Check if the borrowed book is overdue.
        """
        return date.today() > self.due_date
