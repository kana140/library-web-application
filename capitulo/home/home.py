from flask import request, Blueprint, render_template, url_for

import math

import capitulo.adapters.repository as repo
import capitulo.utilities.utilities as utilities
import capitulo.home.services as services

from wtforms import Form, StringField, SelectField

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    books_per_page = 4
    page = request.args.get('page')
    q = request.args.get('q')
    books = services.get_all_books(repo.repo_instance)
    languages = utilities.get_languages()
    results = []
    if q:
        for book in books:
            if q.lower() in (book.get('title')).lower():
                results.append(book)
            for author in book.get('authors'):
                if q.lower() in (author.get('full_name')).lower():
                    results.append(book)
            if q.lower() in (book.get('publisher')).lower():
                results.append(book)
            if q.lower() in str(book.get('release_year')).lower():
                results.append(book)
        for language in utilities.get_languages():
            if q.lower() in language.lower():
                for language_book in services.get_books_by_language(language, repo.repo_instance):
                    results.append(language_book)

    return render_template('home/home.html',
        books=results,
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )

######

    if page is None:
        page = 1
    else:
        page = int(page)

    book_ids = services.get_book_ids_all(repo.repo_instance)

    books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(book_ids) / books_per_page)

    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('home_bp.home', page=i))

    return render_template(
        'home/home.html',
        form=search,
        page_list=page_list,
        books=books,
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )


@home_blueprint.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    search = SearchForm(request.form)

    if search.data['search'] == '':
        books_per_page = 4

        page = request.args.get('page')

        if page is None:
            page = 1
        else:
            page = int(page)

        book_ids = services.get_book_ids_all(repo.repo_instance)

        books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page],
                                         repo.repo_instance)

        number_of_pages = math.ceil(len(book_ids) / books_per_page)

        page_list = []
        for i in range(1, number_of_pages + 1):
            page_list.append(url_for('home_bp.home', page=i))

        return render_template(
            'home/home.html',
            page_list=page_list,
            books=books,
            form=search,
            language_urls=utilities.get_languages_and_urls(),
            author_urls=utilities.get_authors_and_urls(),
            publisher_urls=utilities.get_publishers_and_urls(),
            release_year_urls=utilities.get_release_years_and_urls(),
        )
