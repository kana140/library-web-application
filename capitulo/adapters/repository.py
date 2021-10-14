import abc
from typing import List
from datetime import date

from capitulo.domain.model import Publisher, Author, Book, Review, User, BooksInventory

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a new user account to the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        """ Returns a user account object from the repository by user_name 
            Returns None if there was no associated user """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_users(self) -> int:
        """ Returns the number of users in the repository """
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a book to the repository """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book(self, id: int) -> Book:
        """ Returns a book object from the repository 
            Returns None if there is no associated book """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_books_by_author(self, author: str) -> List[Book]:
        """ Returns a book object from the repository based on the author
            Returns None if there is no associated book """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_books_by_release_year(self, release_year: int) -> List[Book]:
        """ Returns a book object from the repository based on the year
            Returns None if there is no associated book """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_books_by_publisher(self, publisher: str) -> List[Book]:
        """ Returns a book object from the repository based on the year
            Returns None if there is no associated book """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_books_by_author(self, author: str) -> List[Book]:
        """ Returns a book object from the repository based on the author
            Returns None if there are no associated books """
        raise NotImplementedError     
        
    @abc.abstractmethod
    def get_books_by_language(self, language: str) -> List[Book]:
        """ Returns a book object from the repository based on the language
            Returns None if there are no associated books """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_books_by_title(self, title: str) -> List[Book]:
        """ Returns a book object from the repository based on the title
            Returns None if there are no associated books """
        raise NotImplementedError   
    
    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of Books in the repository """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_first_book(self) -> Book:
        """ Returns the first Book object, ordered by id, from the repository 
            Returns None if the repository is empty """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_last_book(self) -> Book:
        """ Returns the last Book object, ordered id, from the repository 
            Returns None if the repository is empty """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reading_list(self, user) -> List[Book]:
        """ Returns the reading list from the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_book_to_reading_list(self, book: Book, user):
        """ Adds a book to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_book_from_reading_list(self, book: Book, user):
        """ Removes book from the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository 
            If the review doesn't have bidirectional links with a Book and a User, this method raises a RepositoryException and doesn't update the repository """
        
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Review not correctly attached to a Book')
    
    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the reviews stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_reviews(self):
        """ Returns the number of reviews stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self):
        """ Returns all books in the repository """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book_ids_for_language(self, language: str):
        """ Returns all the book ids for a given language """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book_ids_for_author(self, author: Author):
        """ Returns all the book ids for a given author """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book_ids_for_publisher(self, publisher: Publisher):
        """ Returns all the book ids for a given publisher """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book_ids_for_year(self, year: int):
        """ Returns all the book ids for a given year """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_book_ids_all(self):
        """ Returns all book ids """
        raise NotImplementedError

    @abc.abstractmethod
    def get_languages(self):
        """ Returns all languages """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_id(self, id_list):
        """ Returns all books by ids """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_authors(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_languages(self):
        raise NotImplementedError