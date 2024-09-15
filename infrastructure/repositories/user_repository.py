"""
User Repository
"""
from infrastructure.repositories.base_repository import BaseRepository
from library.models import User


class UserRepository(BaseRepository):
    """
    Repository for handling User-related database operations.
    """

    def __init__(self, databases=None):
        super().__init__(model_class=User, databases=databases)

    def enroll_user(self, user: User):
        """
        Enroll a user in all specified databases.
        :param user: User instance to enroll.
        :return: List of results for each database operation.
        """
        return self.add(user)

    def get_user_by_id(self, user_uuid):
        """
        Fetch a user by their ID from the first available database.
        :param user_uuid: User ID.
        :return: User instance or None if not found.
        """
        return self.get(user_uuid=user_uuid)

    def list_users(self):
        """
        List all users from all specified databases.
        :return: List of all users from all databases.
        """
        return self.list()