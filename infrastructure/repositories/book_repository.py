"""
Book Repository
"""
from infrastructure.repositories.base_repository import BaseRepository
from library.models import Book


class BookRepository(BaseRepository):
    """
    Repository for handling Book-related database operations.
    """

    def __init__(self, databases=None):
        super().__init__(model_class=Book, databases=databases)

    def add_book(self, book: Book):
        """
        Add a new book to all specified databases.
        :param book: Book instance to add.
        :return: List of results for each database operation.
        """
        return self.add(book)

    def remove_book(self, book_uuid):
        """
        Remove a book from all specified databases.
        :param book_uuid: ID of the book to remove.
        :return: Dictionary of results for each database operation.
        """
        return self.remove(book_uuid=book_uuid)

    def get_book_by_id(self, book_uuid):
        """
        Fetch a book by its ID from the first available database.
        :param book_uuid: ID of the book to fetch.
        :return: Book instance or None if not found.
        """
        return self.get(book_uuid=book_uuid)

    def list_available_books(self):
        """
        List all available books from all specified databases.
        :return: List of books from all databases.
        """
        return self.list(availability_status=True)

    def list_unavailable_books(self):
        """
        List all unavailable books from all specified databases.
        :return: List of books from all databases.
        """
        return self.list(availability_status=False)

    def filter_books(self, publisher=None, category=None):
        """
        Filter books by publisher or category from all specified databases.
        :param publisher: Publisher to filter by.
        :param category: Category to filter by.
        :return: List of filtered books from all databases.
        """
        filters = {'availability_status': True}
        if publisher and category:
            filters['publisher'] = publisher
            filters['category'] = category
        if publisher:
            filters['publisher'] = publisher
        if category:
            filters['category'] = category
        return self.list(**filters)
