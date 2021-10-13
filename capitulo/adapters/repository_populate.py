from pathlib import Path

from capitulo.adapters.repository import AbstractRepository
from capitulo.adapters.csv_data_importer import load_reviews, load_users, load_books
from capitulo.adapters.jsondatareader import BooksJSONReader as reader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load books into the repository
    load_books(data_path, repo, database_mode)

    # Load users into the repository
    users = load_users(data_path, repo)

    # Load reviews into the repository:
    load_reviews(data_path, repo, users)
