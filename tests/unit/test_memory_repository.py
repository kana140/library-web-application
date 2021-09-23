from datetime import date, datetime
from typing import List

import pytest
from capitulo.domain.model import Publisher, Author, Book, Review, User, BooksInventory, make_review
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

def test_repository_can_retrieve_number_of_users(in_memory_repo):
    users_num = in_memory_repo.get_number_of_users()
    assert users_num == 2


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


def test_repository_can_get_first_book(in_memory_repo):
    assert in_memory_repo.get_first_book().book_id == 707611


def test_repository_can_get_last_book(in_memory_repo):
    assert in_memory_repo.get_last_book().book_id == 35452242


def test_repository_can_get_book_ids_for_language(in_memory_repo):
    book_ids = in_memory_repo.get_book_ids_for_language("French")
    assert len(book_ids) == 1
    assert in_memory_repo.get_book(book_ids[0]).title == "Cruelle"


def test_repository_can_get_book_ids_for_author(in_memory_repo):
    book_ids = in_memory_repo.get_book_ids_for_author(14965)
    assert len(book_ids) == 2
    assert in_memory_repo.get_book(book_ids[0]).title == "War Stories, Volume 3"
    assert in_memory_repo.get_book(book_ids[1]).title == "War Stories, Volume 4"

def test_repository_can_get_book_ids_for_publisher(in_memory_repo):
    book_ids = in_memory_repo.get_book_ids_for_publisher("Avatar Press")
    assert len(book_ids) == 4
    assert in_memory_repo.get_book(book_ids[0]).title == "War Stories, Volume 3"
    assert in_memory_repo.get_book(book_ids[3]).title == "War Stories, Volume 4"

def test_repository_can_get_book_ids_for_year(in_memory_repo):
    book_ids = in_memory_repo.get_book_ids_for_year(1997)
    assert len(book_ids) == 1
    assert book_ids[0] == 707611

def test_repository_can_get_all_book_ids(in_memory_repo):
    book_ids = in_memory_repo.get_book_ids_all()
    assert len(book_ids) == 20


def test_repository_can_get_books_by_id(in_memory_repo):
    books = in_memory_repo.get_books_by_id([707611, 2168737])
    assert books[0].title == "Superman Archives, Vol. 2"
    assert books[1].title == "The Thing: Idol of Millions"

def test_repository_can_retrieve_book(in_memory_repo):
    review1 = None
    review2 = None
    in_memory_repo.add_book(Book(342414, "FSOG"))
    book = in_memory_repo.get_book(342414)
    assert book.title == "FSOG"

    user = User('person', 'whatmakesusure2')
    user2 = User('thorke', 'feoiajf23')
    make_review(book, "it was okay", 4, user)
    make_review(book, "this book saved me", 4, user2)
    for item in book.reviews:
        if item.review_text == "it was okay":
            review1 = item
    for item in book.reviews:
        if item.review_text == "this book saved me":
            review2 = item

    assert review1.user.user_name == 'person'
    assert review2.user.user_name == "thorke"


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


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_release_year(in_memory_repo):
    books = in_memory_repo.get_books_by_release_year(3000)
    assert books is None


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_publisher(in_memory_repo):
    books = in_memory_repo.get_books_by_publisher("publisher")
    assert books is None


def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_language(in_memory_repo):
    books = in_memory_repo.get_books_by_language("piglatin")
    assert books is None


def test_repository_can_get_languages(in_memory_repo):
    languages = in_memory_repo.get_languages()
    assert len(languages) == 6


def test_repository_can_get_authors(in_memory_repo):
    authors = in_memory_repo.get_authors()
    assert len(authors) == 31


def test_repository_can_get_publishers(in_memory_repo):
    publishers = in_memory_repo.get_publishers()
    assert len(publishers) == 12


def test_repository_can_get_release_years(in_memory_repo):
    release_years = in_memory_repo.get_release_years()
    assert len(release_years) == 8


def test_repository_get_books_by_title(in_memory_repo):
    matching_books = in_memory_repo.get_books_by_title("Superman Archives, Vol. 2")
    assert len(matching_books) == 1


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


def test_repository_can_add_a_review(in_memory_repo):
    user = User('thorke', 'feoiajf23')
    book = Book(23553, "my life")
    review = make_review(book, "this book saved me", 4, user)
    in_memory_repo.add_review(review)
    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    book = in_memory_repo.get_book(834955)
    review = Review(book, "i really loved this book like it's my own child", 1, None)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_book_properly_attached(in_memory_repo):
    user = User('thorke', 'feoiajf23')
    review = Review(None, "it was okay", 4, user)

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    # Currently 1 review in the test repository
    assert len(in_memory_repo.get_reviews()) == 1
    review = make_review(Book(45242, 'bookbook'), 'not the best', 4, User('badat', 'Hello343'))
    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_reviews()) == 2
    review2 = make_review(Book(23553, "my life"), 'cool', 4, User('thorke', 'feoiajf23'))
    in_memory_repo.add_review(review2)
    assert len(in_memory_repo.get_reviews()) == 3

