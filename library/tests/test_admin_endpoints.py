"""
Admin endpoints tests
"""
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from library.tests.factories import UserFactory, BookFactory, BorrowRecordFactory


# Skip the entire test class if settings.API_NAME is not "admin-api"
@pytest.mark.skipif(settings.API_NAME != "admin-api", reason="Not the admin API")
@pytest.mark.django_db
class TestAdminLibraryEndpoints:

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def book(self):
        return BookFactory()

    @pytest.fixture
    def borrow_book(self):
        return BorrowRecordFactory()

    def test_add_book(self, client):
        url = reverse('add-book')
        book_data = {
            'title': 'Bad Box Man',
            'publisher': 'Joshua',
            'category': 'Fiction',
        }
        response = client.post(url, book_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_remove_book(self, client, book):
        url = reverse('remove-book', args=[book.book_uuid])
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_list(self, client, user):
        url = reverse('user-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_unavailable_books(self, client):
        BookFactory(availability_status=False)
        url = reverse('unavailable-books')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_user_borrowed_books(self, client, borrow_book):
        url = reverse('user-borrowed-books', args=[borrow_book.user.user_uuid])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_borrowed_books(self, client, borrow_book):
        url = reverse('borrowed-books')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
