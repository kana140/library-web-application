from capitulo.adapters.jsondatareader import BooksJSONReader as reader
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from capitulo.adapters.repository import AbstractRepository, RepositoryException
from capitulo.domain.model import Publisher, Author, Book, Review, User, BooksInventory

class MemoryRepository(AbstractRepository):
    # Books ordered by title, not id. id is assumed unique

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__users = list()
        self.__reviews = list()
        self.__languages = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
    
    def get_number_of_users(self) -> int:
        return len(self.__users)

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book
        if book.language not in self.__languages:
            self.__languages.append(book.language)
    
    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self.__book_index[id]
        except KeyError:
            pass
        return book
    
    def get_books_by_author(self, author: str) -> List[Book]:
        # Searching for one author will return all books done by that author.
        matching_books = []
        for book in self.__books:
            for book_author in book.authors:
                if author in book_author.full_name and book not in matching_books:
                    matching_books.append(book)
        if len(matching_books) == 0:
            return None
        return matching_books
    
    def get_books_by_release_year(self, release_year: int) -> List[Book]:
        matching_books = [ book for book in self.__books if book.release_year == release_year]
        if len(matching_books) == 0:
            return None
        return matching_books

    def get_books_by_publisher(self, publisher: str) -> List[Book]:
        matching_books = [ book for book in self.__books if book.publisher.name == publisher]
        if len(matching_books) == 0:
            return None
        return matching_books
    
    def get_books_by_language(self, language: str) -> List[Book]:
        # Needs to be an exact match for the language we're after.
        matching_books = [ book for book in self.__books if book.language == language ]
        if len(matching_books) == 0:
            return None
        return matching_books

    def get_books_by_title(self, title: str) -> List[Book]:
        # Doesn't have to be an exact match, as long as the searched for string is a substring of the title.
        matching_books = [ book for book in self.__books if title in book.title ]
        if len(matching_books) == 0:
            return None
        return matching_books
    
    def get_number_of_books(self) -> int:
        return len(self.__books)
    
    def get_first_book(self) -> Book:
        if len(self.__books) == 0:
            return None
        return self.__books[0]
    
    def get_last_book(self) -> Book:
        if len(self.__books) == 0:
            return None
        return self.__books[-1]
    
    def add_review(self, review):
        super().add_review
        self.__reviews.append(review)
    
    def get_reviews(self):
        return self.__reviews
    
    def get_number_of_reviews(self):
        return len(self.__reviews)
    
    def get_languages(self):
        return self.__languages

    def get_book_ids_for_language(self, language):
        # Needs to be an exact match for the language we're after.
        matching_book_ids = [ book.book_id for book in self.__books if book.language == language ]
        if len(matching_book_ids) == 0:
            return None
        return matching_book_ids
    
    def get_books_by_id(self, id_list):
        # Strip out unrelated IDs
        correct_ids = [id_val for id_val in id_list if id_val in self.__books_index]

        # Retrieve the books
        books = [self.__books_index[id_val] for id_val in correct_ids]
        return books
    
def populate(data_path: Path, repo: MemoryRepository):
    # Using the JSON data reader we can populate the repository
    books_file_path = data_path / 'comic_books_excerpt.json'
    authors_file_path = data_path / 'book_authors_excerpt.json'
    our_reader = reader(books_file_path, authors_file_path)
    our_reader.read_json_files()
    books_to_load = our_reader.dataset_of_books
    for book in books_to_load:
        repo.add_book(book)
