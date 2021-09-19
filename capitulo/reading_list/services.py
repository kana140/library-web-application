from typing import List, Iterable

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import Book, Author, Publisher


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_reading_list(repo: AbstractRepository):
    reading_list = repo.get_reading_list()
    return reading_list


def add_book_to_reading_list(book_id: int, repo: AbstractRepository):
    # Check that the book exists
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    # Update the repo
    repo.add_book_to_reading_list(book)


def remove_book_from_reading_list(book_id: int, repo: AbstractRepository):
    # Check that the book exists
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    #Update the repo
    repo.remove_book_from_reading_list(book)
