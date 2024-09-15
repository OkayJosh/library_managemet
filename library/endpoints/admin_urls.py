"""
Admin API URLs module
"""
from django.urls import path

from library.views.book_vews import AddBookView, UnavailableBooksView, RemoveBookView, BorrowedBookListView
from library.views.user_views import UserListView, UserBorrowedBooksView

urlpatterns = [
    # Add a book to the catalogue/category
    path('books/add/', AddBookView.as_view(), name='add-book'),
    # remove a book from catalogue/category
    path('books/<uuid:book_uuid>/remove/', RemoveBookView.as_view(), name='remove-book'),
    # List users enrolled in the library
    path('users/', UserListView.as_view(), name='user-list'),
    # List the books that are not available for borrowing
    path('books/unavailable/', UnavailableBooksView.as_view(), name='unavailable-books'),
    # List users and the books they have borrowed
    path('users/<uuid:user_uuid>/borrowed/', UserBorrowedBooksView.as_view(), name='user-borrowed-books'),
    # List users and the books they have borrowed
    path('users/borrowed/', BorrowedBookListView.as_view(), name='borrowed-books'),
]
