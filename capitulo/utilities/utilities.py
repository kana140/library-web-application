from flask import Blueprint, request, render_template, redirect, url_for, session

import capitulo.adapters.repository as repo
import capitulo.utilities.services as services

# Configure the Blueprint
utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_languages_and_urls():
    languages = services.get_languages(repo.repo_instance)
    language_urls = dict()
    for language in languages:
        language_urls[language] = url_for('books_bp.books_by_language', language=language)
    return language_urls


def get_authors_and_urls():
    authors = services.get_authors(repo.repo_instance)
    author_urls = dict()
    for author in authors:
        author_urls[author] = url_for('books_bp.books_by_author', author_name=author.full_name, author_id=author.unique_id)
    return author_urls


def get_publishers_and_urls():
    publishers = services.get_publishers(repo.repo_instance)
    publisher_urls = dict()
    for publisher_name in publishers:
        publisher_urls[publisher_name] = url_for('books_bp.books_by_publisher', publisher_name=publisher_name)
    return publisher_urls


def get_release_years_and_urls():
    release_years = services.get_release_years(repo.repo_instance)
    release_year_urls = dict()
    for release_year in release_years:
        release_year_urls[release_year] = url_for('books_bp.books_by_release_year', release_year=release_year)
    return release_year_urls


def get_book(book_id):
    book = services.get_book(book_id, repo.repo_instance)
    return book

def get_all_books():
    books = services.get_all_books(repo.repo_instance)
    return books
