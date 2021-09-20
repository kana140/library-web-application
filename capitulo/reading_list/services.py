from typing import List, Iterable

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import Book, Author, Publisher, User


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_reading_list(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    reading_list = repo.get_reading_list(user)
    return reading_list


def add_book_to_reading_list(book_id: int, user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    reading_list = repo.get_reading_list(user)
    # Check that the book exists
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    # Update the repo
    repo.add_book_to_reading_list(book, user)


def remove_book_from_reading_list(book_id: int, user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    # Check that the book exists
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    #Update the repo
    repo.remove_book_from_reading_list(book, user)
