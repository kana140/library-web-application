from typing import List, Iterable

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import make_review, Book, Review, Author, Publisher


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(book_id: int, review_text: str, user_name: str, rating: int, repo: AbstractRepository):
    # Check that the book exists
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    # Check if the user exists
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create the review
    review = make_review(book, review_text, rating, user)

    # Update the repo
    repo.add_review(review)


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentBookException

    return book_to_dict(book)


def get_book_ids_for_language(language, repo: AbstractRepository):
    book_ids = repo.get_book_ids_for_language(language)
    return book_ids


def get_books_by_author(author, repo: AbstractRepository):
    books = books_to_dict(repo.get_books_by_author(author))
    return books


def get_books_by_publisher(publisher, repo: AbstractRepository):
    books = books_to_dict(repo.get_books_by_publisher(publisher))
    return books


def get_books_by_release_year(release_year, repo: AbstractRepository):
    books = books_to_dict(repo.get_books_by_release_year(release_year))
    return books


def get_book_ids_for_author(author_name, repo: AbstractRepository):
    book_ids = repo.get_book_ids_for_author(author_name)
    return book_ids


def get_books_by_id(id_list, repo: AbstractRepository):
    books = repo.get_books_by_id(id_list)

    # Convert to dict form
    books_as_dict = books_to_dict(books)

    return books_as_dict


def get_reviews_for_book(book_id, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentBookException

    return reviews_to_dict(book.reviews)


def book_to_dict(book: Book):
    book_dict = {
        'id': book.book_id,
        'title': book.title,
        'reviews': reviews_to_dict(book.reviews),
        'description': book.description,
        'publisher': book.publisher.name,
        'authors': authors_to_dict(book.authors),
        'release_year': book.release_year,
        'image_hyperlink': book.image_hyperlink,
        'ebook': book.ebook,
        'num_pages': book.num_pages,
    }
    return book_dict


def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]


def review_to_dict(review: Review):
    review_dict = {
        'book_id': review.book.book_id,
        'user_name': review.user.user_name,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def author_to_dict(author: Author):
    author_dict = {
        'author_id': author.unique_id,
        'full_name': author.full_name
    }
    return author_dict


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


def dict_to_book(dict):
    book = Book(dict.id, dict.title)
    book_publisher = Publisher(dict.publisher)
    book.publisher = book_publisher
    book.description = dict.description
    book.release_year = dict.release_year
    book.image_hyperlink = dict.image_hyperlink
    book.ebook = dict.ebook
    book.num_pages = dict.num_pages

    # There are no authors or reviews
    return book
