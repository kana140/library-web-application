from datetime import date, datetime

import pytest
import sqlalchemy

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

    books = repo.get_books_by_id([1, 2, 3])

    assert len(books) == 3
    assert books[0].title == 'The Switchblade Mamma'
    assert books[1].title == "Cruelle"
    assert books[2].title == 'Captain America: Winter Soldier (The Ultimate Graphic Novels Collection: Publication Order, #7)'

def test_repository_does_not_retrieve_book_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([4, 665745542, 17405342])

    assert len(books) == 1
    assert books[0].title == "Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC"

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


def test_repository_can_get_books_by_language(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    collection = repo.get_books_by_language("French")
    assert collection[0].title == "Cruelle"


def test_repository_can_get_books_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    collection = repo.get_books_by_publisher("DC Comics")
    assert collection[0].title == "Superman Archives, Vol. 2"


def test_repository_can_get_books_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    collection = repo.get_books_by_title("Superman Archives, Vol. 2")
    assert collection[0].title == "Superman Archives, Vol. 2"


def test_repository_can_get_books_by_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    collection = repo.get_books_by_release_year(1997)
    assert collection[0].title == "Superman Archives, Vol. 2"


def test_repository_returns_book_ids_for_existing_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_ids = repo.get_book_ids_for_author('Florence Dupre la Tour')

    assert book_ids == [2]


def test_repository_returns_book_ids_for_existing_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_ids = repo.get_book_ids_for_publisher('DC Comics')
    assert book_ids == [5]

    book_ids = repo.get_book_ids_for_publisher('Avatar Press')
    assert book_ids == [7, 8, 9, 10]


def test_repository_returns_book_ids_for_existing_language(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_ids = repo.get_book_ids_for_language('English')
    assert book_ids == [1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 19, 20]


def test_repository_returns_book_ids_for_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_ids = repo.get_book_ids_for_year('1997')
    assert book_ids == [5]

def test_repository_can_return_books_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_id([7, 8, 9, 10])
    assert books[0].title == "War Stories, Volume 3"

def test_repository_can_get_reading_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    reading_list = repo.get_reading_list("thorke")
    assert reading_list == []

def test_repository_can_add_to_reading_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_to_add = Book(240, "Happy as Larry")
    new_user = User("Jimmy Johnson", "2348fdsf")
    repo.add_user(new_user)
    repo.add_book(book_to_add)
    repo.add_book_to_reading_list(book_to_add, new_user)
    our_list = repo.get_reading_list(new_user.user_name)
    assert our_list[0] == book_to_add

def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_to_add = Book(240, "Happy as Larry")
    user_to_add = User("Borke, Thorkes Brother", "235546H^")
    review_to_add = Review(book_to_add, "THAT WAS SO GOOD MY SOCKS HAVE BEEN BLOWN OFF", 5, user_to_add)
    repo.add_book(book_to_add)
    repo.add_user(user_to_add)
    same_user = repo.get_user(user_to_add.user_name)
    same_book = repo.get_book(book_to_add.book_id)
    repo.add_book_to_reading_list(same_book, same_user)
    repo.add_review(review_to_add)
    get_our_user = repo.get_user(same_user.user_name)

    assert get_our_user.reviews[0] == review_to_add
    assert book_to_add == same_book
    assert user_to_add == same_user

def test_repository_can_remove_from_reading_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_to_add = Book(240, "Happy as Larry")
    user_to_add = User("Borke, Thorkes Brother", "235546H^")
    review_to_add = Review(book_to_add, "THAT WAS SO GOOD MY SOCKS HAVE BEEN BLOWN OFF", 5, user_to_add)
    repo.add_book(book_to_add)
    repo.add_user(user_to_add)
    same_user = repo.get_user(user_to_add.user_name)
    same_book = repo.get_book(book_to_add.book_id)
    repo.add_book_to_reading_list(same_book, same_user)
    repo.add_review(review_to_add)
    grab_user_back = repo.get_user(same_user.user_name)
    assert grab_user_back.reading_list[0].title == "Happy as Larry"
    
    repo.remove_book_from_reading_list(same_book, same_user)
    get_our_user = repo.get_user(same_user.user_name)

    assert get_our_user.reading_list == []

def test_repository_can_get_all_book_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    test_book_ids = repo.get_book_ids_all()

    assert book_ids == test_book_ids

def test_repository_can_get_books_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    results = repo.get_books_by_id([1, 2, 3])

    assert results[0].title == "The Switchblade Mamma"

def test_repository_can_get_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    results = repo.get_all_books()

    assert results[0].title == "The Switchblade Mamma"

    
