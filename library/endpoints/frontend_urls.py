"""
Frontend API URLs module
"""
from django.urls import path

from library.views.book_vews import BookListView, BorrowBookView, BorrowedBookListView, \
    BookAvailabilityView, BookDetailView, BookFilterView
from library.views.user_views import EnrollUserView, UserBorrowRecordsView

urlpatterns = [
    # List available books
    path('books/', BookListView.as_view(), name='book-list'),
    # Borrow books by id (specify how long you want it for in days)
    path('books/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    # Get a single book by its ID
    path('books/<uuid:book_uuid>/', BookDetailView.as_view(), name='book-detail'),
    # Filter books by publishers and categories
    path('books/filter/', BookFilterView.as_view(), name='book-filter'),
    # List all borrowed books
    path('books/borrowed/', BorrowedBookListView.as_view(), name='borrowed-book-list'),
    # Check book availability
    path('books/<uuid:book_uuid>/availability/', BookAvailabilityView.as_view(), name='book-availability'),
    # Enroll a new user
    path('users/enroll/', EnrollUserView.as_view(), name='enroll-user'),
    # Get user's borrowed books
    path('users/<uuid:user_uuid>/borrowed/', UserBorrowRecordsView.as_view(), name='user-borrow-records'),
]
