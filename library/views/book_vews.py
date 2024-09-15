from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID

from library.book_service import BookService
from core.domain.models import Book as BookRecord
from library.models import Book


class BookListView(APIView):
    """
    API view to list all available books.
    """
    def get(self, request):
        book_service = BookService()
        books = book_service.list_available_books()
        return Response(books, status=status.HTTP_200_OK)


class BorrowBookView(APIView):
    """
    API view to borrow a book.
    """
    def post(self, request):
        user_uuid = UUID(request.data.get("user_uuid"))
        book_uuid = UUID(request.data.get("book_uuid"))
        days = request.data.get("days")

        book_service = BookService()
        try:
            borrow_record = book_service.borrow_book(user_uuid, book_uuid, days)
            return Response(borrow_record, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class AddBookView(APIView):
    """
    API view to add a new book.
    """
    def post(self, request):
        book_data = request.data
        book_service = BookService()

        try:
            new_book = book_service.add_new_book(BookRecord(**book_data))
            return Response(new_book, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class RemoveBookView(APIView):
    """
    API view to remove a book by UUID.
    """
    def delete(self, request, book_uuid):
        book_uuid = book_uuid if isinstance(book_uuid, UUID) else UUID(book_uuid)
        book_service = BookService()

        try:
            removed_book = book_service.remove_book(book_uuid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"errors": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

class BorrowedBookListView(APIView):
    """
    API view to list all borrowed books.
    """
    def get(self, request):
        book_service = BookService()
        borrowed_books = book_service.list_borrowed_books()
        return Response(borrowed_books, status=status.HTTP_200_OK)


class BookAvailabilityView(APIView):
    """
    API view to check book availability.
    """
    def get(self, request, book_uuid):
        book_uuid = book_uuid if isinstance(book_uuid, UUID) else UUID(book_uuid)
        book_service = BookService()
        available = book_service.get_book_availability(book_uuid)
        return Response({"available": available}, status=status.HTTP_200_OK)

class BookDetailView(APIView):
    """
    API view to get a single book by its ID.
    """
    def get(self, request, book_uuid):
        book_uuid = book_uuid if isinstance(book_uuid, UUID) else UUID(book_uuid)
        book_service = BookService()
        book = book_service.get_book_by_id(book_uuid)
        return Response(book, status=status.HTTP_200_OK)


class BookFilterView(APIView):
    """
    API view to filter books by publisher and category.
    """
    def get(self, request):
        publisher = request.query_params.get("publisher")
        category = request.query_params.get("category")
        book_service = BookService()
        filtered_books = book_service.filter_books(publisher, category)
        return Response(filtered_books, status=status.HTTP_200_OK)

class UnavailableBooksView(APIView):
    """
    API view to list books that are not available for borrowing.
    """
    def get(self, request):
        book_service = BookService()
        unavailable_books = book_service.list_unavailable_books()
        return Response(unavailable_books, status=status.HTTP_200_OK)