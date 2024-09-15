"""
User Service
"""
import uuid

from rest_framework.exceptions import ValidationError

from core.domain.models import User
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

    def enroll_user(self, user: User):
        """
        Enroll a new user in the library system.
        :param user:
        :return: Serialized user data.
        """
        # Validate input data
        serializer = UserSerializer(
            data=user.__dict__
        )
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        validated_data = serializer.validated_data
        self.default_db.enroll_user(User(**validated_data))
        return {"message": "User Successfully Enrolled"}

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
