"""
Application Serializer
"""

from rest_framework import serializers
from library.models import BorrowRecord, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'

    book_title = serializers.SerializerMethodField()

    def get_book_title(self, obj):
        return obj.book.title
