from typing import List, Iterable

from capitulo.adapters.repository import AbstractRepository
from capitulo.domain.model import make_review, Book, Review, Author, Publisher


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


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


def get_books_by_author(author):
    return


def authors_to_dict(authors: Iterable[Author]):
    return [author_to_dict(author) for author in authors]


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


def get_all_books(repo: AbstractRepository):
    books = books_to_dict(repo.get_all_books())
    return books


def get_book_ids_all(repo: AbstractRepository):
    books = repo.get_book_ids_all()
    return books


def get_books_by_id(id_list, repo: AbstractRepository):
    books = repo.get_books_by_id(id_list)

    # Convert to dict form
    books_as_dict = books_to_dict(books)

    return books_as_dict


def get_books_by_language(language, repo: AbstractRepository):
    books = books_to_dict(repo.get_books_by_language(language))
    return books
