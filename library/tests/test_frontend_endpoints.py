"""
Frontend endpoints tests
"""
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from library.tests.factories import UserFactory, BookFactory, BorrowRecordFactory

# Skip the entire test class if settings.API_NAME is not "admin-api"
@pytest.mark.skipif(settings.API_NAME != "frontend-api", reason="Not the admin API")
@pytest.mark.django_db
class TestFrontendLibraryEndpoints:

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def book(self):
        return BookFactory()

    @pytest.fixture
    def borrow_book(self):
        return BorrowRecordFactory()

    def test_list_books(self, client, book):
        url = reverse('book-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_borrow_book(self, client, book, user):
        url = reverse('borrow-book')
        borrow_data = {
            'user_uuid': str(user.user_uuid),
            'book_uuid': str(book.book_uuid),
            'days': 14
        }
        response = client.post(url, borrow_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_book_detail(self, client, book):
        url = reverse('book-detail', args=[book.book_uuid])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == book.title

    def test_filter_books(self, client, book):
        url = reverse('book-filter')
        filter_data = {
            'publisher': book.publisher,
            'category': book.category,
        }
        response = client.get(url, filter_data)
        assert response.status_code == status.HTTP_200_OK
        # assert len(response.data) > 0

    def test_list_borrowed_books(self, client):
        BorrowRecordFactory()
        url = reverse('borrowed-book-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_check_book_availability(self, client, book):
        url = reverse('book-availability', args=[book.book_uuid])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # assert response.data['availability_status'] == book.availability_status

    def test_enroll_user(self, client):
        url = reverse('enroll-user')
        user_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@example.com'
        }
        response = client.post(url, user_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_borrow_records(self, client, borrow_book):
        url = reverse('user-borrow-records', args=[borrow_book.user.user_uuid])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # assert len(response.data) > 0
