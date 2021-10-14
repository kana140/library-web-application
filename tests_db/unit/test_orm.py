import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from capitulo.domain.model import User, Book, Review, make_review


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234567"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (book_id, title, description, publisher, author, release_year, num_pages, image_hyperlink, language) VALUES (39338, "book 1", :description, "DC Comics", "an_author", :release_year, :num_pages, :image_hyperlink, :language)',
        {'description': None, 'release_year': None, 'language': None, 'image_hyperlink': None, 'num_pages': None}
    )
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]


def insert_reviewed_book(empty_session):
    article_key = insert_book(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rating = 4

    empty_session.execute(
        'INSERT INTO reviews (user_id, book_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :book_id, "Review 1", :rating, :timestamp_1),'
        '(:user_id, :book_id, "Review 2", :rating, :timestamp_2)',
        {'user_id': user_key, 'book_id': article_key, 'rating': rating, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]


def make_book():
    book = Book(
        39338,
        "book 1"
    )
    return book


def make_user():
    user = User("Andrew", "1111111")
    return user


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234567"))
    users.append(("Cindy", "1111111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234567"),
        User("Cindy", "999999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "1111111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_key == fetched_book.id


def test_loading_of_reviewed_book(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book


def test_saving_of_reviews(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Book.
    review_text = "Some review text."
    rating = 4
    review = make_review(book, review_text, rating, user)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, book_id, review_text, rating FROM reviews'))

    assert rows == [(user_key, book_key, review_text, rating)]


def test_saving_of_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT book_id, title, description, image_hyperlink FROM books'))
    assert rows == [(39338, "book 1", None, None,)]


def test_saving_reading_list(empty_session):
    book = make_book()
    user = make_user()

    # Establish the bidirectional relationship between the Book and the User.
    #make_tag_association(article, tag)
    user.add_to_reading_list(book)

    # Persist the Article (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Article. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT title FROM books'))
    book_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT id, user_name FROM users'))
    user_name = rows[0][1]
    assert rows[0][1] == "Andrew"

    # Check that the reading_list_table table has a new record.
    rows = list(empty_session.execute('SELECT title, user_name from reading_lists'))
    book_foreign_key = rows[0][0]
    user_foreign_key = rows[0][1]

    assert book_key == book_foreign_key
    assert user_name == user_foreign_key


def test_save_reviewed_book(empty_session):
    # Create Book User objects.
    book = make_book()
    user = make_user()

    # Create a new Review that is bidirectionally linked with the User and Book.
    review_text = "Some review text."
    rating = 4
    review = make_review(book, review_text, rating, user)

    # Save the new Book.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_book() checks for insertion into the books table.
    rows = list(empty_session.execute('SELECT id FROM books'))
    article_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, book_id, review_text, rating FROM reviews'))
    assert rows == [(user_key, article_key, review_text, rating)]
