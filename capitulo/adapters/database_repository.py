from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from capitulo.domain.model import User, Book, Review, Publisher, Author
from capitulo.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_number_of_users(self):
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__id == id).one()
        except NoResultFound:
            # Ignore any exception and return None
            pass

        return book

    def get_all_books(self) -> List[Book]:
        books = self._session_cm.session.query(Book).all()
        return books

    def get_books_by_author(self, author: str) -> List[Book]:
        if author is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(author in Book._Book__authors).all()
            return books

    def get_books_by_language(self, language: str) -> List[Book]:
        if language is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book._Book__language == language).all()
            return books

    def get_books_by_publisher(self, publisher: str) -> List[Book]:
        if publisher is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book._Book__publisher == publisher).all()
            return books

    def get_books_by_title(self, title: str) -> List[Book]:
        if title is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book._Book__title == title).all()
            return books

    def get_books_by_release_year(self, release_year: int) -> List[Book]:
        if release_year is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            books = self._session_cm.session.query(Book).filter(Book._Book__release_year == release_year).all()
            return books

    def get_book_ids_for_author(self, target_author: str):
        book_ids = []

        row = self._session_cm.session.execute('SELECT author_id FROM authors WHERE author_full_name = :target_author', {'author_full_name': target_author}).fetchone()

        if row is None:
            # No author with the name target_author - create an empty list
            book_ids = list()
        else:
            author_id = row[0]
            # Retrieve book ids of books associated with the language
            book_ids = self._session_cm.session.execute(
                'SELECT book_id FROM book_authors WHERE author_full_name = :target_author ORDER BY book_id ASC',
                {'author_id': author_id}
            ).fetchall()
            book_ids = [id[0] for id in book_ids]
        return book_ids

    def get_book_ids_for_publisher(self, target_publisher: str):
        book_ids = []

        row = self._session_cm.session.execute('SELECT id FROM publishers WHERE publisher_name = :target_publisher',
                                               {'publisher_name': target_publisher}).fetchone()

        if row is None:
            # No author with the name target_author - create an empty list
            book_ids = list()
        else:
            publisher_id = row[0]
            # Retrieve book ids of books associated with the language
            book_ids = self._session_cm.session.execute(
                'SELECT book_id FROM book_authors WHERE publisher_name = :target_publisher ORDER BY book_id ASC',
                {'publisher_id': publisher_id}
            ).fetchall()
            book_ids = [id[0] for id in book_ids]
        return book_ids

    def get_number_of_books(self) -> int:
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def get_first_book(self) -> Book:
        book = self._session_cm.session.query(Book).first()
        return book

    def get_last_book(self) -> Book:
        book = self._session_cm.session(Book).first()
        return book

    def get_languages(self):
        #query = self._session_cm.session.query(Book).filter(Book._Book__language)
        row = self._session_cm.session.execute('SELECT language FROM books').fetchall()
        if row is None:
            languages = list()
        else:
            languages = self._session_cm.session.execute(
                'SELECT language FROM books ORDER BY language ASC').fetchall()
        return languages

    def add_language(self, language: str):
        with self._session_cm as scm:
            scm.session.add(language)
            scm.commit()

    def get_authors(self):
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_publishers(self):
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def get_release_years(self):
        #query = self._session_cm.session.query(Book).filter(Book._Book__language)
        row = self._session_cm.session.execute('SELECT release_year FROM books').fetchall()
        if row is None:
            languages = list()
        else:
            languages = self._session_cm.session.execute(
                'SELECT release_year FROM books ORDER BY release_year ASC').fetchall()
        return languages

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_number_of_reviews(self):
        number_of_reviews = self._session_cm.session.query(Review).count()
        return number_of_reviews

    def get_reading_list(self, user) -> List[Book]:
        pass

    def add_book_to_reading_list(self, book: Book, user):
        pass

    def remove_book_from_reading_list(self, book: Book, user):
        pass

    def get_book_ids_for_language(self, language: str):
        pass

    def get_book_ids_for_year(self, year: int):
        pass

    def get_book_ids_all(self):
        pass




