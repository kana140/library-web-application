import csv

from capitulo.adapters.jsondatareader import BooksJSONReader as reader
from pathlib import Path
from datetime import date, datetime
from typing import List
import sys

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from capitulo.adapters.repository import AbstractRepository, RepositoryException
from capitulo.domain.model import Publisher, Author, Book, Review, User, BooksInventory, make_review


class MemoryRepository(AbstractRepository):
    # Books ordered by title, not id. id is assumed unique

    def __init__(self):
        self.__books = list()
        self.__books_index = dict()
        self.__users = list()
        self.__reviews = list()
        self.__languages = list()
        self.__authors = list()
        self.__publishers = list()
        self.__release_years = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_number_of_users(self) -> int:
        return len(self.__users)

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book
        if book.language is not None:
            if book.language not in self.__languages:
                self.__languages.append(book.language)
        if book.authors is not None:
            for author in book.authors:
                if author not in self.__authors:
                    self.__authors.append(author)
        if book.publisher is not None:
            if book.publisher.name not in self.__publishers:
                self.__publishers.append(book.publisher.name)
        if book.release_year is not None:
            if book.release_year not in self.__release_years:
                if book.release_year is not None:
                    self.__release_years.append(book.release_year)

    def get_book(self, id: int) -> Book:
        book = self.__books_index.get(id)
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
        matching_books = [book for book in self.__books if book.release_year == release_year]
        if len(matching_books) == 0:
            return None
        return matching_books

    def get_books_by_publisher(self, publisher: str) -> List[Book]:
        matching_books = [book for book in self.__books if book.publisher.name == publisher]
        if len(matching_books) == 0:
            return None
        return matching_books

    def get_books_by_language(self, language: str) -> List[Book]:
        # Needs to be an exact match for the language we're after.
        matching_books = [book for book in self.__books if book.language == language]
        if len(matching_books) == 0:
            return None
        return matching_books

    def get_books_by_title(self, title: str) -> List[Book]:
        # Doesn't have to be an exact match, as long as the searched for string is a substring of the title.
        matching_books = [book for book in self.__books if title in book.title]
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

    # Reading list implementation
    def get_reading_list(self, user) -> List[Book]:
        return user.reading_list

    def add_book_to_reading_list(self, book: Book, user: User):
        if book not in user.reading_list:
            user.add_to_reading_list(book)

    def remove_book_from_reading_list(self, book: Book, user: User):
        if book in user.reading_list:
            user.remove_from_reading_list(book)

    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_number_of_reviews(self):
        return len(self.__reviews)

    def get_languages(self):
        return self.__languages

    def get_authors(self):
        return sorted(self.__authors)

    def get_publishers(self):
        return sorted(self.__publishers)

    def get_release_years(self):
        return sorted(self.__release_years)

    def get_all_books(self):
        return sorted(self.__books)

    def get_book_ids_for_language(self, language):
        # Needs to be an exact match for the language we're after.
        matching_book_ids = [book.book_id for book in self.__books if book.language == language]
        if len(matching_book_ids) == 0:
            return None
        return matching_book_ids

    def get_book_ids_for_author(self, author_id):
        matching_book_ids = []
        for book in self.__books:
            for author in book.authors:
                if author_id == int(author.unique_id):
                    matching_book_ids.append(book.book_id)
        return matching_book_ids

    def get_book_ids_for_publisher(self, publisher_name: str):
        matching_book_ids = [book.book_id for book in self.__books if publisher_name == book.publisher.name]
        if len(matching_book_ids) == 0:
            return None
        return matching_book_ids

    def get_book_ids_for_year(self, year: int):
        matching_book_ids = [book.book_id for book in self.__books if int(year) == book.release_year]
        if len(matching_book_ids) == 0:
            return None
        return matching_book_ids

    def get_book_ids_all(self):
        book_ids = [book.book_id for book in self.__books]
        if len(book_ids) == 0:
            return None
        return book_ids

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
    users = load_users(data_path, repo)
    load_reviews(data_path, repo, users)


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    comments_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(comments_filename):
        review = make_review(
            book=repo.get_book(int(data_row[2])),
            review_text=data_row[3],
            rating=int(data_row[4]),
            user=users[data_row[1]],

        )
        repo.add_review(review)