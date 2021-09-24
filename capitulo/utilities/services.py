from typing import Iterable
import random

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import Book


def get_languages(repo: AbstractRepository):
    languages = repo.get_languages()
    return languages


def get_authors(repo: AbstractRepository):
    authors = repo.get_authors()
    return authors


def get_publishers(repo: AbstractRepository):
    publishers = repo.get_publishers()
    return publishers


def get_release_years(repo: AbstractRepository):
    release_years = repo.get_release_years()
    return release_years


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)
    return book


def get_all_books(repo: AbstractRepository):
    books = repo.get_all_books()
    return books


def get_books_by_author(author, repo: AbstractRepository):
    books = repo.get_books_by_author(author)
    return books
