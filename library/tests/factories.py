"""
Factory boy factory tests
"""
from datetime import timedelta

import factory
from django.utils.timezone import now

from library.models import Book, User, BorrowRecord


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    user_uuid = factory.Faker('uuid4')
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    email = factory.Faker('email')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    book_uuid = factory.Faker('uuid4')
    title = factory.Faker('name')
    publisher = factory.Faker('company')
    category = factory.Faker('word')
    availability_status = True


class BorrowRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BorrowRecord

    user = factory.SubFactory(UserFactory)
    book = factory.SubFactory(BookFactory, availability_status=False)
    borrow_date = factory.LazyFunction(now)
    due_date = factory.LazyFunction(lambda: now() + timedelta(days=14))
    record_uuid = factory.Faker('uuid4')
