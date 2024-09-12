"""
Application tasks
"""
import logging

from infrastructure.repositories.book_repository import BookRepository
from infrastructure.repositories.borrow_repository import BorrowRepository
from infrastructure.repositories.user_repository import UserRepository
from library_managemet.celery import app

LOG = logging.getLogger(__name__)

class EventProcessor:
    """
    Class to handle different types of events and delegate them to appropriate repositories.
    """

    def __init__(self):
        self.repositories = {
            "book_events": (self.book_actions, BookRepository()),
            "enroll_events": (self.user_actions, UserRepository()),
            "borrow_events": (self.borrow_actions, BorrowRepository())
        }

    def process_event(self, topic, event):
        """
        Process the incoming event based on the topic.
        :param topic: The event topic (e.g., 'book_events', 'user_events', 'borrow_events').
        :param event: The event data.
        """
        if topic not in self.repositories:
            raise ValueError(f"Unknown topic: {topic}")

        callable_action, repository = self.repositories[topic]
        action = event.get("action")

        LOG.info(f"Processing event {event}, actions {callable_action}, repository {repository}, topic {topic}")
        called_action = callable_action()
        if action not in called_action:
            raise ValueError(f"Unknown action: {action}")

        # Execute the corresponding action
        called_action[action](event, repository)

    def book_actions(self):
        return {
            "add": self.add_book,
            "remove": self.remove_book
        }

    def user_actions(self):
        return {
            "add": self.enroll_user,
            "remove": self.remove_user
        }

    def borrow_actions(self):
        return {
            "add": self.create_borrow_record,
            "remove": self.remove_borrow_record
        }

    def add_book(self, event, repository):
        repository.add_book(event["book"])

    def remove_book(self, event, repository):
        repository.remove_book(event["book_uuid"])

    def enroll_user(self, event, repository):
        repository.enroll_user(event["user"])

    def remove_user(self, event, repository):
        # TODO: implement method for removing user
        repository.remove_user(event["user_uuid"])

    def create_borrow_record(self, event, repository):
        borrow_record = {key: value for key, value in event.items() if key != "action"}
        repository.create_borrow_record(**borrow_record)

    def remove_borrow_record(self, event, repository):
        repository.remove_borrow_record(event["borrow_uuid"])


@app.task
def process_event(topic, event):
    """
    Celery task to process events by delegating to the EventProcessor.
    :param topic: The event topic (e.g., 'book_events', 'user_events', 'borrow_events').
    :param event: The event data.
    """
    processor = EventProcessor()
    processor.process_event(topic, event)
