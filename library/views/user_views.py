from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID

from core.domain.models import User
from library.user_service import UserService


class UserListView(APIView):
    """
    API view to list all users.
    """
    def get(self, request):
        user_service = UserService()
        users = user_service.list_users()
        return Response(users, status=status.HTTP_200_OK)


class EnrollUserView(APIView):
    """
    API view to enroll a new user.
    """
    def post(self, request):
        email = request.data.get("email")
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")

        user_service = UserService()
        try:
            new_user = user_service.enroll_user(User(email, firstname, lastname))
            return Response(new_user, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class UserBorrowRecordsView(APIView):
    """
    API view to get a user's borrowed books.
    """
    def get(self, request, user_uuid):
        user_uuid = user_uuid if isinstance(user_uuid, UUID) else UUID(user_uuid)
        user_service = UserService()
        borrow_records = user_service.get_user_borrow_records(user_uuid)
        return Response(borrow_records, status=status.HTTP_200_OK)

class UserBorrowedBooksView(APIView):
    """
    API view to list users and the books they have borrowed.
    """
    def get(self, request, user_uuid):
        user_uuid = user_uuid if isinstance(user_uuid, UUID) else UUID(user_uuid)
        user_service = UserService()
        borrowed_books = user_service.get_user_borrow_records(user_uuid)
        return Response(borrowed_books, status=status.HTTP_200_OK)
