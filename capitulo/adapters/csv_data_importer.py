import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import Book, User, make_review
from capitulo.adapters.jsondatareader import BooksJSONReader as reader


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file
        headers = next(reader)

        # Read remaining rows from the CSV file
        for row in reader:
            # Strip any leading/trailing white space from data read
            row = [item.strip() for item in row]
            yield row


def load_books(data_path: Path, repo: AbstractRepository, database_mode: bool):
    books_file_path = data_path / 'comic_books_excerpt.json'
    authors_file_path = data_path / 'book_authors_excerpt.json'
    our_reader = reader(books_file_path, authors_file_path)
    our_reader.read_json_files()
    books_to_load = our_reader.dataset_of_books
    for book in books_to_load:
        repo.add_book(book)

def load_users(data_path: Path, repo: AbstractRepository):
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


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    reviews_filename = str(data_path / "reviews.csv")
    for data_row in read_csv_file(reviews_filename):
        review = make_review(
            book=repo.get_book(int(data_row[2])),
            review_text=data_row[3],
            rating=int(data_row[4]),
            user=users[data_row[1]],
        )
        repo.add_review(review)
