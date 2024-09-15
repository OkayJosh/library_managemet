"""
Library Models
"""

from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django_extensions.db.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    """
    Model for a library user.
    """
    user_uuid = models.UUIDField(editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    def clean(self):
        """
        Ensure all fields are valid.
        """
        if not self.email or not self.firstname or not self.lastname:
            raise ValidationError("User must have a valid email, firstname, and lastname")

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.email})"


class Book(TimeStampedModel):
    """
    Model for a book in the library.
    """
    book_uuid = models.UUIDField(editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    availability_status = models.BooleanField(default=True)

    def lend_out(self):
        """
        Mark the book as lent out.
        """
        if not self.availability_status:
            raise ValidationError("Book is already lent out.")
        self.availability_status = False
        self.save()

    def return_book(self):
        """
        Mark the book as returned.
        """
        if self.availability_status:
            raise ValidationError("Book is already available.")
        self.availability_status = True
        self.save()

    def __str__(self):
        return f"{self.title} - {self.publisher} ({'Available' if self.availability_status else 'Lent out'})"


class BorrowRecord(TimeStampedModel):
    """
    Model for a record of a book borrowed by a user.
    """
    record_uuid = models.UUIDField(editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()
    book_uuid = None
    user_uuid = None

    def __init__(self, *args, **kwargs):
        self.user_uuid = kwargs.pop('user_uuid', None)
        self.book_uuid = kwargs.pop('book_uuid', None)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.user_uuid:
            self.user = User.objects.get(user_uuid=self.user_uuid)

        if self.book_uuid:
            self.book = Book.objects.get(book_uuid=self.book_uuid)

        # Call the original save method
        super().save(*args, **kwargs)

    def is_overdue(self) -> bool:
        """
        Check if the borrowed book is overdue.
        """
        return date.today() > self.due_date

    def __str__(self):
        return f"BorrowRecord: {self.user} borrowed {self.book} on {self.borrow_date}, due {self.due_date}"
