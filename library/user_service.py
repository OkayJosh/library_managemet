"""
User Service
"""
import uuid

from rest_framework.exceptions import ValidationError

from library.serializers import BorrowRecordSerializer
from library.validators import UserSerializer
from infrastructure.persistence.base_postgres_handler import PostgresHandlerFrontend, PostgresHandlerAdmin

class UserService:
    """
    Service layer for user-related use cases.
    """
    active_db = {'default': PostgresHandlerFrontend, 'admin': PostgresHandlerAdmin}

    def __init__(self, default_db='default'):
        """
        Initialization
        """
        self.default_db = self.active_db[default_db]()

    def enroll_user(self, email: str, firstname: str, lastname: str):
        """
        Enroll a new user in the library system.
        :param email:
        :param firstname:
        :param lastname:
        :return: Serialized user data.
        """
        # Validate input data
        serializer = UserSerializer(
            data={"email": email, "firstname": firstname, "lastname": lastname}
        )
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        validated_data = serializer.validated_data
        new_user = self.default_db.enroll_user(**validated_data)
        return UserSerializer(new_user).data

    def list_users(self):
        """
        List all enrolled users from the admin database.
        :return: Serialized data of all users.
        """
        users = self.default_db.list_users()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    def get_user_borrow_records(self, user_uuid: uuid):
        """
        Get the books borrowed by a specific user from the admin database.
        :param user_uuid:
        :return: Serialized borrow records.
        """
        borrow_records = self.default_db.get_borrow_record(user_uuid=user_uuid, book_uuid=None)
        serializer = BorrowRecordSerializer(borrow_records, many=True)
        return serializer.data  # Adjust if serialization is required
