"""
Validator for application
"""
from datetime import timedelta

from django.utils.timezone import now
from rest_framework import serializers

class BorrowSerializer(serializers.Serializer):
    """
    Serializer for borrow-related input.
    """

    days = serializers.IntegerField()
    book_uuid = serializers.UUIDField()
    user_uuid = serializers.UUIDField()

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer with the optional default_db parameter.
        :param args:
        :param kwargs:
        """
        self.default_db = kwargs.pop('default_db', None)
        super().__init__(*args, **kwargs)

    def validate_days(self, value):
        """
        Validate that the borrow period is within allowed limits.
        :param value: Number of days.
        :return: Validated number of days.
        """
        MIN_BORROW_DAYS = 1
        MAX_BORROW_DAYS = 30
        if value < MIN_BORROW_DAYS:
            raise serializers.ValidationError(f"Borrow period must be at least {MIN_BORROW_DAYS} day(s).")
        if value > MAX_BORROW_DAYS:
            raise serializers.ValidationError(f"Borrow period cannot exceed {MAX_BORROW_DAYS} days.")
        return value

    def validate(self, data):
        """
        Validate that the user and book exist and that the book is available.
        :param data: Input data.
        :return: Validated data.
        """
        user_uuid = data.get('user_uuid')
        book_uuid = data.get('book_uuid')

        # Fetch user and book information from the admin database
        user = self.default_db.get_user_by_id(user_uuid=user_uuid)

        if not user:
            raise serializers.ValidationError("User not found.")


        book = self.default_db.get_book_by_id(book_uuid=book_uuid)

        if not book:
            raise serializers.ValidationError("User not found.")

        if not book.availability_status:
            raise serializers.ValidationError(f"Book '{book.title}' is not available for borrowing.")

        # Calculate borrow_date and due_date based on the input days
        borrow_date = now()
        due_date = borrow_date + timedelta(days=data.get('days'))

        # Remove 'days' from the validated data and add 'borrow_date' and 'due_date'
        data.pop('days')
        data['borrow_date'] = borrow_date
        data['due_date'] = due_date

        return data


class UserSerializer(serializers.Serializer):
    """
    Serializer for user-related input.
    """
    user_uuid = serializers.UUIDField()
    email = serializers.EmailField()
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)

    def validate_firstname(self, value):
        """
        Validate that the firstname is non-empty.
        :param value: Firstname.
        :return: Validated firstname.
        """
        if not value:
            raise serializers.ValidationError("Firstname must not be empty.")
        return value

    def validate_lastname(self, value):
        """
        Validate that the lastname is non-empty.
        :param value: Lastname.
        :return: Validated lastname.
        """
        if not value:
            raise serializers.ValidationError("Lastname must not be empty.")
        return value
