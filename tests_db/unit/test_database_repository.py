from datetime import date, datetime

import pytest

import capitulo.adapters.repository as repo
from capitulo.adapters.database_repository import SqlAlchemyRepository
from capitulo.domain.model import Publisher, Author, Book, Review, User, BooksInventory, make_review
from capitulo.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    # Check that the query returned x books.
    assert number_of_books == 20

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_books = repo.get_number_of_books()

    new_book_id = 12345689 + number_of_books

    book = Book(
        new_book_id,
        "Happy Do Lalee"
    )
    repo.add_book(book)

    assert repo.get_book(12345689 + number_of_books) == book

def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(707611)

    # Check that the book has the expected title.
    assert book.title == "Superman Archives, Vol. 2"

    # Check that the book is commented as expected.
    review_one = [review for review in book.reviews if review.review_text == 'Best book ever, the best'][
        0]
    review_two = [review for review in book.reviews if review.review_text == 'Wow! This book was incredible. Super awe-inspiring'][0]
    review_three = [review for review in book.reviews if review.review_text == 'one of the best books ever, brings me back to the time i was a child and no one would talk to me not even my mum or dad good times'][0]

    assert review_one.user.user_name == 'thorke'
    assert review_two.user.user_name == 'thorke'
    assert review_three.user.user_name == 'thorke'

    # Check that the book is tagged as expected.
    assert book.authors[0].full_name == "Jerry Siegel" or "Joe Shuster"
    assert book.authors[1].full_name == "Jerry Siegel" or "Joe Shuster"

def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(201)
    assert book is None

def test_repository_can_retrieve_books_by_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_release_year(2016)

    # Check that the query returned 3 books.
    assert len(books) == 5

    # these books are no jokes...
    books = repo.get_books_by_release_year(1997)

    # Check that the query returned 5 books.
    assert len(books) == 1

def test_repository_does_not_retrieve_a_book_when_there_are_no_books_for_a_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_release_year(2003)
    assert len(books) == 0

def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    reviews = repo.get_reviews()

    assert len(reviews) == 6

    review_one = [review for review in reviews if review.review_text == 'Terrible, just terrible.'][0]
    review_two = [review for review in reviews if review.review_text == 'Best book ever, the best'][0]
    review_three = [review for review in reviews if review.review_text == 'Wow! This book was incredible. Super awe-inspiring'][0]
    review_four = [review for review in reviews if review.review_text == 'one of the best books ever, brings me back to the time i was a child and no one would talk to me not even my mum or dad good times'][0]
    review_five = [review for review in reviews if review.review_text == 'AN ABSOLUTE ROMP'][0]
    review_six = [review for review in reviews if review.review_text == 'This was the greatest thing Ive read since that time I fell over on the pavement and read what someone had written in the concrete when it when it was drying, you know how people do that? They wrote - nice dry -, like - nice try -, but it was in drying concrete! Isnt that just hilarious?!?! But yes this is the second best.'][0]

    assert review_one.user.user_name == "thorke"
    assert review_two.user.user_name == "thorke"
    assert review_three.user.user_name == "thorke"
    assert review_four.user.user_name == "thorke"
    assert review_five.user.user_name == "fmercury"
    assert review_six.user.user_name == "tyler"

def test_repository_can_get_first_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_first_book()
    assert book.title == 'The Switchblade Mamma'

def test_repository_can_get_last_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_last_book()
    assert book.title == 'D.Gray-man, Vol. 16: Blood & Chains'

def test_repository_can_get_books_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([18955715, 17405342, 30735315])

    assert len(books) == 3
    assert books[0].title == 'She Wolf #1'
    assert books[1].title == "Seiyuu-ka! 12"
    assert books[2].title == 'D.Gray-man, Vol. 16: Blood & Chains'

def test_repository_does_not_retrieve_book_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([345, 665745542, 17405342])

    assert len(books) == 1
    assert books[
               0].title == "Seiyuu-ka! 12"

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([0, 199])

    assert len(books) == 0

def test_repository_can_count_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_user = User('Jimmy Jones', 'ho0gwa2tz^T')
    repo.add_user(new_user)

    assert repo.get_number_of_users() == 4

def test_repository_can_get_books_by_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_book = Book(23657, "Jerry and the Jerry-Eaters")
    new_author = Author(5200, "Henry Harrison")
    new_book.add_author(new_author)
    repo.add_book(new_book)

    collection = repo.get_books_by_author(new_author)

    assert collection[0].authors[0].full_name == "Henry Harrison"