from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import insert, select, delete

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from capitulo.domain.model import User, Book, Review, Publisher, Author
from capitulo.adapters.repository import AbstractRepository
from capitulo.adapters.orm import reading_list_table

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
            if book.publisher != None:
                scm.session.add(book.publisher)
            for author in book.authors:
                scm.session.add(author)
            scm.commit()

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None
            pass

        return book

    def get_all_books(self) -> List[Book]:
        books = self._session_cm.session.query(Book).all()
        return books

    def get_books_by_author(self, author: Author) -> List[Book]:
        if author is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            # books = self._session_cm.session.query(Book).filter(author in Book._Book__authors).all()
            result = []
            books = list(self._session_cm.session.query(Book).all())
            for book in books:
                if author in book.authors:
                    result.append(book)
            return result

    def get_books_by_language(self, language: str) -> List[Book]:
        if language is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            # books = self._session_cm.session.query(Book).filter(Book._Book__language == language).all()
            result = []
            books = list(self._session_cm.session.query(Book).all())
            for book in books:
                if book.language == language:
                    result.append(book)
            return result

    def get_books_by_publisher(self, publisher: str) -> List[Book]:
        if publisher is None:
            books = self._session_cm.session.query(Book).all()
            return books
        else:
            # Return books matching author; return an empty list if there are no matches.
            result = []
            books = list(self._session_cm.session.query(Book).all())
            for book in books:
                if book.publisher != None and book.publisher.name == publisher:
                    result.append(book)
            return result
            # books = self._session_cm.session.query(Book).filter(Book._Book__publisher == publisher).all()
            # return books

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

    def get_book_ids_for_author(self, full_name: str):
        book_ids = []

        row = self._session_cm.session.execute('SELECT id FROM authors WHERE full_name = :full_name',
                                               {'full_name': full_name}).fetchone()

        if row is None:
            # No author with the name full_name - create an empty list
            book_ids = list()
        else:
            author_id = row[0]
            # Retrieve book ids of books associated with the author
            book_ids = self._session_cm.session.execute(
                'SELECT book_id FROM book_authors WHERE author_id = :author_id ORDER BY book_id ASC',
                {'author_id': author_id}
            ).fetchall()
            book_ids = [id[0] for id in book_ids]
        return book_ids

    def get_book_ids_for_publisher(self, name: str):
        book_ids = []
        book_ids = self._session_cm.session.execute('SELECT books.book_id FROM publishers LEFT JOIN books ON books.publisher = publishers.name WHERE publishers.name = :name',
                                                    {'name': name}).fetchall()
        if book_ids is None:
            # No existing publisher - create an empty list
            book_ids = list()
        book_ids = [id[0] for id in book_ids]
        return book_ids

    def get_book_ids_for_language(self, language: str):
        book_ids = []
        row = self._session_cm.session.execute('SELECT book_id FROM books WHERE language = :language',
                                               {'language': language}).fetchall()
        if row is None:
            # No author with the name target_author - create an empty list
            book_ids = list()
        else:
            book_ids = [id[0] for id in row]
        return book_ids

    def get_book_ids_for_year(self, year: int):
        book_ids = []
        row = self._session_cm.session.execute('SELECT book_id FROM books WHERE release_year = :year',
                                               {'year': year}).fetchall()
        if row is None:
            # No author with the name target_author - create an empty list
            book_ids = list()
        else:
            book_ids = [id[0] for id in row]
        return book_ids

    def get_number_of_books(self) -> int:
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def get_first_book(self) -> Book:
        book = self._session_cm.session.query(Book).first()
        return book

    def get_last_book(self) -> Book:
        book = self._session_cm.session.query(Book).order_by(Book._Book__id.desc()).first()
        return book

    def get_languages(self):
        # query = self._session_cm.session.query(Book).filter(Book._Book__language)
        row = self._session_cm.session.execute('SELECT language FROM books').fetchall()
        if row is None:
            languages = list()
        else:
            languages = self._session_cm.session.execute(
                'SELECT language FROM books ORDER BY language ASC').fetchall()
            languages = [item[0] for item in languages]
            languages = list(dict.fromkeys(languages))
        return sorted(languages)

    def add_language(self, language: str):
        with self._session_cm as scm:
            scm.session.add(language)
            scm.commit()

    def get_authors(self):
        authors = self._session_cm.session.query(Author).all()
        return sorted(authors)

    def get_publishers(self):
        publishers = self._session_cm.session.query(Publisher).all()
        result = []
        for publisher in publishers:
            result.append(publisher.name)
        return sorted(result)

    def get_release_years(self):
        # query = self._session_cm.session.query(Book).filter(Book._Book__language)
        #row = self._session_cm.session.execute('SELECT release_year FROM books').fetchall()
        #if row is None:
        #    release_year = list()
        #else:
        #    release_year = self._session_cm.session.execute(
        #        'SELECT release_year FROM books ORDER BY release_year ASC').fetchall()
        release_years = self._session_cm.session.execute(
            'SELECT release_year FROM books WHERE release_year IS NOT NULL ORDER BY release_year ASC'
        )
        release_years = [item[0] for item in release_years]
        release_years = list(dict.fromkeys(release_years))
        return release_years

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

    def get_reading_list(self, user_name: str) -> List[Book]:
        # Implement a method of narrowing down the books to only those that are linked to the specified user
        current_user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).first()
        reading_list = current_user.reading_list
        return reading_list

    def add_book_to_reading_list(self, book: Book, user: User):
        stmt = insert(reading_list_table).values(title = book.title, user_name = user.user_name)
        with self._session_cm as scm:
            scm.session.execute(stmt)
            scm.commit()

    def remove_book_from_reading_list(self, book: Book, user):
        stmt = delete(reading_list_table).where(reading_list_table.c.title == book.title, reading_list_table.c.user_name == user.user_name)
        with self._session_cm as scm:
            scm.session.execute(stmt)
            scm.commit()

    def get_book_ids_all(self):
        book_ids = []

        row = self._session_cm.session.execute('SELECT id FROM books').fetchall()
        book_ids = [val[0] for val in row]
        return book_ids

    def get_books_by_id(self, id_list):
        books = self._session_cm.session.query(Book).filter(Book._Book__book_id.in_(id_list)).all()
        return books
