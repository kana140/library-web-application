from datetime import date, datetime
from typing import List

import pytest
from capitulo.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from capitulo.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('keitel', '358473723')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('keitel') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')
    # does not work


def test_repository_does_not_retrieve_a_non_existant_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_books = in_memory_repo.get_number_of_books()


# fix this

def test_repository_can_add_book(in_memory_repo):
    book = Book(342414, "FSOG")
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book(342414) is book


def test_repository_can_retrieve_book(in_memory_repo):
    book = in_memory_repo.get_book(834955)

    assert book.title == "War Stories, Volume 3"
    # expand on this?


def test_repository_does_not_retrieve_a_non_existent_book(in_memory_repo):
    book = in_memory_repo.get_book(467802478)
    assert book is None

def test_repository_can_retrieve_books_by_author(in_memory_repo):
    books = in_memory_repo.get_books_by_author("Garth Ennis")
    assert len(books) == 2

def test_repository_can_retrieve_books_by_language(in_memory_repo):
    books = in_memory_repo.get_books_by_language("English")
    assert len(books) == 15

def test_repository_can_retrieve_books_by_release_year(in_memory_repo):
    books = in_memory_repo.get_books_by_release_year(2006)
    assert len(books) == 2

def test_repository_can_retrieve_books_by_publisher(in_memory_repo):
    books = in_memory_repo.get_books_by_publisher("Avatar Press")
    assert len(books) == 4

def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_author(in_memory_repo):
    books = in_memory_repo.get_books_by_author("ur mum")
    assert books is None
    #actually need to change memory_repository function


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_release_year(in_memory_repo):
    books = in_memory_repo.get_books_by_release_year(3000)
    assert books is None
