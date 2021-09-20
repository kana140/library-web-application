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
    user = User('fmercury', 'mvNNbc1eLA$i')
    in_memory_repo.add_user(user)
    user_returned = in_memory_repo.get_user('fmercury')
    assert user_returned == user


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_books = in_memory_repo.get_number_of_books()
    assert number_of_books == 20


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
    # actually need to change memory_repository function


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_release_year(in_memory_repo):
    books = in_memory_repo.get_books_by_release_year(3000)
    assert books is None


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_publisher(in_memory_repo):
    books = in_memory_repo.get_books_by_publisher("publisher")
    assert books is None


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_language(in_memory_repo):
    books = in_memory_repo.get_books_by_language("piglatin")
    assert books is None


def test_repository_can_get_langauges(in_memory_repo):
    languages = in_memory_repo.get_languages()
    assert len(languages)


def test_repository_can_retrieve_reading_list_for_user(in_memory_repo):
    book = Book(23553, "my life")
    user = User("iam", "Tired123")
    in_memory_repo.add_user(user)
    book2 = Book(23553, "I have")
    user2 = User("aaaaaaa", "Headache1")
    in_memory_repo.add_user(user2)
    in_memory_repo.add_book_to_reading_list(book, user)
    in_memory_repo.add_book_to_reading_list(book2, user2)
    reading_list = in_memory_repo.get_reading_list(user)
    reading_list2 = in_memory_repo.get_reading_list(user2)
    assert reading_list is not reading_list2


def test_repository_can_add_book_to_reading_list_for_user(in_memory_repo):
    book = Book(23553, "my life")
    user = User("iam", "Tired123")
    in_memory_repo.add_user(user)
    reading_list = in_memory_repo.get_reading_list(user)
    assert reading_list == []
    in_memory_repo.add_book_to_reading_list(book, user)
    assert reading_list[0] == book
    assert len(reading_list) == 1


def test_repository_can_remove_book_from_reading_list_for_user(in_memory_repo):
    book = Book(23553, "my life")
    user = User("iam", "Tired123")
    reading_list = in_memory_repo.get_reading_list(user)
    assert reading_list == []
    in_memory_repo.add_book_to_reading_list(book, user)
    assert len(reading_list) == 1
    in_memory_repo.remove_book_from_reading_list(book, user)
    assert len(reading_list) == 0
